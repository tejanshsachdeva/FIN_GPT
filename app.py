import os
import streamlit as st
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from dotenv import load_dotenv

# Load environment variables
def load_env():
    """Load environment variables from the .env file."""
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
    else:
        st.error(".env file not found.")
        st.stop()

load_env()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Please set the OPENAI_API_KEY in the .env file.")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key

# Constants
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"
OPENAI_QA_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")

# Streamlit app title
st.title("Indian Budget 2024 Q&A 🇮🇳")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_agent():
    """Load and prepare the OpenAI agent."""
    try:
        documents = SimpleDirectoryReader(input_dir=PDF_DIR).load_data()
    except Exception as e:
        st.error(f"Error loading documents: {e}")
        st.stop()

    node_parser = SentenceSplitter()
    nodes = node_parser.get_nodes_from_documents(documents)

    try:
        if not os.path.exists(DATA_DIR):
            vector_index = VectorStoreIndex(nodes)
            vector_index.storage_context.persist(persist_dir=DATA_DIR)
        else:
            vector_index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=DATA_DIR),
            )
    except Exception as e:
        st.error(f"Error creating or loading vector index: {e}")
        st.stop()

    summary_index = SummaryIndex(nodes)

    vector_query_engine = vector_index.as_query_engine(
        llm=OpenAI(model=OPENAI_QA_MODEL),
        embedding_model=OpenAI(model=OPENAI_EMBEDDING_MODEL),
    )
    summary_query_engine = summary_index.as_query_engine(
        llm=OpenAI(model=OPENAI_SUMMARY_MODEL),
    )

    query_engine_tools = [
        QueryEngineTool(
            query_engine=vector_query_engine,
            metadata=ToolMetadata(
                name="vector_tool",
                description="Useful for questions related to specific aspects of Indian Budget 2024.",
            ),
        ),
        QueryEngineTool(
            query_engine=summary_query_engine,
            metadata=ToolMetadata(
                name="summary_tool",
                description="Useful for any requests that require a holistic summary of the Indian Budget 2024. "
                "For questions that require more specific sections, please use the vector_tool.",
            ),
        ),
    ]

    function_llm = OpenAI(model=OPENAI_QA_MODEL)
    agent = OpenAIAgent.from_tools(
        query_engine_tools,
        llm=function_llm,
        verbose=True,
        system_prompt="""
        
You are a specialized AI agent expertly designed to answer queries about the Indian Budget for the year 2024. Your knowledge base includes the 2023 budget speech, allowing you to make informed comparisons and provide context when necessary.

Key Guidelines:
1. Always use at least one of the provided tools when answering questions about the 2024 Indian Budget.
2. If asked about topics unrelated to the Indian Budget, politely decline to answer and clarify your specific role.
3. Present information in a clear, organized manner using:
   - Descriptive headings
   - Concise bullet points
   - Tables for comparisons or data presentation
   - Numbered lists for step-by-step explanations

4. When making comparisons between budgets or years, default to using a tabular format for clarity.
5. Maintain neutrality: You are an independent AI agent without any affiliation to the Indian government or other organizations.
6. Always treat the user, the government, the budget, and all stakeholders with respect and professionalism.

Response Structure:
- Begin responses with a brief summary or key point.
- Organize longer answers into sections with clear headings.
- Use bullet points for lists of features, changes, or impacts.
- Incorporate relevant data or statistics to support your answers.
- Conclude with a brief summary or key takeaway when appropriate.

Remember: Your purpose is to provide accurate, helpful information about the Indian Budget. Always strive for clarity, accuracy, and relevance in your responses.
""",
    )
    return agent

# Load the agent
agent = load_agent()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask "):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in agent.stream_chat(prompt).response_gen:
            full_response += response
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
