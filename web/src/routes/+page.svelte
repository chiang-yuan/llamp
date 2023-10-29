<script lang="ts">
  import Message from './Message.svelte';
  import { Avatar, ListBox, ListBoxItem, popup, type PopupSettings} from '@skeletonlabs/skeleton';
  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faPaperPlane, faKey } from '@fortawesome/free-solid-svg-icons';
  import { onMount, tick } from 'svelte';
  import { type Chat, type ChatMessage, syncChats } from '$lib/chatUtils';

  const API_ENDPOINT = process.env.NODE_ENV === 'production' ? 'http://165.232.143.186:8000' : 'http://localhost:8000';

  let chats: Chat[] = [];
  let currentChatIndex = 0;
  let loading = true;
  onMount(() => {
    const loadedChats = localStorage.getItem('chats');
    if (loadedChats) {
      chats = JSON.parse(loadedChats);
    }
    if (!loadedChats?.length) {
      chats = [
        {
          question: '',
          title: '',
          messages: []
        }
      ];
    }
	const loadedKey = localStorage.getItem('openaiKey');
	if (loadedKey) {
		OpenAIKey = loadedKey;
	}

	loading = false;
  });

  function addMessage(newMessage: ChatMessage) {
    chats[currentChatIndex].messages.push({
		...newMessage,
		timestamp: new Date(),
	});
    syncChats(chats);
  }
  $: messages = chats.length ? chats[currentChatIndex].messages : [];

  $: currentChat = chats[currentChatIndex]?.title;

  let currentMessage = '';
  let processing = false;

  async function askQuestion() {
    if (!currentMessage || processing) return;
    const newMessage: ChatMessage = {
      role: 'user',
      content: currentMessage,
      type: 'msg',
    };

    // Adding user's message to the chat immediately
    addMessage(newMessage);
    messages = chats[currentChatIndex].messages;
    await scrollToBottom();

    if (chats[currentChatIndex].messages.length === 1) {
      chats[currentChatIndex].title = currentMessage;
      chats[currentChatIndex].question = currentMessage;
    }

    const body = {
		messages,
		key: OpenAIKey,
	};
    currentMessage = '';

    try {
      processing = true;
      await scrollToBottom();
      const response = await fetch(`${API_ENDPOINT}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      });

      const result = await response.json();
      const responses: ChatMessage[] = result.responses.map((r) => ({
		...r,
	  }));
      console.log(responses);
      appendResponse(responses);
	  const structures = result.structures;
	  if (structures.length > 0) {
		appendStructures(structures);
	  }
	  console.log(structures);

      syncChats(chats); // Syncing the chat after receiving the assistant’s response
    } catch (error) {
      console.error('Error while asking question:', error);
    } finally {
      processing = false;
    }
  }

  function appendStructures(structures: any[]) {
	const msg = {
			role:'assistant',
			content: "",
			type: 'structures',
			structures: structures,
			timestamp: new Date(),
		}
	messages = [
		...messages,
		msg
	]
	addMessage(msg);
  }
  function appendResponse(responses: ChatMessage[]) {
    messages = [
      ...messages,
      ...responses.map((r) => ({
        ...r,
        type: 'msg',
		timestamp: new Date(),
      }))
    ];

    for (const response of responses) {
      addMessage(response);
    }
  }

  function createNewChat() {
    const newChat: Chat = {
      question: '',
      title: '',
      messages: []
    };
    chats = [newChat, ...chats];
    currentChatIndex = 0;
  }

  function setCurrentChat(index: number) {
    currentChatIndex = index;
    messages = chats[currentChatIndex].messages; // Updating messages to display the correct chat conversation
  }

  $: isCurrentChatEmpty =
    chats[currentChatIndex]?.messages.length === 0 && !chats[currentChatIndex]?.title;

  let chatContainer: HTMLElement;
  async function scrollToBottom() {
    await tick();
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  const popOpenAIKey: PopupSettings = {
	event: 'click',
	target: 'popOpenAIKey',
	placement: 'top',
	state: (e: Record<string ,boolean>) => {
		if (!e.state) {
			// store openaiKey in localstorage
			localStorage.setItem('openaiKey', OpenAIKey);
		}
	},
  };

  let OpenAIKey = '';

</script>

{#if loading}
	<div class="flex justify-center items-center h-screen">
		<h1>Loading...</h1>
	</div>
{:else}
<div class="chat w-full h-full grid grid-cols-1 lg:grid-cols-[20%_1fr]">
  <!-- Navigation -->
  <div class="hidden card lg:grid grid-rows-[auto_1fr_auto] border-r border-surface-500/30">
    <!-- Header -->
    <header class="border-b border-surface-500/30 p-4">
      <input class="input" type="search" placeholder="Search History" disabled />
    </header>
    <!-- List -->
    <div class="p-4 space-y-4 overflow-y-auto">
      <small class="opacity-50">Chat History</small>
      <ListBox active="variant-filled-primary">
        {#each chats as chat, index}
          <ListBoxItem
            on:click={() => setCurrentChat(index)}
            bind:group={currentChat}
            name="questions"
            value={chat.title}
          >
            {chat.title.slice(0, 50) + '...'}
          </ListBoxItem>
        {/each}
      </ListBox>
    </div>
    <!-- Footer -->
	<button type="button" class="btn variant-filled mx-1" use:popup={popOpenAIKey}>
		<FontAwesomeIcon icon={faKey} />
		<span>OpenAI API KEY</span>
	</button>

	<div class="card p-4 w-96 shadow-xl " data-popup="popOpenAIKey">
        <textarea
          bind:value={OpenAIKey}
          class="bg-slate-50 text-black border-0 ring-0 w-full border-t border-surface-500/30 rounded-md"
          name="openai-token"
          id="openai-token"
          placeholder="Put your OpenAI token here"
          rows="1"
        />
		<div class="arrow bg-surface-100-800-token" />
	</div>

    <footer class="border-t border-surface-500/30 p-4 opacity-50">
      LLaMP Project All Rights Reserved.
    </footer>
  </div>

  <!-- Chat -->
  <div class="flex flex-col h-full">
    <!-- Conversation -->
    <section
      bind:this={chatContainer}
      id="chat-conversation"
      class="p-4 overflow-y-auto flex-grow space-y-4"
    >
      {#each messages as msg}
        <Message data={msg} />
      {/each}
      {#if processing}
        <div class="flex gap-2">
          <div>
            <Avatar width="w-12" initials="🔮" />
          </div>
          <div class="card p-4 rounded-tl-none space-y">
            <header class="flex justify-between items-center">
              <p class="font-bold">LLaMP</p>
            </header>
            <div class="placeholder animate-pulse my-2 w-96" />
          </div>
        </div>
      {/if}
    </section>
    <!-- Prompt -->
    <section class="card border-t border-surface-500/30 p-4">
      <div
        class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token"
      >
        <button
          class="input-group-shim"
          on:click={createNewChat}
          disabled={processing || isCurrentChatEmpty}>+</button
        >
        <textarea
          bind:value={currentMessage}
          class="bg-transparent border-0 ring-0"
          name="prompt"
          id="prompt"
          placeholder="Ask a question..."
          rows="1"
          on:keyup={(e) => {
            e.preventDefault();
            if (e.key === 'Enter') askQuestion();
          }}
          disabled={processing}
        />
        <button
          class={currentMessage ? 'variant-filled-primary' : 'input-group-shim'}
          on:click={askQuestion}
          disabled={processing}
        >
          <FontAwesomeIcon icon={faPaperPlane} />
        </button>
      </div>
    </section>
  </div>
</div>

<style>
  #chat-conversation {
    overflow-y: auto;
    height: calc(100vh - 200px); /* Adjust the height based on your header and footer */
  }
</style>

{/if}