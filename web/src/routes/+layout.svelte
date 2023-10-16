<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';

	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
</script>

<svelte:head>
	<title>LLaMP</title>
</svelte:head>

<!-- App Shell -->
<AppShell class="flex flex-col h-screen">
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<span class="lg:inline hidden"><strong class="text-xl">LLaMP 🦙🔮 - Large-Language model for Materials Project</strong></span>
				<span class="lg:hidden"><strong class="text-xl">LLaMP</strong></span>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<!-- <a
					class="btn btn-sm variant-ghost-surface"
					href="#"
					target="_blank"
					rel="noreferrer"
				>
					Discord
				</a> -->
				<!-- <a
					class="btn btn-sm variant-ghost-surface"
					href="#"
					target="_blank"
					rel="noreferrer"
				>
					Twitter
				</a> -->
				<a
					class="btn btn-sm variant-ghost-surface"
					href="https://materialsproject.org"
					target="_blank"
					rel="noreferrer"
				>
					Materials Project
				</a>
				<a
					class="btn btn-sm variant-ghost-surface"
					href="https://github.com/chiang-yuan/llamp"
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
