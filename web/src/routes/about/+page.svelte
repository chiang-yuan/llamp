<script lang="ts">
  import IntegrationsCarousel from './IntegrationsCarousel.svelte';

  import ychiang from '$lib/images/ychiang.jpg';
  import ccchou from '$lib/images/ccchou.jpg';
  import janosh from '$lib/images/janosh.jpg';
  import { CodeBlock } from '@skeletonlabs/skeleton';

  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faEnvelope } from '@fortawesome/free-solid-svg-icons';
  import { faGithub } from '@fortawesome/free-brands-svg-icons';
  import { onMount } from 'svelte';

  let loading = true;
  onMount(() => {
    loading = false;
  });
</script>

<svelte:head>
  <title>About LLaMP</title>
</svelte:head>
{#if loading}
  Loading...
{:else}
  <div class="container mx-auto px-8 lg:px-10 py-12 max-w-6xl">
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">
        <a href="/about">LLaMP</a>
      </h1>
      <p class="h3 mb-8">
        Large Language model Made Powerful for High-fidelity Materials Science Knowledge Retrieval
        and Distillation
      </p>
    </div>

    <section class="mb-12">
      <!-- <h2 class="text-2xl font-bold mb-4">Meet Our Team</h2> -->
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div class="text-center">
          <a href="https://chiang-yuan.github.io" target="_blank" class="text-blue-500">
            <img src={ychiang} alt="Yuan Chiang" class="mx-auto w-32 h-32 rounded-full mb-2" />
            <p class="font-semibold text-xl">Yuan Chiang</p>
            <p class="text-gray-500 text-md">UC Berkeley</p>
            <p class="text-gray-500 text-md">Lawrence Berkeley National Laboratory</p>
          </a>
          <a href="https://github.com/chiang-yuan" target="_blank" class="text-purple-600">
            <FontAwesomeIcon icon={faGithub} />
          </a>
          <a href="mailto:cyrusyc@berkeley.edu" class="text-purple-600">
            <FontAwesomeIcon icon={faEnvelope} />
          </a>
        </div>
        <!-- Repeat for other members -->
        <div class="text-center">
          <a href="https://github.com/knhn1004" target="_blank" class="text-blue-500">
            <img src={ccchou} alt="Chia Hong Chou" class="mx-auto w-32 h-32 rounded-full mb-2" />
            <p class="font-semibold text-xl">Chia-Hong Chou</p>
            <p class="text-gray-500 text-md">Foothill College</p>
          </a>
          <a href="https://github.com/knhn1004" target="_blank" class="text-purple-600">
            <FontAwesomeIcon icon={faGithub} />
          </a>
        </div>
        <div class="text-center">
          <a href="https://janosh.dev" class="text-blue-500">
            <img
              src={janosh}
              alt="Janosh Riebesell"
              target="_blank"
              class="mx-auto w-32 h-32 rounded-full mb-2"
            />
            <p class="font-semibold text-xl">Janosh Riebesell</p>
            <p class="text-gray-500 text-md">Cambridge University</p>
            <p class="text-gray-500 text-md">Lawrence Berkeley National Laboratory</p>
          </a>
          <a href="https://github.com/janosh" target="_blank" class="text-purple-600">
            <FontAwesomeIcon icon={faGithub} />
          </a>
        </div>
      </div>
    </section>

    <section class="mb-12">
      <h2 class="text-2xl font-bold mb-4">Abstract</h2>
      <p>
        Reducing hallucination of Large Language Models (LLMs) should be the top priority of any
        attempt to make LLMs useful and reliable for scientific applications. However, it is
        nontrivial and inevitably biased to fine-tune LLMs against pre-selected literature or
        documents. Here we present LLaMP, a <i>retrieval augmented generation</i> (RAG) framework to
        build a data-aware agent that interacts with computational and experimental data on
        Materials Project (<a href="https://materialsproject.org" class="text-blue-500"
          >https://materialsproject.org</a
        >). Without any fine-tuning, the agent can understand complex materials science concepts,
        fetch relevant data stores on-the-fly, process higher-order data (such as crystal structures
        and dielectric tensors), and summarize multi-step procedures for solid-state synthesis. We
        envision that the framework lays the foundation for a future autonomous laboratory where
        multiple LLM agents communicate and cooperate in synergy with robotics to drive materials
        synthesis without hard-encoded human logic and intervention.
      </p>
    </section>

    <section class="mb-12 flex justify-center items-center">
      <iframe 
          title="LLaMP Introduction"
          class="w-full lg:w-3/4 aspect-video mx-auto my-auto"
          src="https://docs.google.com/presentation/d/e/2PACX-1vR1LjNO2gp_jVUkIX4qxdkAC0Q9PJ4c2vOvNY2HP6-HjlZCOAdiciw8yTpgZvpw9-a9tF7qT8oC6ntV/embed?start=false&loop=true&delayms=3000" 
          frameborder="0" 
          allowfullscreen="true" 
          mozallowfullscreen="true" 
          webkitallowfullscreen="true">
      </iframe>
    </section>

    <section class="mb-12">
      <h2 class="text-2xl font-bold mb-4">Preprint</h2>
      <ul class="space-y-4">
        <li class="border p-4 rounded shadow">
          <h3 class="text-xl font-bold">Coming soon</h3>
          <!-- <p>Abstract of Paper 1.</p> -->
          <!-- <a href="#" class="text-blue-500">Read More</a> -->
        </li>
        <!-- Repeat for other papers -->
      </ul>
    </section>

    <section class="mb-12">
      <h2 class="text-2xl font-bold mb-4">Integrations</h2>
	  {#if loading === false}
	  
		<IntegrationsCarousel />
		{/if}
	  

      <!-- Repeat for other groups -->
    </section>
    <section class="mb-12 flex flex-wrap md:flex-nowrap">
      <div class="w-full md:w-1/2 p-4">
        <h2 class="text-2xl font-bold mb-4">Citation</h2>
        <CodeBlock
          code={`
@software{llamp2023,
  author={Yuan Chiang, Chia-Hong Chou, Janosh Riebesell},
  title={LLaMP: Large Language model for Materials Project},
  url={http://ingress.llamp.development.svc.spin.nersc.org/},
  version={0.1.0},
  date={2023-11-06},
}
		`}
        />
      </div>
      <div class="md:w-1/2 p-4">
        <h2 class="text-2xl font-bold mb-4">Acknowledgements</h2>
        <p />
      </div>
    </section>

    <footer class="text-center mt-8">© 2023 LLaMP. All Rights Reserved.</footer>
  </div>
{/if}
