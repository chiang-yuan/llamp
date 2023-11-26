<script lang="ts">
  import SideBar from '$lib/components/SideBar.svelte';

  import Message from '../lib/components/Message.svelte';
  import { Avatar, getDrawerStore } from '@skeletonlabs/skeleton';

  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faPaperPlane, faBars } from '@fortawesome/free-solid-svg-icons';
  import { onMount, onDestroy } from 'svelte';
  import { type Chat, type ChatMessage, syncChats, type SimulationDataItem } from '$lib/chatUtils';
  import { OpenAiAPIKey, mpAPIKey, keyNotSet, chats, currentChatIndex } from '$lib/store';

  const WS_ENDPOINT =
	process.env.NODE_ENV === 'production'
		? 'ws://ingress.llamp.development.svc.spin.nersc.org/ws'
		: 'ws://localhost:8000/ws';

  let loading = true;

  onMount(() => {
    loading = false;
	openWebSocket();
  });

    onDestroy(() => {
    if (websocket) {
      websocket.close();
    }
  });

  function addMessage(newMessage: ChatMessage) {
    newMessage = {
      ...newMessage,
      timestamp: new Date()
    };
    chats.update((currentChats: Chat[]) => {
      const updatedChats = [...currentChats];
      const updatedMessages = [...updatedChats[$currentChatIndex].messages, newMessage];
      updatedChats[$currentChatIndex].messages = updatedMessages;
      return updatedChats;
    });
  }

  let currentMessage = '';
  let processing = false;
  let websocket: WebSocket|null = null;

async function openWebSocket() {
	if (websocket && websocket.readyState === WebSocket.OPEN) {
		return;
	}
    websocket = new WebSocket(WS_ENDPOINT);

    websocket.onmessage = function(event) {
console.log(event);
      const result = JSON.parse(event.data);
      processWebSocketResponse(result);
    };

    websocket.onerror = function(event) {
      console.error('WebSocket error:', event);
    };

    websocket.onclose = function(event) {
      console.log('WebSocket connection closed:', event);
    };
}

async function processWebSocketResponse(result) {
  const responses = result.responses.map(r => ({ ...r }));
  appendResponse(responses);
  const structures = result.structures;

  let simulation_data = result.simulation_data;
  if (simulation_data?.length > 0) {
    simulation_data = JSON.parse(simulation_data);
    simulation_data = simulation_data
      .map(r => ({
        time: r['Time[ps]'],
        Etot: r['Etot/N[eV]']
      }))
      .slice(0, 10);

    appendSimulation(simulation_data, structures);
  } else if (structures?.length > 0) {
    appendStructures(structures);
  }
  console.log('structures: ', structures);

  syncChats();
}

async function askQuestion() {
  if (!currentMessage || processing) {
	return;
  }
  if (!websocket || websocket.readyState !== WebSocket.OPEN) {
    console.error("WebSocket is not open");
    return;
  }

    const newMessage: ChatMessage = {
      role: 'user',
      content: currentMessage,
      type: 'msg',
      timestamp: new Date() // Assuming you want to add a timestamp here as well
    };

    // Adding user's message to the chat immediately
    addMessage(newMessage);

    chats.update((currentChats: Chat[]) => {
      const updatedChats = [...currentChats];
      if (updatedChats[$currentChatIndex].messages.length === 1) {
        updatedChats[$currentChatIndex].title = currentMessage;
        updatedChats[$currentChatIndex].question = currentMessage;
      }
      return updatedChats;
    });

  const body = {
    messages: $chats[$currentChatIndex].messages,
    openAIKey: $OpenAiAPIKey,
    mpAPIKey: $mpAPIKey
  };

  currentMessage = '';

  try {
    processing = true;

    // Send data over WebSocket
    websocket!.send(JSON.stringify(body));
  } catch (error) {
    console.error('Error while asking question:', error);
  } finally {
    processing = false;
  }
}

