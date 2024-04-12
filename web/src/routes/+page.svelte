<script lang="ts">
  import { OpenAiOrg } from './../lib/store.ts';
  import SideBar from '$lib/components/SideBar.svelte';

  import Message from '../lib/components/Message.svelte';
  import { Avatar, getDrawerStore } from '@skeletonlabs/skeleton';

  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faPaperPlane, faBars } from '@fortawesome/free-solid-svg-icons';
  import { onMount } from 'svelte';
  import { type Chat, type ChatMessage } from '$lib/chatUtils';
  import {
    OpenAiAPIKey,
    mpAPIKey,
    keyNotSet,
    chats,
    currentChatIndex,
    current_chat_id
  } from '$lib/store';

  const BASE_URL =
    process.env.NODE_ENV === 'production'
      ? 'http://ingress.llamp.development.svc.spin.nersc.org/api'
      : 'http://localhost:8000/api';

  let loading = true;

  onMount(() => {
    loading = false;
    if ($chats[0].chat_id) {
      current_chat_id.set($chats[0].chat_id);
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
  //  let updated_chat_id = '';

  async function getStream(message: ChatMessage) {
    const response = await fetch(`${BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: message.content,
        OpenAiAPIKey: $OpenAiAPIKey,
        mpAPIKey: $mpAPIKey,
        OpenAiOrg: $OpenAiOrg,
        chat_id: $current_chat_id
      })
    });

    if (!response.body) {
      throw new Error('No response body');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    let newChatId: string = '';
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      if (chunk.startsWith('[chat_id]')) {
        newChatId = chunk.substring(9).trim();
        continue;
      }

      if (chunk.startsWith('[structures]')) {
        appendStructures(chunk.substring(12).split(','));
        continue;
      }
      buffer += chunk;

      let startIdx = 0;
      while ((startIdx = buffer.indexOf('```', startIdx)) !== -1) {
        const endIdx = buffer.indexOf('```', startIdx + 3);
        if (endIdx !== -1) {
          if (buffer.substring(startIdx, startIdx + 7) === 'json') {
          }
          if (startIdx > 0 && !buffer.startsWith('Action:')) {
            appendResponses([
              {
                role: 'assistant',
                content: buffer
                  .substring(0, startIdx)
                  .replace('Thought:', '<p class="font-bold">🤔 Thought:</p>')
                  .replace('Action:', '')
                  .trim(),
                type: 'msg',
                timestamp: new Date()
              }
            ]);
          }
          let codeBlock = buffer.substring(startIdx + 3, endIdx);
          if (codeBlock.startsWith('json')) {
            codeBlock = codeBlock.substring(4);
          }

          try {
            let { action, action_input } = JSON.parse(codeBlock);
            let content = '';
            if (action == 'Final Answer') {
              //  content += `<p> <span class="font-bold">✅ Final Answer: </span></p>`;
            } else if (action.includes('MP')) {
              content += `<p> <span class="font-bold">🔨 Tool: </span>${action}</p>`;
            } else if (action.includes('_')) {
              content += `<p class="font-bold"> </p>`;
              content += `<p> <span class="font-bold">🔮 API Endpoint: </span>${action}</p>`;
            } else {
              content += `<p class="font-bold">${action}</p>`;
            }
            if (typeof action_input === 'string') {
              content += action_input;
            } else if (action_input?.input) {
              content += action_input.input;
            } else if (action.includes('_')) {
              content += `
			  <div class="codeblock overflow-hidden shadow bg-neutral-900/90  text-sm text-white rounded-container-token shadow " data-testid="codeblock"><header class="codeblock-header text-xs text-white/50 uppercase flex justify-between items-center p-2 pl-4"><span class="codeblock-language">parameters</span></header> <pre class="codeblock-pre whitespace-pre-wrap break-all p-4 pt-1"><code class="codeblock-code language-plaintext lineNumbers">${JSON.stringify(action_input).trim()}</code></pre></div>`;
            } else {
              content += JSON.stringify(action_input).trim();
            }
            appendResponses([
              {
                role: 'assistant',
                content: content,
                type: 'msg',
                timestamp: new Date()
              }
            ]);
          } catch (error) {
            console.error('Failed to parse JSON:', error);
          }

          buffer = buffer.substring(endIdx + 3);
        } else {
          break;
        }
      }
    }
    current_chat_id.set(newChatId);
    chats.update((currentChats: Chat[]) => {
      if (!currentChats[$currentChatIndex].chat_id) {
        currentChats[$currentChatIndex].chat_id = newChatId;
      }
      return currentChats;
    });
  }

  async function askQuestion() {
    if (!currentMessage || processing) {
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

    currentMessage = '';

    try {
      processing = true;
      await getStream(newMessage);
    } catch (error) {
      console.error('Error while asking question:', error);
    } finally {
      processing = false;
    }
  }

  async function loadStructures(materialIds: string[]): Promise<string[]> {
    const structures = await Promise.all(
      materialIds.map(async (materialId) => {
        const response = await fetch(`${BASE_URL}/structures/${materialId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch structure');
        }

        const data = await response.json();
        return data;
      })
    );

    return structures as string[];
  }

  async function appendStructures(materialIds: string[]) {
    const structures = await loadStructures(materialIds);

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

  function appendResponses(responses: ChatMessage[]) {
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
    current_chat_id.set(undefined);
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
