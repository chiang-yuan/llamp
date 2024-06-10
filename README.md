<h1 align="center">
    <b>LLaMP 🦙🔮</b>
    <br>
    <a href="https://arxiv.org/abs/2401.17244">
      <img src="https://img.shields.io/badge/cs.CL-2401.17244-b31b1b?logo=arxiv&logoColor=white" alt="arXiv">
    </a>
    <a href="http://ingress.llamp.development.svc.spin.nersc.org/about">
      <img src="https://img.shields.io/badge/web-demo-magenta?style=flat&link=http%3A%2F%2Fingress.llamp.development.svc.spin.nersc.org%2Fabout" alt="Website">
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
> TL;DR: LLaMP is a multimodal retrieval-augmented generation (RAG) framework of hierarchical ReAct agents that can dynamically and recursively interact with [Materials Project](https://materialsproject.org) to ground LLMs on high-fidelity materials informatics.

This repository accompanies our paper [**LLaMP: Large Language Model Made Powerful for High-fidelity Materials Knowledge Retrieval and Distillation**](https://arxiv.org/abs/2401.17244). Our codebase is built upon [LangChain](https://github.com/langchain-ai/langchain) and is designed to be modular and extensible, and can be used to reproduce the experiments in the paper, as well as to develop new experiments.

LLaMP is also a homonym of **Large Language model [Materials Project](https://materialsproject.org)**. :wink: It empowers LLMs with large-scale computational materials database to reduce the likelihood of hallucination for materials informatics. 

<h4 align="center">
  <img src="https://python.langchain.com/v0.1/img/brand/wordmark-dark.png" height="30">
  <img src="https://raw.githubusercontent.com/sveltejs/branding/master/svelte-horizontal.svg" height="30"/>
  <a href="https://elementari.janosh.dev/"><img src="https://raw.githubusercontent.com/janosh/elementari/main/static/favicon.svg" height="30"/></a>
  <a href="https://www.skeleton.dev/"><img src="https://user-images.githubusercontent.com/1509726/199282306-7454adcb-b765-4618-8438-67655a7dee47.png" height="30"/></a>
</h4>

## 🔮 Quick Start

#### Python API

```shell
git clone https://github.com/chiang-yuan/llamp.git
cd llamp/api
pip install -e .
```

After installation, check out [colab notebook chat](http://colab.research.google.com/github/chiang-yuan/llamp/blob/main/experiments/00-notebook-chat.ipynb) or the notebooks in `experiments` to start. 

#### (Optional) Atomistic Simulation

You may need to install additional packages to support atomistic simulations:

```shell
pip install ase, atomate2, jobflow, mace-torch
```

#### (Optional) Docker Web Interface 

```shell
docker-compose up --build
```

## 👋 Contributing

We understand sometime it is difficult to navigate Materials Project database! We want everyone to be able to access materials informatics through conversational AI. We are looking for contributors to help us build a more powerful and user-friendly LLaMP to support more MP API endpoints or external datastore and agents.

To contirbute to LLaMP, please follow these steps:

1. Fork the repository
2. Set up environment variables
    ```shell
    cp .env.example .env.local
    ```
3. Deploy local development environment 
    ```shell
    docker-compose up
    ```
4. Make changes and submit a pull request

## 🌟 Authors and Citation

<a href="https://github.com/chiang-yuan"><img src="https://avatars.githubusercontent.com/u/41962462?v=4" title="chiang-yuan" width="50" height="50"></a>
<a href="https://github.com/knhn1004"><img src="https://avatars.githubusercontent.com/u/49494541?v=4" title="knhn1004" width="50" height="50"></a>
<a href="https://github.com/Ht2214"><img src="https://avatars.githubusercontent.com/u/78026336?v=4" title="Ht2214" width="50" height="50"></a>
<a href="https://github.com/janosh"><img src="https://avatars.githubusercontent.com/u/30958850?v=4" title="janosh" width="50" height="50"></a>

![Alt](https://repobeats.axiom.co/api/embed/75e53e291a07ad8d4b60e5f800726debe01351fb.svg "Repobeats analytics image")

If you use LLaMP, our code and data in your research, please cite our paper:

```bibtex
@article{chiang2024llamp,
  title={LLaMP: Large Language Model Made Powerful for High-fidelity Materials Knowledge Retrieval and Distillation},
  author={Chiang, Yuan and Chou, Chia-Hong and Riebesell, Janosh},
  journal={arXiv preprint arXiv:2401.17244},
  year={2024}
}
```

## 🤗 Acknowledgements

We thank Matthew McDermott (@mattmcdermott), Jordan Burns in Materials Science and Engineering at UC Berkeley for their valuable feedback and suggestions. We also thank the [Materials Project](https://materialsproject.org) team for their support and for providing the data used in this work. We also thank Dr. Karlo Berket (@kbuma) and Dr. Anubhav Jain (@computron) for their advice and guidance.

