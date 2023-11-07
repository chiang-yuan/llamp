<script lang="ts">
  import { mpAPIKey, OpenAiAPIKey } from '$lib/store.ts';
  import type { SvelteComponent } from 'svelte';
  export let parent: SvelteComponent;

  const cBase = 'card p-4 w-modal shadow-xl space-y-4';
  const cHeader = 'text-2xl font-bold';
  const cForm = 'p-4 space-y-4 rounded-container-token';
</script>

<div class="modal-example-form {cBase}">
  <header class={cHeader}>Setting API Keys 🔑</header>
  <!-- Enable for debugging: -->
  <form class="modal-form {cForm}">
    <label class="label">
      <span>OPENAI_API_KEY</span>
      <input class="input" type="password" bind:value={$OpenAiAPIKey} placeholder="sk-xxx" />
    </label>
    <label class="label">
      <span>MP_API_KEY</span>
      <input
        class="input"
        type="password"
        bind:value={$mpAPIKey}
        placeholder="Your Materials Project API Key"
      />
    </label>
  </form>
  <!-- prettier-ignore -->
  <footer class="modal-footer {parent.regionFooter}">
        <button class="btn {parent.buttonPositive}" on:click={parent.onClose}>Ok</button>
    </footer>
</div>
