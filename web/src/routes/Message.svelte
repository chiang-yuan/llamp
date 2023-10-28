<script lang="ts">
  import type { ChatMessage } from '$lib/chatUtils';
  import { Avatar } from '@skeletonlabs/skeleton';
  import { Structure, StructureCard } from 'elementari'
  import Carousel from 'svelte-carousel'
  export let data: ChatMessage;
  $: user = data.role === 'user';

  let width,height;

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
    timestamp: '2 hours ago',
    message:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl eget ultricies aliquam, quam libero ultricies nunc, nec aliquet nisl nunc eu nunc. Nulla facil',
    color: 'primary'
  };
</script>

{#if data.content}

  <div class="flex gap-2 {user ? 'justify-end' : ''}">
    <div>
      <Avatar width="w-14" initials={user ? '🦖' : '🔮'} class={user ? 'order-2' : 'order-1'} />
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
      <Avatar width="w-14" initials={user ? '🦖' : '🔮'} class={user ? 'order-2' : 'order-1'} />
    </div>
    <div class="card p-4 rounded-tl-none space-y-2 {user ? 'order-1' : 'order-2 variant-soft'}">
      <header class="flex justify-between items-center">
        {#if !user}
          <p class="font-bold">{bubble.name}</p>
        {/if}
        <small class="opacity-50">{bubble.timestamp}</small>
      </header>
	  <div class="max-w-xl">
		<Carousel
			particlesToShow={3}
			particlesToScroll={3}
			autoplay
			pauseOnFocus
		>
			{#each data?.structures as stc }
			<div>
				<Structure structure={stc} --struct-height="500px" --struct-width="500px" camera_position={{x: 3,y:3, z:3}}/>
				<StructureCard structure={stc} />
			</div>
			{/each}
	  </Carousel>
	  </div>
	  
    </div>
  </div>
{/if}
