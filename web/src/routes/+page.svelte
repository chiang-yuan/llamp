<script lang="ts">
  import SideBar from '$lib/components/SideBar.svelte';

  import Message from '../lib/components/Message.svelte';
  import { Avatar, getDrawerStore } from '@skeletonlabs/skeleton';

  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faPaperPlane, faBars } from '@fortawesome/free-solid-svg-icons';
  import { onMount } from 'svelte';
  import { type Chat, type ChatMessage, syncChats, type SimulationDataItem } from '$lib/chatUtils';
  import { OpenAiAPIKey, mpAPIKey, keyNotSet, chats, currentChatIndex } from '$lib/store';

  const API_ENDPOINT =
    process.env.NODE_ENV === 'production'
      ? 'http://ingress.llamp.development.svc.spin.nersc.org/api'
      : 'http://localhost:8000/api';

  let loading = true;

  onMount(() => {
    loading = false;
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

  async function askQuestion() {
    if (!currentMessage || processing) return;

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
      const response = await fetch(`${API_ENDPOINT}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      });

      const result = await response.json();
      const responses: ChatMessage[] = result.responses.map((r: ChatMessage) => ({
        ...r
      }));
      appendResponse(responses);
      const structures = result.structures;

      let simulation_data = result.simulation_data;
      if (simulation_data?.length > 0) {
        simulation_data = JSON.parse(simulation_data);
        simulation_data = simulation_data
          .map((r: SimulationDataItem) => ({
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
