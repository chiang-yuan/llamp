<h1 align="center">
    <b>LLaMP 🦙🔮</b>
    <br>
    <a href="https://arxiv.org/abs/2401.17244">
      <img src="https://img.shields.io/badge/cs.CL-2401.17244-b31b1b?logo=arxiv&logoColor=white" alt="arXiv">
    </a>
    <a href="https://github.com/chiang-yuan/llamp/stargazers">
      <img src="https://img.shields.io/github/stars/chiang-yuan/llamp?style=social" alt="Github Stars">
    </a>
    <a href="http://colab.research.google.com/github/chiang-yuan/llamp/blob/main/experiments/00-notebook-chat.ipynb">
      <img src="https://camo.githubusercontent.com/f5e0d0538a9c2972b5d413e0ace04cecd8efd828d133133933dfffec282a4e1b/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667">
    </a>
</h1>
<h4 align="center">Large Language Model Made Powerful for High-fidelity Materials Knowledge Retrieval and Distillation</h4>


> [!TIP]
> TL;DR: LLaMP is a multimodal retrieval-augmented generation (RAG) framework of hiearchical ReAct agents that can dynamically and recursively interact with Materials Project to ground LLMs on high-fidelity materials informatics.

We are sorry! LLaMP is actually a homonym of **Large Language model [Materials Project](https://materialsproject.org)**. :wink: It empowers LLMs with the largest computational materials database [Materials Project](https://materialsproject.org) to reduce the likelihood of hallucination for materials data.

<!-- LLaMP is a web-based assistant that allows you to explore and interact with materials data in a conversational and intuitive manner. It integrates the power of the Materials Project API and the intelligence of OpenAI's GPT-3.5 to offer a comprehensive and user-friendly solution for discovering and understanding computational materials data based on quantum mechanical calculations. -->

<h4 align="center">
  <img src="https://raw.githubusercontent.com/sveltejs/branding/master/svelte-horizontal.svg" height="30"/>
  <a href="https://elementari.janosh.dev/"><img src="https://raw.githubusercontent.com/janosh/elementari/main/static/favicon.svg" height="30"/></a>
</h4>

## Introduction

Reducing hallucination of Large Language Models (LLMs) is imperative for use in the sciences where reproducibility is crucial. However, LLMs inherently lack long-term memory, making it a nontrivial, ad hoc, and inevitably biased task to fine-tune them on domain-specific literature and data. Here we introduce LLaMP, a multimodal retrieval-augmented generation (RAG) framework of multiple data-aware reasoning-and-acting (ReAct) agents that dynamically interact with computational and experimental data on Materials Project (MP). Without fine-tuning, LLaMP demonstrates an ability to comprehend and integrate various modalities of materials science concepts, fetch relevant data stores on the fly, process higher-order data (such as crystal structures and elastic tensors), and summarize multi-step procedures for solid-state synthesis. The proposed framework offers an intuitive and nearly hallucination free approach to exploring materials informatics and establishes a pathway for knowledge distillation and fine-tuning other language models.


## Installation

### Python API

Install from source:
```shell
cd api
pip install .
```

### Build the app locally

```shell
docker-compose up --build
```

## Contributing

### Environment Variables for development

```
cp .env.example .env.local
```

### Spinning up Development Environment

Please set the env vars using the above instructions before running

```
docker-compose up
```
