<script lang="ts">
  let w: number;
  import Carousel from 'svelte-carousel';
  import mp from '$lib/images/mp.png';
  import op from '$lib/images/openai-white-lockup.svg';
  import lc from '$lib/images/langchain.png';
  import ar from '$lib/images/arxiv-logo.svg';
  import { writable } from 'svelte/store';
  import { onMount } from 'svelte';

  const imgContainerStyle = `p-2 h-48 flex justify-center items-center`;
  const windowWidth = writable(window.innerWidth);
  function handleResize() {
    windowWidth.set(window.innerWidth);
  }
  $: particlesToShow =
    $windowWidth >= 1024 ? 4 : $windowWidth >= 768 ? 3 : $windowWidth >= 512 ? 2 : 1;
  onMount(() => {
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });
</script>

<Carousel autoplay duration={1000} arrows={false} swiping={false} {particlesToShow}>
  <div class={imgContainerStyle}>
    <a href="https://materialsproject.org" target="_blank" rel="noreferrer">
      <div class="rounded shadow flex flex-col justify-items-center align-middle">
        <img src={mp} alt="Materials Project" class="w-full my-auto rounded" />
        <!-- <h3 class="text-xl font-bold">Materials Project</h3>
            <p>Description</p> -->
      </div>
    </a>
  </div>
  <div class={imgContainerStyle}>
    <a href="https://openai.com/" target="_blank" rel="noreferrer">
      <div class="rounded shadow">
        <img src={op} alt="Open AI" class="w-full h-48 my-auto rounded mb-4" />
      </div>
    </a>
  </div>
  <div class={imgContainerStyle}>
    <a href="https://langchain.com" target="_blank" rel="noreferrer">
      <div class="rounded shadow">
        <img src={lc} alt="Langchain" class="w-full h-48 my-auto rounded mb-4" />
        <!-- <h3 class="text-xl font-bold">Materials Project</h3>
            <p>Description</p> -->
      </div>
    </a>
  </div>
  <div class={imgContainerStyle}>
    <a href="https://arxiv.org" target="_blank" rel="noreferrer">
      <div class="rounded shadow">
        <img src={ar} alt="ArXiv" class="w-full h-48 my-auto rounded mb-4" />
      </div>
    </a>
  </div>
</Carousel>
