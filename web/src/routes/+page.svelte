<script lang="ts">

import { Avatar, CodeBlock, ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
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

	// for display purposes only
	interface Question {
		question: string;
		title: string;
		timeElapsedInitials: string;
	};

	const questions: Question[] = [
		{
			question: 'How do I extract BCC Al crystal structure and print pymatgen dictionary?',
			title: 'Extract BCC Al crystal structure and print pymatgen dictionary',
			timeElapsedInitials: '2H',
		},
		{
			question: 'Is YbCl3 magnetic or non-magnetic?',
			title: 'Magnetic properties of YbCl3?',
			timeElapsedInitials: '1H',
		},
		{
			question: 'Can you summarize the properties of the two magnetic substances?',
			title: 'Summary of two magnetic substances',
			timeElapsedInitials: '1.5H',
		},
		{
			question: 'What is the crystal structure of LiFePO4?',
			title: 'Crystal structure of LiFePO4?',
			timeElapsedInitials: '1H',
		},
	];

	let currentQuestion = questions[0].title;


	let currentMessage = '';
</script>




<section class="flex-grow">
	<div class="chat w-full h-full grid grid-cols-1 lg:grid-cols-[30%_1fr]">
		<!-- Navigation -->
		<div class="hidden card lg:grid grid-rows-[auto_1fr_auto] border-r border-surface-500/30">
			<!-- Header -->
			<header class="border-b border-surface-500/30 p-4">
				<input class="input" type="search" placeholder="Search..." />
			</header>
			<!-- List -->
			<div class="p-4 space-y-4 overflow-y-auto">
				<small class="opacity-50">Chat History</small>
				<ListBox active="variant-filled-primary">
					{#each questions as question}
						<ListBoxItem bind:group={currentQuestion} name="questions" value={question.title}>
							<svelte:fragment slot="lead">
								<Avatar width="w-8" initials={question.timeElapsedInitials}/>
							</svelte:fragment>
							{question.title.slice(0, 50) + '...'}
						</ListBoxItem>
					{/each}
				</ListBox>
			</div>
			<!-- Footer -->
			<!-- <footer class="border-t border-surface-500/30 p-4">(footer)</footer> -->
		</div>

		<!-- Chat -->
		<div class="flex flex-col h-full">
			<!-- Conversation -->
			<section class="p-4 overflow-y-auto flex-grow space-y-4">
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
							placeholder="Write a message..."
							rows="1"
						/>
						<button class={currentMessage ? 'variant-filled-primary' : 'input-group-shim'} >
							<i class="fa-solid fa-paper-plane" />
						</button>
					</div>
				</section>
			</div>
		</div>
	</section>
