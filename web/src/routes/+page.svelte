<script lang="ts">
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
      : 'http://localhost:8000';

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

  function parseActionInput(input: string): string {
    const prefix = 'Final Output: Action:';
    if (!input.startsWith(prefix)) {
      return input;
    }
    const jsonPart = input.substring(prefix.length).trim();
    const match = /"action_input"\s*:\s*"((?:\\.|[^"\\])*)"/.exec(jsonPart);

    if (!match || match.length < 2) {
      return input;
    }
    return match[1].replace(/\\n/g, '\n');
  }

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
        chat_id: $current_chat_id
      })
    });

    if (!response.body) {
      throw new Error('No response body');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    const stack = [];
    let currentSection = '';
    let newChatId: string = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const tokens = decoder.decode(value, { stream: true });
      if (tokens.startsWith('[chat_id]')) {
        newChatId = tokens.substring(9).trim();
        continue;
      }

      if (tokens.startsWith('[structures]')) {
        appendStructures(tokens.substring(12).split(','));
        continue;
      }

      for (let token of tokens) {
        if (token === '{') {
          stack.push(token);
          currentSection += token;
        } else if (token === '}') {
          if (stack.length > 0 && stack[stack.length - 1] === '{') {
            stack.pop();
            currentSection += token;
            if (stack.length === 0) {
              if (currentSection.startsWith('{"simulation_data"')) {
                return appendSimulation(JSON.parse(currentSection), []);
              } else {
                const content = parseActionInput(currentSection);

                if (content.length > 0) {
                  appendResponses([
                    {
                      role: 'assistant',
                      content,
                      type: 'msg',
                      timestamp: new Date()
                    }
                  ]);
                }
              }
              currentSection = ''; // Reset for the next section
            }
          } else {
            // Handle mismatched closing brace if necessary
            console.error('Mismatched closing brace encountered');
          }
        } else {
          currentSection += token;
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

    if (currentSection !== '') {
      console.error('Incomplete section encountered at the end of the stream');
    }
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

      // Update chat_id
      //  chats.update((currentChats: Chat[]) => {
      //    if (!currentChats[$currentChatIndex].chat_id) {
      //      currentChats[$currentChatIndex].chat_id = updated_chat_id;
      //    }
      //    return updated_chat_id;
      //  });

      //current_chat_id.set(updated_chat_id);
    } catch (error) {
      console.error('Error while asking question:', error);
    } finally {
      processing = false;
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
