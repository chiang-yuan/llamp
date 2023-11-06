<script lang="ts">
  import Message from './Message.svelte';
  import {
    Avatar,
    ListBox,
    ListBoxItem,
    getModalStore,
    Drawer,
    getDrawerStore
  } from '@skeletonlabs/skeleton';
  import type { ModalSettings, DrawerSettings, DrawerStore } from '@skeletonlabs/skeleton';

  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faPaperPlane, faKey, faTrash, faBars } from '@fortawesome/free-solid-svg-icons';
  import { onMount, tick } from 'svelte';
  import {
    type Chat,
    type ChatMessage,
    syncChats,
    clearChats,
    type SimulationDataItem
  } from '$lib/chatUtils';
  import { OpenAiAPIKey, mpAPIKey, keyNotSet, chats } from '$lib/store';

  const API_ENDPOINT =
    process.env.NODE_ENV === 'production'
      ? 'http://ingress.llamp.development.svc.spin.nersc.org/api'
      : 'http://localhost:8000/api';

  let currentChatIndex = 0;
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
      const updatedMessages = [...updatedChats[currentChatIndex].messages, newMessage];
      updatedChats[currentChatIndex].messages = updatedMessages;
      return updatedChats;
    });
  }

  $: currentChat = $chats[currentChatIndex]?.title;

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

    await scrollToBottom();

    chats.update((currentChats: Chat[]) => {
      const updatedChats = [...currentChats];
      if (updatedChats[currentChatIndex].messages.length === 1) {
        updatedChats[currentChatIndex].title = currentMessage;
        updatedChats[currentChatIndex].question = currentMessage;
      }
      return updatedChats;
    });

    const body = {
      messages: $chats[currentChatIndex].messages,
      openAIKey: $OpenAiAPIKey,
      mpAPIKey: $mpAPIKey
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

      await scrollToBottom();
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
        ...updatedChats[currentChatIndex].messages,
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
      updatedChats[currentChatIndex].messages = updatedMessages;
      return updatedChats;
    });
  }

  function appendStructures(structures: any[]) {
    chats.update((currentChats: Chat[]) => {
      const updatedChats = [...currentChats];
      const updatedMessages = [
        ...updatedChats[currentChatIndex].messages,
        {
          role: 'assistant',
          content: '',
          type: 'structures',
          structures,
          timestamp: new Date()
        }
      ];
      updatedChats[currentChatIndex].messages = updatedMessages;
      return updatedChats;
    });
  }

  function appendResponse(responses: ChatMessage[]) {
    chats.update((currentChats: Chat[]) => {
      const updatedChats = [...currentChats];
      const updatedMessages = [
        ...updatedChats[currentChatIndex].messages,
        ...responses.map((r) => ({
          ...r,
          type: 'msg',
          timestamp: new Date(),
          content: r.content ? r.content : ''
        }))
      ];
      updatedChats[currentChatIndex].messages = updatedMessages;
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
    currentChatIndex = 0;
  }

  function setCurrentChat(index: number) {
    currentChatIndex = index;
  }

  $: isCurrentChatEmpty =
    chats[currentChatIndex]?.messages.length === 0 && !chats[currentChatIndex]?.title;

  let chatContainer: HTMLElement;
  async function scrollToBottom() {
    await tick();
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  const modalStore = getModalStore();
  function handleOpenModal() {
    const modal: ModalSettings = {
      type: 'component',
      component: 'keySettingsModal'
    };
    modalStore.trigger(modal);
  }

  const drawerStore = getDrawerStore();
  function openDrawer() {
    drawerStore.open({ id: 'mobile-chats' });
  }
</script>

<div class="hidden card lg:grid grid-rows-[auto_1fr_auto] border-r border-surface-500/30">
  <!-- Header -->
  <header class="border-b border-surface-500/30 p-4">
    <input class="input" type="search" placeholder="Search History" disabled />
  </header>
  <!-- List -->
  <div class="p-4 space-y-4 overflow-y-auto">
    <small class="opacity-50">Chat History</small>
    <ListBox active="variant-filled-primary">
      {#each $chats as chat, index}
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
  <button type="button" class="btn variant-filled mx-1 mb-1" on:click={handleOpenModal}>
    <FontAwesomeIcon icon={faKey} />
    <span>Key Settings</span>
  </button>
  <button type="button" class="btn variant-filled-primary mx-1" on:click={clearChats}>
    <FontAwesomeIcon icon={faTrash} />
    <span>Clear Chats</span>
  </button>

  <footer class="border-t border-surface-500/30 p-4 opacity-50">
    LLaMP Project All Rights Reserved.
  </footer>
</div>
