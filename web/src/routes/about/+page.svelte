<script lang="ts">
  import IntegrationsCarousel from './IntegrationsCarousel.svelte';

  import ychiang from '$lib/images/ychiang.jpg';
  import ccchou from '$lib/images/ccchou.jpg';
  import janosh from '$lib/images/janosh.jpg';
  import elvis from '$lib/images/elvis.jpg';
  import { CodeBlock } from '@skeletonlabs/skeleton';

  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faEnvelope } from '@fortawesome/free-solid-svg-icons';
  import { faGithub } from '@fortawesome/free-brands-svg-icons';
  import { onMount } from 'svelte';

  let loading = true;
  onMount(() => {
    loading = false;
  });

  import Message from '../../lib/components/Message.svelte';
  import { type Chat, type ChatMessage, syncChats, type SimulationDataItem } from '$lib/chatUtils';
  
  let exMsgA1: ChatMessage = {
    role: 'user',
    content: 'What is the bandgap of of stable MgSe?',
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgA2: ChatMessage = {
    role: 'assistant',
    content: 'The bandgap of stable MgSe is approximately 2.5765 eV',
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgB1: ChatMessage = {
    role: 'user',
    content: 'Give me one structure of barium titanate',
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgB2: ChatMessage = {
    role: 'assistant',
    content: 'The function is readily available on LLaMP. Please try it out in the app and refer to the slides for demo while we are working on this block.',
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgE1: ChatMessage = {
    role: 'user',
    content: "What's the elastic tensor of NaCl?",
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgE2: ChatMessage = {
    role: 'assistant',
    content: "The elastic tensor of NaCl is as follows: \n - Voigt bulk modulus (k_voigt): 22.59 GPa \n - Reuss bulk modulus (k_reuss): 22.59 GPa \n - Voigt-Reuss-Hill bulk modulus (k_vrh): 22.59 GPa \n - Voigt shear modulus (g_voigt): 14.51 GPa \n - Reuss shear modulus (g_reuss): 14.04 GPa \n - Voigt-Reuss-Hill shear modulus (g_vrh): 14.27 GPa \n - Universal anisotropy: 0.17 \n - Homogeneous Poisson ratio: 0.24 \n\n The elastic tensor components are as follows: \n ``` \n [[46.0, 11.0, 11.0, 0.0, 0.0, 0.0], \n [11.0, 46.0, 11.0, 0.0, 0.0, 0.0], \n [11.0, 11.0, 46.0, 0.0, 0.0, 0.0], \n [0.0, 0.0, 0.0, 12.0, 0.0, 0.0], \n [0.0, 0.0, 0.0, 0.0, 12.0, 0.0], \n [0.0, 0.0, 0.0, 0.0, 0.0, 12.0]] \n ``` \n ...",
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgT1: ChatMessage = {
    role: 'user',
    content: "What's the formation energy of GaAs?",
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgT2: ChatMessage = {
    role: 'assistant',
    content: "The formation energy of GaAs varies among different thermodynamic calculations. Here are some of the formation energy values for GaAs from different thermodynamic endpoints: \n 1. Formation Energy: -0.302 eV/atom \n 2. Formation Energy: -0.018 eV/atom \n 3. Formation Energy: -0.446 eV/atom \n 4. Formation Energy: 0.182 eV/atom \n 5. Formation Energy: -0.094 eV/atom \n 6. Formation Energy: -0.036 eV/atom \n 7. Formation Energy: -0.098 eV/atom \n 8. Formation Energy: -0.002 eV/atom \n 9. Formation Energy: 0.014 eV/atom \n \n Please note that these values are obtained from different thermodynamic calculations and may vary slightly.",
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgS1: ChatMessage = {
    role: 'user',
    content: "Give me five example synthesis recipes for synthesizing PbZr0.52Ti0.48O3",
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgS2: ChatMessage = {
    role: 'assistant',
    content: "[error] This model's maximum context length is 16385 tokens. However, your messages resulted in 19201 tokens (8912 in the messages, 10289 in the functions). Please reduce the length of the messages or functions.. Please try again.",
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgS3: ChatMessage = {
    role: 'user',
    content: "Give me two example synthesis recipes for synthesizing PbZr0.52Ti0.48O3 then",
    type: 'msg',
    timestamp: new Date(),
  };
  let exMsgS4: ChatMessage = {
    role: 'assistant',
    content: "Here are two example synthesis recipes for synthesizing PbZr0.52Ti0.48O3:\n 1. Synthesis Recipe 1:\n    - Source: [DOI: 10.1016/j.matlet.2011.04.088](https://doi.org/10.1016/j.matlet.2011.04.088)\n    - Synthesis Type: Solid-state\n    - Reaction: PbO + 0.48 TiO2 + 0.52 ZrO2 → Pb(Zr0.52Ti0.48)O3\n    - Precursors: PbO, TiO2, ZrO2\n    - Operations: Starting synthesis, Mixing, Milling, Drying, Heating, Annealing\n\n 2. Synthesis Recipe 2:\n    - Source: [DOI: 10.1016/j.ceramint.2011.04.098](https://doi.org/10.1016/j.ceramint.2011.04.098)\n    - Synthesis Type: Solid-state\n    - Reaction: PbO + 0.48 TiO2 + 0.52 ZrO2 → Pb(Zr0.52Ti0.48)O3\n    - Precursors: ZrO2, TiO2, PbO\n    - Operations: Mixing, Mixing, Milling, Stirring, Drying, Calcination, Calcination, Starting synthesis, Fabrication, Curing\n\n Please note that these synthesis recipes are provided as examples from the available literature. The specific conditions and parameters may vary depending on the desired outcome and experimental setup.",    
    type: 'msg',
    timestamp: new Date(),
  };
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
      <p class="h4 mb-8">
        Large Language model Made Powerful for High-fidelity Materials Science Knowledge Retrieval
        and Distillation
      </p>
    </div>

    <section class="mb-12">
      <!-- <h3 class="h3 font-bold mb-4">Meet Our Team</h3> -->
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
          <a href="https://www.linkedin.com/in/elvis-hsieh/" target="_blank" class="text-blue-500">
            <img src={elvis} alt="Elvis Hsieh" class="mx-auto w-32 h-32 rounded-full mb-2" />
            <p class="font-semibold text-xl">Elvis Hsieh</p>
            <p class="text-gray-500 text-md">UC Berkeley</p>
          </a>
          <a href="https://github.com/Ht2214" target="_blank" class="text-purple-600">
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
      <h3 class="h3 font-bold mb-4">Abstract</h3>
      <p>
        Reducing hallucination of Large Language Models (LLMs) should be the top priority of any attempt to make LLMs useful and reliable for scientific applications. However, LLMs suffer from the lack of long-term memory and it is nontrivial and inevitably biased to fine-tune LLMs against pre-selected literature or documents. Here we present LLaMP, a <i>retrieval augmented generation</i> (RAG) framework to build a data-aware agent that interacts with computational and experimental data on Materials Project (<a href="https://materialsproject.org" class="text-blue-500">https://materialsproject.org</a>). Without any fine-tuning, the agent can understand complex materials science concepts,
        fetch relevant data stores on-the-fly, process higher-order data (such as crystal structures and dielectric tensors), and summarize multi-step procedures for solid-state synthesis. We envision that the framework lays the foundation for a future autonomous laboratory where multiple LLM agents communicate and cooperate in synergy with robotics to drive materials synthesis without hard-coded human logic and intervention.
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
      <h3 class="h3 font-bold mb-4">Preprint</h3>
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
      <h3 class="h3 font-bold mb-4">Demo Conversations</h3>
      <blockquote class="h4 blockquote" style="margin: 1rem;">
        Bandstructure information (semicondutor/device applications)
      </blockquote>
      <div class="card variant-ghost-tertiary">
        <section
          class="overflow-y-auto flex-grow p-4 space-y-4"
        >
          <!-- {#each $chats[$currentChatIndex].messages as msg, index (msg)} -->
            <Message data={exMsgA1} />
            <Message data={exMsgA2} />
          <!-- {/each} -->
        </section>
      </div>
      <blockquote class="h4 blockquote" style="margin: 1rem;">
        Crystal structure summary and visualization by <a href="https://elementari.janosh.dev/" target="_blank" class="text-blue-500">Elementari</a>
      </blockquote>
      <div class="card variant-ghost-warning">
        <section
          class="overflow-y-auto flex-grow p-4 space-y-4"
        >
          <Message data={exMsgB1} />
          <Message data={exMsgB2} />
        </section>
      </div>
      <blockquote class="h4 blockquote" style="margin: 1rem;">
        Synthesis recipes (experiment copilot, autonomous laboratory applications)
      </blockquote>
      <div class="card variant-ghost-tertiary">
        <section
          class="overflow-y-auto flex-grow p-4 space-y-4"
        >
          <Message data={exMsgS1} />
          <Message data={exMsgS2} />
          <Message data={exMsgS3} />
          <Message data={exMsgS4} />
        </section>
      </div>
      <blockquote class="h4 blockquote" style="margin: 1rem;">
        Higher-order data retrieval such as elastic tensor (mechanics applications)
      </blockquote>
      <div class="card variant-ghost-warning">
        <section
          class="overflow-y-auto flex-grow p-4 space-y-4"
        >
          <!-- {#each $chats[$currentChatIndex].messages as msg, index (msg)} -->
            <Message data={exMsgE1} />
            <Message data={exMsgE2} />
          <!-- {/each} -->
        </section>
      </div>
    </section>

    <section class="mb-12">
      <h3 class="h3 font-bold mb-4">Integrations</h3>
      {#if loading === false}
      <IntegrationsCarousel />
      {/if}
    </section>


    <section class="mb-12 flex flex-wrap md:flex-nowrap">
      <div class="w-full md:w-1/2 p-4">
        <h3 class="h3 font-bold mb-4">Citation</h3>
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
        <h3 class="h3 font-bold mb-4">Acknowledgements</h3>
        <p>We thank Matthew McDermott, Jordan Burns for early test and input, and Karlo Berket for helpful discussion.</p>
      </div>
    </section>

    <footer class="text-center mt-8">© 2023 LLaMP. All Rights Reserved.</footer>
  </div>
{/if}
