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
      <img src="https://colab.research.google.com/assets/colab-badge.svg">
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

## Copyright Notice and License

*** Copyright Notice ***

LLaMP Copyright (c) 2025, The Regents of the University of California,
through Lawrence Berkeley National Laboratory (subject to receipt of
any required approvals from the U.S. Dept. of Energy), Haw-Ting Hsieh,
and Yuan Chiang. All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit others to do so.

****************************

*** License Agreement ***

LLaMP Copyright (c) 2025, The Regents of the University of California,
through Lawrence Berkeley National Laboratory (subject to receipt of
any required approvals from the U.S. Dept. of Energy), Haw-Ting Hsieh,
and Yuan Chiang. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

(1) Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

(2) Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

(3) Neither the name of the University of California, Lawrence Berkeley
National Laboratory, U.S. Dept. of Energy, Haw-Ting Hsieh, Yuan Chiang nor the names of the other contributors may be used to endorse or promote products derived from this software without specific prior written permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

You are under no obligation whatsoever to provide any bug fixes, patches,
or upgrades to the features, functionality or performance of the source
code ("Enhancements") to anyone; however, if you choose to make your
Enhancements available either publicly, or directly to Lawrence Berkeley
National Laboratory, without imposing a separate written license agreement
for such Enhancements, then you hereby grant the following license: a
non-exclusive, royalty-free perpetual license to install, use, modify,
prepare derivative works, incorporate into other computer software,
distribute, and sublicense such enhancements or derivative works thereof,
in binary and source code form.
