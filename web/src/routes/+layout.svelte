<script lang="ts">
  import { showAlpha } from './../lib/store.ts';
  import '../app.postcss';
  import { AppShell, AppBar, LightSwitch } from '@skeletonlabs/skeleton';
  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faGithub } from '@fortawesome/free-brands-svg-icons';
  import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
  import { storePopup } from '@skeletonlabs/skeleton';
  import { Modal, initializeStores, Drawer, getDrawerStore } from '@skeletonlabs/skeleton';
  import type { ModalComponent } from '@skeletonlabs/skeleton';
  import KeySettingsModal from './KeySettingsModal.svelte';
  import SideBar from '$lib/components/SideBar.svelte';

  initializeStores();
  storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

  const modalRegistry: Record<string, ModalComponent> = {
    keySettingsModal: { ref: KeySettingsModal }
  };
  const drawerStore = getDrawerStore();
</script>

<svelte:head>
  <title>LLaMP</title>
</svelte:head>

<Modal components={modalRegistry} />
<Drawer>
  {#if $drawerStore.id == 'mobile-chats'}
    <SideBar />
  {/if}
</Drawer>
<!-- App Shell -->
<AppShell class="flex flex-col h-screen">
  <svelte:fragment slot="header">
    <!-- App Bar -->
    <AppBar>
      <svelte:fragment slot="lead">
        <a href="/">
          <span class="lg:inline hidden"
            ><strong class="text-xl">LLaMP 🦙🔮 - Large Language model for Materials Project</strong
            ></span
          >
          <span class="lg:hidden"><strong class="text-xl">LLaMP</strong></span>
        </a>
      </svelte:fragment>
      <svelte:fragment slot="trail">
        <a class="btn bg-gradient-to-br variant-gradient-primary-secondary" href="/">
          <span class="lg:inline hidden">Try Now</span>
        </a>
        <a class="btn bg-gradient-to-br variant-soft-secondary" href="/about">
          <span class="lg:inline hidden">About LLaMP</span>
        </a>
        <a
          class="btn bg-gradient-to-br variant-soft-secondary"
          href="https://materialsproject.org"
          target="_blank"
          rel="noreferrer"
        >
          <span class="lg:inline hidden">Materials Project</span>
        </a>
        <a
          class="btn-icon variant-ghost"
          href="https://github.com/chiang-yuan/llamp"
          target="_blank"
          rel="noreferrer"
          style="font-size: 1.75rem;"
        >
          <FontAwesomeIcon icon={faGithub} />
        </a>
        <LightSwitch height="h-8" width="w-16" />
      </svelte:fragment>
    </AppBar>
  </svelte:fragment>
  <!-- Page Route Content -->
  <slot />
  {#if $showAlpha}
    <aside
      class="variant-filled fixed top-[70px] left-0 w-full z-50 flex flex-row justify-items-end items-center"
    >
      <!-- Message -->
      <div class="alert-message px-4">
        <h3 class="h3">LLaMP is now in alpha 🚀</h3>
      </div>
      <button
        class="btn inline"
        style="margin-top: 0"
        on:click={() => {
          showAlpha.set(false);
        }}>X</button
      >
    </aside>
  {/if}
</AppShell>
