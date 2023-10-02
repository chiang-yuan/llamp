<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
</script>

<!-- App Shell -->
<AppShell class="flex flex-col h-screen">
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">LLaMP</strong>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<a
					class="btn btn-sm variant-ghost-surface"
					href="#"
					target="_blank"
					rel="noreferrer"
				>
					Discord
				</a>
				<a
					class="btn btn-sm variant-ghost-surface"
					href="#"
					target="_blank"
					rel="noreferrer"
				>
					Twitter
				</a>
				<a
					class="btn btn-sm variant-ghost-surface"
					href="#"
					target="_blank"
					rel="noreferrer"
				>
					GitHub
				</a>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />
</AppShell>
