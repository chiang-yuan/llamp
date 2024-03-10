<center>
    <h1 align="center">
        <b>LLaMP 🦙🔮</b>
        <br>
        <a href="https://arxiv.org/abs/2401.17244">
          <img src="https://img.shields.io/badge/cs.CL-2401.17244-b31b1b?logo=arxiv&logoColor=white" alt="arXiv">
        </a>
        <a href="https://github.com/chiang-yuan/llamp/stargazers">
          <img src="https://img.shields.io/github/stars/chiang-yuan/llamp?style=social" alt="Github Stars">
        </a>
    </h1>
    <h4>Large Language Model Made Powerful for High-fidelity Materials Knowledge Retrieval and Distillation</h4>
</center>

> TL;DR: LLaMP is a multimodal retrieval-augmented generation (RAG) framework of hiearchical ReAct agents that can dynamically and recursively interact with Materials Project to ground LLMs on high-fidelity materials informatics.

We are sorry! LLaMP is actually a homonym of **Large Language model [Materials Project](https://materialsproject.org)**. :wink: It empowers LLMs with scientific knowledge and reduces the likelihood of hallucination for materials data distillation.

<!-- LLaMP is a web-based assistant that allows you to explore and interact with materials data in a conversational and intuitive manner. It integrates the power of the Materials Project API and the intelligence of OpenAI's GPT-3.5 to offer a comprehensive and user-friendly solution for discovering and understanding computational materials data based on quantum mechanical calculations. -->


<!-- <img src="https://raw.githubusercontent.com/sveltejs/branding/master/svelte-horizontal.svg" height="30"/>
<a href="https://elementari.janosh.dev/"><img src="https://raw.githubusercontent.com/janosh/elementari/main/static/favicon.svg" height="30"/></a> -->

## :crystal_ball: Introduction

Reducing hallucination of Large Language Models (LLMs) is imperative for use in the sciences where reproducibility is crucial. However, LLMs inherently lack long-term memory, making it a nontrivial, ad hoc, and inevitably biased task to fine-tune them on domain-specific literature and data. Here we introduce LLaMP, a multimodal retrieval-augmented generation (RAG) framework of multiple data-aware reasoning-and-acting (ReAct) agents that dynamically interact with computational and experimental data on Materials Project (MP). Without fine-tuning, LLaMP demonstrates an ability to comprehend and integrate various modalities of materials science concepts, fetch relevant data stores on the fly, process higher-order data (such as crystal structures and elastic tensors), and summarize multi-step procedures for solid-state synthesis. The proposed framework offers an intuitive and nearly hallucination free approach to exploring materials informatics and establishes a pathway for knowledge distillation and fine-tuning other language models.

<!-- **:mag_right: Key Features of LLaMP**

1. **Natural Language Interaction:** Say goodbye to complex queries and technical jargon. LLaMP understands human language, allowing you to communicate your materials-related questions in a conversational and intuitive manner.

2. **Expertly Curated Data:** By harnessing the capabilities of the Materials Project API, LLaMP provides access to a vast repository of materials data, including composition, properties, structures, and more.

3. **Intelligent Responses:** Powered by OpenAI's GPT-3.5, LLaMP not only retrieves data but also delivers insightful and informative responses in plain language, making complex materials concepts easy to comprehend.

4. **Effortless Exploration:** Whether you're seeking materials with specific properties, analyzing trends, or comparing compositions, LLaMP streamlines the exploration process, ensuring you find the information you need quickly.

5. **Custom Functionality:** LLaMP's innovative design enables you to leverage predefined functions tailored to materials research. These functions allow you to retrieve, filter, and analyze materials data in a structured and efficient manner.

6. **Personalized Experience:** LLaMP adapts to your preferences, learning from each interaction to provide increasingly accurate and relevant responses over time.

7. **Seamless Integration:** As a web-based assistant, LLaMP is accessible from anywhere, eliminating the need for complicated installations or setups.

Whether you're a researcher, engineer, student, or anyone with a curiosity about materials, LLaMP is your indispensable companion on the journey of material exploration. It transforms the way we access and engage with materials data, making the pursuit of scientific knowledge more accessible and enjoyable than ever before.

Experience the future of materials exploration with LLaMP – your intelligent guide to the world of materials science and discovery. -->

## :hammer_and_wrench: Installation

### Build the app locally

```shell
docker-compose up --build
```

## 🤝 Contributing

### Environment Variables for development

```
cp .env.example .env.local
```

### Spinning up Development Environment

Please set the env vars using the above instructions before running

```
docker-compose up
```

## 📑 Documentation

This project is structured into various directories, each serving a specific purpose in the application's architecture.

### Frontend

The frontend of this application is built using SvelteKit and is contained within the `web/` directory. Detailed documentation regarding the frontend architecture, file structure, and development guidelines can be found in the [frontend README](web/README.md).

<!-- [📖 Read the frontend documentation](web/README.md) -->

## :rocket: Usage