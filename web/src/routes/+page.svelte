<script lang="ts">
	import Message from './Message.svelte';

	import { Avatar, CodeBlock, ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

	// for display purposes only
	interface Chat {
		question: string;
		title: string;
		timeElapsedInitials: string;
	};

	const chats: Chat[] = [
		{
			question: 'How do I extract BCC Al crystal structure and print pymatgen dictionary?',
			title: 'Extract BCC Al crystal structure and print pymatgen dictionary',
			timeElapsedInitials: '2H',
		},
		{
			question: 'Is YbCl3 magnetic or non-magnetic?',
			title: 'Magnetic properties of YbCl3?',
			timeElapsedInitials: '8H',
		},
		{
			question: 'Can you summarize the properties of the two magnetic substances?',
			title: 'Summary of two magnetic substances',
			timeElapsedInitials: '1D',
		},
		{
			question: 'What is the crystal structure of LiFePO4?',
			title: 'Crystal structure of LiFePO4?',
			timeElapsedInitials: '2W',
		},
	];


	// TODO: move to lib
	interface ChatMessage {
		role: 'assistant' | 'user';
		content: string;
		type: 'info' | 'msg'; // information (eg. processing) or message
	};

	let messages: ChatMessage[] = []

	let currentChat = chats[0].title;

	let currentMessage = '';
	let processing = false;

	async function askQuestion() {
		if (!currentMessage) return;
		const newMessage: ChatMessage = {
			"role": "user",
			"content": currentMessage,
			"type": "msg",
		}
		messages = [...messages, newMessage];
		const body = messages;
		currentMessage = '';

		try {
		processing = true;
		const response = await fetch('http://localhost:8000/ask', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json',
			},
			body: JSON.stringify(body)
		});

		const result = await response.json();
		console.log(result);
		// Handle the result here - e.g., append the response to your chat, etc.
		} catch (error) {
		console.error("Error while asking question:", error);
		} finally {
			processing = false;
		}
	}
</script>





<div class="chat w-full h-full grid grid-cols-1 lg:grid-cols-[30%_1fr]">
	<!-- Navigation -->
	<div class="hidden card lg:grid grid-rows-[auto_1fr_auto] border-r border-surface-500/30">
		<!-- Header -->
		<header class="border-b border-surface-500/30 p-4">
			<input class="input" type="search" placeholder="Search History" />
		</header>
		<!-- List -->
		<div class="p-4 space-y-4 overflow-y-auto">
			<small class="opacity-50">Chat History</small>
			<ListBox active="variant-filled-primary">
				{#each chats as chat}
					<ListBoxItem bind:group={currentChat} name="questions" value={chat.title}>
						<svelte:fragment slot="lead">
							<Avatar width="w-8" initials={chat.timeElapsedInitials}/>
						</svelte:fragment>
						{chat.title.slice(0, 50) + '...'}
					</ListBoxItem>
				{/each}
			</ListBox>
		</div>
		<!-- Footer -->
		<footer class="border-t border-surface-500/30 p-4 opacity-50">LLaMP Project All Rights Reserved.</footer>
	</div>

<!-- Chat -->
	<div class="flex flex-col h-full">
		<!-- Conversation -->
		<section class="p-4 overflow-y-auto flex-grow space-y-4">
			{#each messages as msg}
				<Message data={msg}/>
			{/each}
		</section>
		<!-- Prompt -->
		<section class="card border-t border-surface-500/30 p-4">
  <div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token">
    <button class="input-group-shim">+</button>
    <textarea
      bind:value={currentMessage}
      class="bg-transparent border-0 ring-0"
      name="prompt"
      id="prompt"
      placeholder="Ask a question..."
      rows="1"
      on:keyup={(e) => { 
		e.preventDefault();
		if (e.key === 'Enter') askQuestion(); 
		}}
    />
    <button
      class={currentMessage ? 'variant-filled-primary' : 'input-group-shim'} 
      on:click={askQuestion}
    >
      <FontAwesomeIcon icon={faPaperPlane} />
    </button>
  </div>
</section>
		
	</div>
</div>