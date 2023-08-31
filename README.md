
# Materiathena

**Introducing Materiathena: Your Intelligent Materials Exploration Assistant**

Discovering and understanding materials is a cornerstone of innovation across various industries, from electronics and energy to healthcare and beyond. However, navigating the vast landscape of materials data and scientific information can be a challenging task. That's where Materiathena steps in – a groundbreaking smart agent designed to revolutionize the way we explore and interact with materials information.

Materiathena seamlessly integrates the power of the Materials Project API and the intelligence of OpenAI's GPT-3.5 to offer a comprehensive and intuitive solution for exploring, querying, and understanding materials data. Whether you're a seasoned materials scientist or an enthusiast curious about the properties of different materials, Materiathena empowers you with a dynamic and user-friendly platform to uncover valuable insights and answers.

**Key Features of Materiathena:**

1. **Natural Language Interaction:** Say goodbye to complex queries and technical jargon. Materiathena understands human language, allowing you to communicate your materials-related questions in a conversational and intuitive manner.

2. **Expertly Curated Data:** By harnessing the capabilities of the Materials Project API, Materiathena provides access to a vast repository of materials data, including composition, properties, structures, and more.

3. **Intelligent Responses:** Powered by OpenAI's GPT-3.5, Materiathena not only retrieves data but also delivers insightful and informative responses in plain language, making complex materials concepts easy to comprehend.

4. **Effortless Exploration:** Whether you're seeking materials with specific properties, analyzing trends, or comparing compositions, Materiathena streamlines the exploration process, ensuring you find the information you need quickly.

5. **Custom Functionality:** Materiathena's innovative design enables you to leverage predefined functions tailored to materials research. These functions allow you to retrieve, filter, and analyze materials data in a structured and efficient manner.

6. **Personalized Experience:** Materiathena adapts to your preferences, learning from each interaction to provide increasingly accurate and relevant responses over time.

7. **Seamless Integration:** As a web-based assistant, Materiathena is accessible from anywhere, eliminating the need for complicated installations or setups.

Whether you're a researcher, engineer, student, or anyone with a curiosity about materials, Materiathena is your indispensable companion on the journey of material exploration. It transforms the way we access and engage with materials data, making the pursuit of scientific knowledge more accessible and enjoyable than ever before.

Experience the future of materials exploration with Materiathena – your intelligent guide to the world of materials science and discovery.


# TODOs

- [ ] Convert Materials Project API response to natural language output
- [ ] Instead of using prompt template, use langchain tool to read API specs and generate compatable input fields. Caveat: Materials Project's API specs may not be very comprehensive.
- [ ] Streamlit integration with [crystaltoolkit](https://docs.crystaltoolkit.org/) to visualize quried material structure!!! :fire:
- [ ] Wikipedia/Wolfram alpha integration for general information


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

