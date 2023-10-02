<script lang="ts">
	import { Avatar } from '@skeletonlabs/skeleton';
	// TODO: move to lib
	interface ChatMessage {
		role: 'assistant' | 'user';
		content: string;
		type: 'info' | 'msg'; // information (eg. processing) or message
	};
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
	};

	const bubble: MessageFeed= {
		id: 1,
		host: true,
		avatar: 1,
		name: 'LLaMP',
		timestamp: '2 hours ago',
		message: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl eget ultricies aliquam, quam libero ultricies nunc, nec aliquet nisl nunc eu nunc. Nulla facil',
		color: 'primary',
	}


</script>



{#if !data.content}
{:else}
<div class="flex gap-2 {user ? 'justify-end' : ''}">
	<div>
		<Avatar width="w-12" initials={user? "CH" :"MP"} class="{user ? 'order-2' : 'order-1'}"/>
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
{/if}