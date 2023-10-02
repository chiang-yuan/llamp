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

	let currentMessage = '';
</script>




<section class="card">
	<div class="chat w-full h-full grid grid-cols-1 lg:grid-cols-[30%_1fr]">
		<!-- Navigation -->
		<div class="hidden lg:grid grid-rows-[auto_1fr_auto] border-r border-surface-500/30">
			<!-- Header -->
			<header class="border-b border-surface-500/30 p-4">
				<input class="input" type="search" placeholder="Search..." />
			</header>
			<!-- List -->
			<div class="p-4 space-y-4 overflow-y-auto">
				<small class="opacity-50">Contacts</small>
				<ListBox active="variant-filled-primary">
					<ListBoxItem  group="Person" name="people" value="Person">
						<svelte:fragment slot="lead">
							<Avatar src="https://i.pravatar.cc/?img={14}" width="w-8" />
						</svelte:fragment>
					"Person"
					</ListBoxItem>
				</ListBox>
			</div>
			<!-- Footer -->
			<!-- <footer class="border-t border-surface-500/30 p-4">(footer)</footer> -->
		</div>

		<!-- Chat -->
		<div class="grid grid-row-[1fr_auto]">
			<!-- Conversation -->
			<section class="max-h-[500px] p-4 overflow-y-auto space-y-4">
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
				<section class="border-t border-surface-500/30 p-4">
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


