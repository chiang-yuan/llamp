<script lang="ts">
  import type { ChatMessage } from '$lib/chatUtils';
  import { Avatar } from '@skeletonlabs/skeleton';
  import { Structure, StructureCard } from 'elementari';
  import Carousel from 'svelte-carousel';
  import * as marked from 'marked';
  import DOMPurify from 'dompurify';
  export let data: ChatMessage;

  function processMathJax(node) {
    MathJax.typesetPromise([node]).catch((err) =>
      console.error('MathJax typeset promise failed:', err)
    );
  }

  $: user = data.role === 'user';
  let w: number;

  interface MessageFeed {
    id: number;
    host: boolean;
    avatar: number;
    name: string;
    timestamp: string;
    message: string;
    color: string;
  }

  const bubble: MessageFeed = {
    id: 1,
    host: true,
    avatar: 1,
    name: 'LLaMP',
    timestamp: new Date(data.timestamp).toLocaleTimeString(),
    message:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl eget ultricies aliquam, quam libero ultricies nunc, nec aliquet nisl nunc eu nunc. Nulla facil',
    color: 'primary'
  };

  let parsedContent: string;
  $: if (data && data.content) {
    const mpRegex = /mp-\d+/g;
    function processLinks(content: string): string {
      // Process the links first
      content = content.replace(mpRegex, (materialId: string) => {
        const tailwindClasses = 'underline text-blue-600 hover:opacity-75';
        return `<a href="https://next-gen.materialsproject.org/materials/${materialId}"
        class="${tailwindClasses}" target="_blank" rel="noopener noreferrer">${materialId}</a>`;
      });

      // Then replace <pre> tags to include the class
      content = content.replace(/<pre>/g, '<pre class="whitespace-pre-wrap">');

      return content;
    }

    parsedContent = processLinks(DOMPurify.sanitize(marked.parse(data.content)));
  }
</script>

{#if data.type == 'msg' && data.content.length > 0 && !parsedContent.startsWith('<p> log=') && !parsedContent.includes('<pre class="whitespace-pre-wrap"><code class="language-AGENT_ACTION:">')}
  <div class="flex gap-2 {user ? 'justify-end' : ''} text-wrap">
    <div>
      <Avatar
        width="w-14"
        initials={user ? '🦖' : '🔮'}
        class={user ? 'order-2' : 'order-1'}
        background="bg-secondary-600"
        border="border-4 border-surface-300-600-token hover:!border-primary-500"
        cursor="cursor-pointer"
      />
    </div>
    <div class="card p-4 rounded-tl-none space-y-2 {user ? 'order-1' : 'order-2 variant-soft'}">
      <header class="flex justify-between items-center">
        {#if !user}
          <p class="font-bold">{bubble.name}</p>
        {/if}
        <small class="opacity-50">{bubble.timestamp}</small>
      </header>

      <div use:processMathJax>
        {@html parsedContent}
      </div>
    </div>
  </div>
{:else if data.type == 'structures'}
  <div class="flex gap-2 {user ? 'justify-end' : ''}">
    <div>
      <Avatar
        width="w-14"
        initials={user ? '🦖' : '🔮'}
        class={user ? 'order-2' : 'order-1'}
        background="bg-secondary-600"
        border="border-4 border-surface-300-600-token hover:!border-primary-500"
        cursor="cursor-pointer"
      />
    </div>
    <div class="card p-4 rounded-tl-none space-y-2 {user ? 'order-1' : 'order-2 variant-soft'}">
      <header class="flex justify-between items-center">
        {#if !user}
          <p class="font-bold">{bubble.name}</p>
        {/if}
        <small class="opacity-50">{bubble.timestamp}</small>
      </header>
      <div class="max-w-[250px] lg:max-w-5xl">
        <div
          class="snap-x scroll-px-4 snap-mandatory scroll-smooth flex gap-4 overflow-x-auto px-4 py-10"
        >
          {#each data?.structures as stc}
            <div>
              <Structure
                structure={stc}
                --struct-height={w > 768 ? '500px' : '280px'}
                --struct-width={w > 768 ? '500px' : '280px'}
                camera_position={{ x: 3, y: 3, z: 3 }}
                show_image_atoms={false}
                show_bonds={true}
              />
              <div style="max-width: 280px">
                <StructureCard structure={stc} />
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
{:else if data.type == 'simulation'}
  <div class="flex gap-2 {user ? 'justify-end' : ''}">
    <div>
      <Avatar
        width="w-14"
        initials={user ? '🦖' : '🔮'}
        class={user ? 'order-2' : 'order-1'}
        background="bg-secondary-600"
        border="border-4 border-surface-300-600-token hover:!border-primary-500"
        cursor="cursor-pointer"
      />
    </div>
    <div class="card p-4 rounded-tl-none space-y-2 {user ? 'order-1' : 'order-2 variant-soft'}">
      <header class="flex justify-between items-center">
        {#if !user}
          <p class="font-bold">{bubble.name}</p>
        {/if}
        <small class="opacity-50">{bubble.timestamp}</small>
      </header>
      <div class="max-w-lg">
        <pre class="whitespace-pre-wrap" bind:this={parsedContent}>{@html parsedContent}</pre>
        <Carousel
          autoplay
          duration={500}
          autoplayProgressVisible
          arrows={false}
          swiping={false}
          particlesToShow={1}
        >
          {#each data?.structures as stc}
            <div>
              <Structure
                structure={stc}
                --struct-height="500px"
                --struct-width="500px"
                camera_position={{ x: 3, y: 3, z: 3 }}
              />
            </div>
          {/each}
        </Carousel>
      </div>
    </div>
  </div>
{:else if data.type == 'simulation_chart'}
  <div class="flex gap-2 {user ? 'justify-end' : ''}">
    <div>
      <Avatar
        width="w-14"
        initials={user ? '🦖' : '🔮'}
        class={user ? 'order-2' : 'order-1'}
        background="bg-secondary-600"
        border="border-4 border-surface-300-600-token hover:!border-primary-500"
        cursor="cursor-pointer"
      />
    </div>
    <div class="card p-4 rounded-tl-none space-y-2 {user ? 'order-1' : 'order-2 variant-soft'}">
      <header class="flex justify-between items-center">
        {#if !user}
          <p class="font-bold">{bubble.name}</p>
        {/if}
        <small class="opacity-50">{bubble.timestamp}</small>
      </header>
      <div class="max-w-lg">
        <pre class="whitespace-pre-wrap" bind:this={parsedContent}>{@html parsedContent}</pre>
        <path stroke="none" fill-opacity="0" class="voronoi-cell" d={data.similation_data} />
      </div>
    </div>
  </div>
{/if}

<style>
  .math-inline {
    font-style: italic; /* Style your math expressions as needed */
  }
</style>
