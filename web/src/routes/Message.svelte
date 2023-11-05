<script lang="ts">
  import type { ChatMessage } from '$lib/chatUtils';
  import { Avatar } from '@skeletonlabs/skeleton';
  import { Structure, StructureCard } from 'elementari';
  import Carousel from 'svelte-carousel';
  export let data: ChatMessage;

  $: user = data.role === 'user';

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
  console.log('data: ', data)
</script>

{#if data.type == 'msg' && data.content.length > 0}

  <div class="flex gap-2 {user ? 'justify-end' : ''}">
    <div>
      <Avatar 
        width="w-14" initials={user ? '🦖' : '🔮'} class={user ? 'order-2' : 'order-1'} 
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
      <pre class="whitespace-pre-wrap">{data.content}</pre>
    </div>
  </div>
{:else if data.type == 'structures'}

  <div class="flex gap-2 {user ? 'justify-end' : ''}">
    <div>
      <Avatar 
        width="w-14" initials={user ? '🦖' : '🔮'} class={user ? 'order-2' : 'order-1'} 
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
	  <div class="max-w-5xl">
		<div class="snap-x scroll-px-4 snap-mandatory scroll-smooth flex gap-4 overflow-x-auto px-4 py-10">
			{#each data?.structures as stc }
			<div>
				<Structure structure={stc} --struct-height="500px" --struct-width="500px" camera_position={{x: 3,y:3, z:3}}/>
				<StructureCard structure={stc} />
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
        width="w-14" initials={user ? '🦖' : '🔮'} class={user ? 'order-2' : 'order-1'} 
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
      <pre class="whitespace-pre-wrap">{data.content}</pre>
		<Carousel
			autoplay
			duration={500}
			autoplayProgressVisible
			arrows={false}
			swiping={false}
			particlesToShow={1}
		>
		{#each data?.structures as stc }
		<div>
			<Structure structure={stc} --struct-height="500px" --struct-width="500px" camera_position={{x: 3,y:3, z:3}}/>
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
        width="w-14" initials={user ? '🦖' : '🔮'} class={user ? 'order-2' : 'order-1'} 
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
      <pre class="whitespace-pre-wrap">{data.content}</pre>
		<path
        stroke="none"
        fill-opacity="0"
        class="voronoi-cell"
        d={data.similation_data}
		></path>
	  </div>
    </div>
  </div>
{/if}
