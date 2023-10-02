<script lang="ts">
	import { Avatar } from '@skeletonlabs/skeleton';
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

<div class="grid grid-cols-[auto_1fr] gap-2">
<Avatar width="w-12" initials="MP"/>
<div class="card p-4 variant-soft rounded-tl-none space-y-2">
	<header class="flex justify-between items-center">
		<p class="font-bold">{bubble.name}</p>
		<small class="opacity-50">{bubble.timestamp}</small>
	</header>
	<p>{bubble.message}</p>
</div>
</div>

