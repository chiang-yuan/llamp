import os
import re

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    AgentType,
    BaseSingleActionAgent,
    Tool,
    initialize_agent,
    load_tools,
)
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
    ReActSingleInputOutputParser,
)
from langchain.agents.schema import AgentAction
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.document_transformers import (
    LongContextReorder,
)
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings, OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import ArxivQueryRun, StructuredTool, Tool, tool
from langchain.tools.render import (
    format_tool_to_openai_function,
    render_text_description_and_args,
)
from langchain.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain.vectorstores import Chroma

REACT_MULTI_JSON_PROMPT = hub.pull("hwchase17/react-multi-input-json")

load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", None)

class ARXIVAgent:
    """Agent that uses the arXiv API and PDF loader to answer questions about scientific papers and preprints."""

    def __init__(self, llm, hf_api_key=HF_API_KEY, embeddings_model_name="all-MiniLM-L6-v2"):
        self.llm = llm
        # self.summary_chain = load_summarize_chain(self.llm, chain_type="map_reduce", verbose=True)
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=HF_API_KEY,
            model_name=embeddings_model_name
            )
        self.chain = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(
                    x["intermediate_steps"]
                ),
            }
            | self.prompt
            | self.llm.bind(stop=["Observation"])
            # TODO: add a summarizer to take care of large reponses
            # | ReActSingleInputOutputParser()
            | JSONAgentOutputParser()
        )

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def description(self) -> str:
        return self.__doc__

    class PDFLoaderInputSchema(BaseModel):
        url: str = Field(..., description="URL to a PDF file.")
        query: str = Field(..., description="Query to search for in the PDF file.")

    def load_pdf_from_url(self, url: str, query: str):
        loader = PyPDFLoader(url, extract_images=False)
        pages = loader.load_and_split()
        retriever = Chroma.from_documents(pages, embedding=self.embeddings).as_retriever(
            search_kwargs={"k": 10}
        )
        docs = retriever.get_relevant_documents(query)
        # could add StuffDocumentsChain here https://python.langchain.com/docs/modules/data_connection/document_transformers/post_retrieval/long_context_reorder
        return docs
    
    @property
    def tools(self) -> list[Tool]: 
        pdf_tool = StructuredTool.from_function(
            func=self.load_pdf_from_url,
            name="load_pdf_from_url",
            description=re.sub(
                r"\s+", " ",
                """Load a PDF from a URL and return a list of documents relevant 
                to the query. For example, the URL to a paper on arXiv.org has the
                format https://arxiv.org/pdf/{arxiv_id}.pdf, where {arxiv_id} is
                the arXiv identifier of the paper.
                """).replace("\n", " "),
            return_direct=True,
            args_schema=self.PDFLoaderInputSchema,
        )

        return [
            ArxivQueryRun(api_wrapper=ArxivAPIWrapper()),
            pdf_tool
        ]

    @property
    def prompt(self):
        partial_prompt = REACT_MULTI_JSON_PROMPT.partial(
            tools=render_text_description_and_args(self.tools),
            tool_names=", ".join([t.name for t in self.tools]),
        )
        partial_prompt.messages[0].prompt.template = re.sub(
                r"\s+", " ",
                f"""You are a helpful agent called {self.name} having access to 
                papers and preprints on arXiv through arXiv API and PDF loaders. 
                "Preprint" means the paper might not have been peer-reviewed yet. 
                Be critical of the information you find."""
            ).replace("\n", " ") + partial_prompt.messages[0].prompt.template
        return partial_prompt

    def as_executor(
        self,
        verbose=True,
        return_intermediate_steps=False,
        max_iterations=5,
        handle_parsing_errors=True,
        **kwargs,
    ) -> AgentExecutor:
        return AgentExecutor(
            agent=self.chain,
            tools=self.tools,
            verbose=verbose,
            return_intermediate_steps=return_intermediate_steps,
            max_iterations=max_iterations,
            handle_parsing_errors=handle_parsing_errors,
            **kwargs,
        )
    
    class ChainInputSchema(BaseModel):
        input: str = Field(..., description="Complete question to ask the assistatn agent. Should include all the context and details needed to answer the question holistically.")
        # agent_scratchpad: str = ""

    def as_tool(
            self, 
            return_direct=False,
            agent_kwargs={},
            tool_kwargs={},
            ) -> Tool:
        
        def run(input: str):
            return self.as_executor(**agent_kwargs).invoke({
                "input": input,
            })
        
        return StructuredTool.from_function(
            func=run,
            name=self.name,
            description=self.description,
            return_direct=return_direct,
            args_schema=self.ChainInputSchema,
            **tool_kwargs,
        )