<script lang="ts">
  import { closeModal } from 'svelte-modals';
  import { mpAPIKey, OpenAiAPIKey } from '$lib/store.ts';
  export let isOpen: boolean;
</script>

<div class="modal-wrapper">
  {#if isOpen}
    <div role="dialog" class="modal">
      <div class="contents">
		<label for="openai-token" class="text-surface-100-800-token">OpenAI API Key</label>
        <textarea
          bind:value={$OpenAiAPIKey}
          class="bg-slate-50 text-black border-0 ring-0 w-full border-t border-surface-500/30 rounded-md"
          name="openai-token"
          id="openai-token"
          placeholder="Put your OpenAI API Key here"
          rows="1"
        />
		<label for="openai-token" class="text-surface-100-800-token">MP API Key</label>
        <textarea
          bind:value={$mpAPIKey}
          class="bg-slate-50 text-black border-0 ring-0 w-full border-t border-surface-500/30 rounded-md"
          name="openai-token"
          id="openai-token"
          placeholder="Put your MP API Key here"
          rows="1"
        />
        <div class="arrow bg-surface-100-800-token" />
		<div class="my-2" />
		<button class="btn variant-filled mx-1 mb-1" on:click={closeModal}>OK</button>
      </div>
    </div>
  {/if}
</div>

<style>
  .modal-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* Optional: for a backdrop */
  }
  .modal {
    position: fixed;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;

    /* allow click-through to backdrop */
    pointer-events: none;
  }

  .contents {
    min-width: 500px;
    border-radius: 6px;
    padding: 16px;
    background: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    pointer-events: auto;
  }

  .actions {
    margin-top: 32px;
    display: flex;
    justify-content: flex-end;
  }
</style>
