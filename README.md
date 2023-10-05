# LLaMP - Large Language model Made Powerful :llama::crystal_ball:

### **Introducing LLaMP: Large Language model Made Powerful** :rocket:

We are sorry! LLaMP is actually a homonym of **Large Language model [Materials Project](https://materialsproject.org)**. :wink: It empowers LLMs with scientific knowledge and reduces the likelihood of hallucination for materials data distillation.

LLaMP is a web-based assistant that allows you to explore and interact with materials data in a conversational and intuitive manner. It integrates the power of the Materials Project API and the intelligence of OpenAI's GPT-3.5 to offer a comprehensive and user-friendly solution for discovering and understanding computational materials data based on quantum mechanical calculations.

Click [here](https://docs.google.com/presentation/d/e/2PACX-1vR1LjNO2gp_jVUkIX4qxdkAC0Q9PJ4c2vOvNY2HP6-HjlZCOAdiciw8yTpgZvpw9-a9tF7qT8oC6ntV/pub?start=false&loop=false&delayms=3000) for introduction slides.

<img src="https://raw.githubusercontent.com/sveltejs/branding/master/svelte-horizontal.svg" height="30"/>
<a href="https://elementari.janosh.dev/"><img src="https://raw.githubusercontent.com/janosh/elementari/main/static/favicon.svg" height="30"/></a>

## :crystal_ball: Introduction

Discovering and understanding materials is a cornerstone of innovation across various industries, from electronics and energy to healthcare and beyond. However, navigating the vast landscape of materials data and scientific information can be a challenging task. That's where LLaMP steps in – a groundbreaking smart agent designed to revolutionize the way we explore and interact with materials information.

LLaMP seamlessly integrates the power of the Materials Project API and the intelligence of OpenAI's GPT-3.5 to offer a comprehensive and intuitive solution for exploring, querying, and understanding materials data. Whether you're a seasoned materials scientist or an enthusiast curious about the properties of different materials, LLaMP empowers you with a dynamic and user-friendly platform to uncover valuable insights and answers.

**:mag_right: Key Features of LLaMP**

1. **Natural Language Interaction:** Say goodbye to complex queries and technical jargon. LLaMP understands human language, allowing you to communicate your materials-related questions in a conversational and intuitive manner.

2. **Expertly Curated Data:** By harnessing the capabilities of the Materials Project API, LLaMP provides access to a vast repository of materials data, including composition, properties, structures, and more.

3. **Intelligent Responses:** Powered by OpenAI's GPT-3.5, LLaMP not only retrieves data but also delivers insightful and informative responses in plain language, making complex materials concepts easy to comprehend.

4. **Effortless Exploration:** Whether you're seeking materials with specific properties, analyzing trends, or comparing compositions, LLaMP streamlines the exploration process, ensuring you find the information you need quickly.

5. **Custom Functionality:** LLaMP's innovative design enables you to leverage predefined functions tailored to materials research. These functions allow you to retrieve, filter, and analyze materials data in a structured and efficient manner.

6. **Personalized Experience:** LLaMP adapts to your preferences, learning from each interaction to provide increasingly accurate and relevant responses over time.

7. **Seamless Integration:** As a web-based assistant, LLaMP is accessible from anywhere, eliminating the need for complicated installations or setups.

Whether you're a researcher, engineer, student, or anyone with a curiosity about materials, LLaMP is your indispensable companion on the journey of material exploration. It transforms the way we access and engage with materials data, making the pursuit of scientific knowledge more accessible and enjoyable than ever before.

Experience the future of materials exploration with LLaMP – your intelligent guide to the world of materials science and discovery.

## :hammer_and_wrench: Installation

## :rocket: Usage

## Resources

### [Materials Project](https://materialsproject.org/)

- [Materials Project API Doc](https://docs.materialsproject.org/)
- [Materials Porject API Specs](https://api.materialsproject.org/docs)
- [OpenAPI JSON](https://api.materialsproject.org/openapi.json)
- [MP API usage examples](https://docs.materialsproject.org/downloading-data/using-the-api/examples)
- [MP API github](https://github.com/materialsproject/api)

### Langchain

https://python.langchain.com/docs/modules/chains/additional/openapi

- https://python.langchain.com/docs/integrations/retrievers/arxiv
- https://python.langchain.com/docs/integrations/toolkits/openapi

### OpenAI

- [Function calling via ChatGPT API](https://www.youtube.com/watch?v=0-zlUy7VUjg&ab_channel=GregKamradt%28DataIndy%29)

### Streamlit

- [Text summerization with langchain openai and create a
  streamlit app](https://alphasec.io/summarize-text-with-langchain-and-openai/)
- [Twitter bot for arxiv summarization](https://levelup.gitconnected.com/build-a-twitter-bot-for-arxiv-paper-summarization-by-openai-and-langchain-in-10-minutes-e57de6b32e03)
- [Langchaing: Build a Text Summarization app](https://blog.streamlit.io/langchain-tutorial-3-build-a-text-summarization-app/)

### CyrstalToolkit, Dash, Plotly

- [Dash ChatGPT App Challenge](https://community.plotly.com/t/dash-chatgpt-app-challenge/75763/26)

### Environment Variables for development

```
cp .env.example .env.local
```

### Spinning up Development Environment

Please set the env vars using the above instructions before running

```
docker-compose up
```