// Ensure to call a function to close the WebSocket when the component unmounts or when you are done using it
function closeWebSocket() {
  if (websocket) {
    websocket.close();
  }
}


  function appendSimulation(simulation_data: any[], structures: any[]) {
    chats.update((currentChats: Chat[]) => {
      const updatedChats = [...currentChats]; // Create a shallow copy of the current chats array
      const updatedMessages = [
        ...updatedChats[$currentChatIndex].messages,
        {
          role: 'assistant',
          content: 'Simulation:\n',
          type: 'simulation',
          structures: structures,
          timestamp: new Date()
        },
        {
          role: 'assistant',
          content: 'Chart: ',
          type: 'simulation_chart',
          timestamp: new Date(),
          simulationData: simulation_data
        }
      ];
      updatedChats[$currentChatIndex].messages = updatedMessages;
      return updatedChats;
    });
  }

  function appendStructures(structures: any[]) {
    chats.update((currentChats: Chat[]) => {
      const updatedChats = [...currentChats];
      const updatedMessages = [
        ...updatedChats[$currentChatIndex].messages,
        {
          role: 'assistant',
          content: '',
          type: 'structures',
          structures,
          timestamp: new Date()
        }
      ];
      updatedChats[$currentChatIndex].messages = updatedMessages;
      return updatedChats;
    });
  }

  function appendResponse(responses: ChatMessage[]) {
    chats.update((currentChats: Chat[]) => {
      const updatedChats = [...currentChats];
      const updatedMessages = [
        ...updatedChats[$currentChatIndex].messages,
        ...responses.map((r) => ({
          ...r,
          type: 'msg',
          timestamp: new Date(),
          content: r.content ? r.content : ''
        }))
      ];
      updatedChats[$currentChatIndex].messages = updatedMessages;
      return updatedChats;
    });
  }

  function createNewChat() {
    if (processing) return;
    if ($chats.length === 1 && $chats[0].messages.length === 0) return;
    const newChat: Chat = {
      question: '',
      title: '',
      messages: []
    };
    chats.update((currentChats: Chat[]) => [newChat, ...currentChats]);
    $currentChatIndex = 0;
  }

  $: isCurrentChatEmpty =
    chats[$currentChatIndex]?.messages.length === 0 && !chats[$currentChatIndex]?.title;

  const drawerStore = getDrawerStore();
  function openDrawer() {
    drawerStore.open({ id: 'mobile-chats' });
  }
</script>

<svelte:head>
  <title>LLaMP</title>
</svelte:head>

{#if loading}
  <div class="flex justify-center items-center h-screen">
    <h1>Loading...</h1>
  </div>
{:else}
  <div class="w-full lg:hidden pb-2 bg-surface-100-800-token">
    <button class="btn variant-soft-surface w-full" on:click={openDrawer}>
      <FontAwesomeIcon icon={faBars} />
    </button>
  </div>
  <div class="flex flex-col lg:flex-row w-full">
    <div
      class="hidden lg:flex lg:flex-col lg:sticky lg:top-0 lg:w-[20%] lg:overflow-y-auto"
      style="max-height: calc(100vh - 4.5rem);"
    >
      <SideBar />
    </div>

    <!-- Chat -->
    <div
      class="flex flex-col min-h-[calc(100vh-7.5rem)] lg:min-h-[calc(100vh-5rem)] w-full lg:w-[80%]"
    >
      <!-- Conversation -->
      <section
        id="chat-conversation"
        class="overflow-y-auto flex-grow p-4 space-y-4 variant-soft-surface"
      >
        {#each $chats[$currentChatIndex].messages as msg, index (msg)}
          <Message data={msg} />
        {/each}
        {#if processing}
          <div class="flex gap-2 max-w-[250px] lg:max-w-5xl">
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
      <section class="sticky bottom-0 p-4 border-t border-surface-500/30 variant-soft-surface">
        <div
          class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token"
        >
          <button
            class="input-group-shim"
            on:click={createNewChat}
            disabled={processing || isCurrentChatEmpty || $keyNotSet}>+</button
          >
          <textarea
            bind:value={currentMessage}
            class="bg-transparent border-0 ring-0"
            name="prompt"
            id="prompt"
            placeholder={$keyNotSet
              ? '❌ Please set your API keys in [Key Settings]'
              : 'Ask a question...'}
            rows="1"
            on:keyup={(e) => {
              e.preventDefault();
              if (e.key === 'Enter') askQuestion();
            }}
            disabled={processing || $keyNotSet}
          />
          <button
            class={currentMessage ? 'variant-filled-primary' : 'input-group-shim'}
            on:click={askQuestion}
            disabled={processing || $keyNotSet}
          >
            <FontAwesomeIcon icon={faPaperPlane} />
          </button>
        </div>
      </section>
    </div>
  </div>
{/if}
