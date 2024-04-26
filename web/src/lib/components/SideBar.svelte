<script lang="ts">
  import { ListBox, ListBoxItem, getModalStore } from '@skeletonlabs/skeleton';
  import type { ModalSettings } from '@skeletonlabs/skeleton';

  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faKey, faTrash } from '@fortawesome/free-solid-svg-icons';
  import { clearChats } from '$lib/chatUtils';
  import { chats, currentChatIndex, current_chat_id } from '$lib/store';

  $: currentChat = $chats[$currentChatIndex]?.title;

  function setCurrentChat(index: number) {
    currentChatIndex.set(index);

    const selectedChatId = $chats[index]?.chat_id;
    current_chat_id.set(selectedChatId);
  }

  const modalStore = getModalStore();
  function handleOpenModal() {
    const modal: ModalSettings = {
      type: 'component',
      component: 'keySettingsModal'
    };
    modalStore.trigger(modal);
  }
  function removeChat(index: number) {
    if ($chats.length === 1) {
      return;
    }
    if (index === $currentChatIndex) {
      setCurrentChat(0);
    }

    $chats = $chats.filter((_, i) => i !== index);
  }
</script>

<div class="flex flex-col h-full variant-soft-surface">
  <!-- Set the flex direction to column and height to full -->

  <header class="border-b border-surface-500/30 p-4">
    <input class="input" type="search" placeholder="Search History" disabled />
  </header>

  <!-- List -->
  <div class="flex-grow p-4 space-y-4 overflow-y-auto">
    <!-- flex-grow will make this div take up all available space -->
    <small class="opacity-50">Chat History</small>
    <ListBox active="variant-filled-primary">
      {#each $chats as chat, index}
        <ListBoxItem
          on:click={() => setCurrentChat(index)}
          bind:group={currentChat}
          name="questions"
          value={chat.title}
        >
          <div class="flex justify-between items-center">
            <span>{chat.title.slice(0, 50) + '...'}</span>
            <button class="ml-auto" on:click={() => removeChat(index)}>X</button>
          </div>
        </ListBoxItem>
      {/each}
    </ListBox>
  </div>

  <!-- Buttons -->
  <div class="mx-1 mb-1 space-y-1 px-2">
    <!-- This div wraps your buttons and pushes them to the bottom -->
    <button type="button" class="btn variant-filled w-full mb-1" on:click={handleOpenModal}>
      <FontAwesomeIcon icon={faKey} />
      <span>Key Settings</span>
    </button>
    <button type="button" class="btn variant-filled-primary w-full" on:click={clearChats}>
      <FontAwesomeIcon icon={faTrash} />
      <span>Clear Chats</span>
    </button>
  </div>

  <footer class="border-t border-surface-500/30 p-4 opacity-50">
    © 2023 LLaMP. All Rights Reserved.
  </footer>
</div>
