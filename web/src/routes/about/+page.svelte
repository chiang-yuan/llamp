<script lang="ts">
  import Carousel from 'svelte-carousel';
  import avatar from '$lib/images/avatar.jpeg';
  import ychiang from '$lib/images/ychiang.jpg';
  import ccchou from '$lib/images/ccchou.jpg';
  import janosh from '$lib/images/janosh.jpg';
  import mp from '$lib/images/mp.png';
  import ucb from '$lib/images/ucberkeley.png';
  import op from '$lib/images/openai-white-lockup.svg';
  import lc from '$lib/images/langchain.png';
  import ar from '$lib/images/arxiv-logo.svg';
  import { CodeBlock } from '@skeletonlabs/skeleton';

  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faLink, faEnvelope, faBars } from '@fortawesome/free-solid-svg-icons';
  import { faGithub } from '@fortawesome/free-brands-svg-icons';
  import AppShell from '@skeletonlabs/skeleton';
</script>

<svelte:head>
  <title>About LLaMP</title>
</svelte:head>

<div class="container mx-auto px-4 py-12">
  <div class="text-center">
    <h1 class="text-4xl font-bold mb-4">
      <a href="/about">LLaMP</a>
    </h1>
    <p class="h3 mb-8">
      Large Language model Made Powerful for High-fidelity Materials Science Knowledge Retrieval and Distillation 
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
          <FontAwesomeIcon icon={faGithub}/>
        </a>
        <a href="mailto:cyrusyc@berkeley.edu" class="text-purple-600">
          <FontAwesomeIcon icon={faEnvelope}/>
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
          <FontAwesomeIcon icon={faGithub}/>
        </a>
      </div>
      <div class="text-center">
        <a href="https://janosh.dev" class="text-blue-500">
          <img src={janosh} alt="Janosh Riebesell" target="_blank" class="mx-auto w-32 h-32 rounded-full mb-2"/>
          <p class="font-semibold text-xl">Janosh Riebesell</p>
          <p class="text-gray-500 text-md">Cambridge University</p>
          <p class="text-gray-500 text-md">Lawrence Berkeley National Laboratory</p>
        </a>
        <a href="https://github.com/janosh" target="_blank" class="text-purple-600">
          <FontAwesomeIcon icon={faGithub}/>
        </a>
      </div>
    </div>
  </section>

  <section class="mb-12">
    <h2 class="text-2xl font-bold mb-4">Abstract</h2>
    <p>
      Reducing hallucination of Large Language Models (LLMs) should be the top priority of any attempt to make LLMs useful and reliable for scientific applications. However, it is nontrivial and inevitably biased to fine-tune LLMs against pre-selected literature or documents. Here we present LLaMP, a <i>retrieval augmented generation</i> (RAG) framework to build a data-aware agent that interacts with computational and experimental data on Materials Project (<a href="https://materialsproject.org" class="text-blue-500">https://materialsproject.org</a>). Without any fine-tuning, the agent can understand complex materials science concepts, fetch relevant data stores on-the-fly, process higher-order data (such as crystal structures and dielectric tensors), and summarize multi-step procedures for solid-state synthesis. We envision that the framework lays the foundation for a future autonomous laboratory where multiple LLM agents communicate and cooperate in synergy with robotics to drive materials synthesis without hard-encoded human logic and intervention.
    </p>
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
    <Carousel autoplay duration={1000} arrows={false} swiping={false} particlesToShow={4}>
      <div class="p-2">
        <a href="https://materialsproject.org" target="_blank" rel="noreferrer">
          <div class="rounded shadow">
            <img src={mp} alt="Materials Project" class="w-full h-48 my-auto rounded mb-4" />
            <!-- <h3 class="text-xl font-bold">Materials Project</h3>
            <p>Description</p> -->
          </div>
        </a>
      </div>
      <div class="p-2">
        <a href="https://openai.com/" target="_blank" rel="noreferrer">
          <div class="rounded shadow">
            <img src={op} alt="Open AI" class="w-full h-48 my-auto rounded mb-4" />
          </div>
        </a>
      </div>
      <div class="p-2">
        <a href="https://langchain.com" target="_blank" rel="noreferrer">
          <div class="rounded shadow">
            <img src={lc} alt="Langchain" class="w-full h-48 my-auto rounded mb-4" />
            <!-- <h3 class="text-xl font-bold">Materials Project</h3>
            <p>Description</p> -->
          </div>
        </a>
      </div>
      <div class="p-2">
        <a href="https://arxiv.org" target="_blank" rel="noreferrer">
          <div class="rounded shadow">
            <img src={ar} alt="ArXiv" class="w-full h-48 my-auto rounded mb-4" />
          </div>
        </a>
      </div>
    </Carousel>

    <!-- Repeat for other groups -->
  </section>
  <section class="mb-12 flex flex-wrap md:flex-nowrap">
    <div class="w-full md:w-1/2 p-4">
      <h2 class="text-2xl font-bold mb-4">Citation</h2>
      <CodeBlock
        code={`
{
	@article{author2023,
	title={Title of Article},
	author={Author Name},
	journal={Journal Name},
	year={2023}
}
		`}
      />
    </div>
    <div class="md:w-1/2 p-4">
      <h2 class="text-2xl font-bold mb-4">Acknowledgements</h2>
      <p>
        
      </p>
    </div>
  </section>

  <footer class="text-center mt-8">© 2023 LLaMP. All Rights Reserved.</footer>
</div>
