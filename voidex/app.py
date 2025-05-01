from typing import Literal
from atomic_agents.agents.base_agent import (
    BaseAgent,
    BaseAgentInputSchema,
    BaseAgentConfig,
)
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator
import instructor
import openai
import streamlit as st


from voidex.paths import STREAMLIT_CSS_PATH


def create_chat_agent() -> BaseAgent:
    return BaseAgent(
        BaseAgentConfig(
            client=instructor.from_openai(openai.OpenAI()),
            model="gpt-4o-mini",
            system_prompt_generator=SystemPromptGenerator(
                background=[
                    "You are an assistant to the Voidex, a document loader and vector database.",
                    "The Voidex takes in search queries and performs semantic search on the documents it contains.",
                    "Your role is to facilitate providing search queries to the Voidex based on the user's input.",
                    "The primary language will be English.",
                ]
            ),
            max_tokens=1024,
        )
    )


def apply_custom_css():

    with open(STREAMLIT_CSS_PATH) as file:
        st.markdown(
            f"<style>\n{file.read()}\n</style>",
            unsafe_allow_html=True,
        )

    # Add custom fonts
    st.markdown(
        """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Lato:wght@400;700&display=swap" rel="stylesheet">
    """,
        unsafe_allow_html=True,
    )


def setup_page_config():
    st.set_page_config(
        page_title="VOIDEX",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )


# Initialize the session state to store conversation history
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "librarian" not in st.session_state:
        st.session_state.librarian = create_chat_agent()

    if "documents" not in st.session_state:
        st.session_state.documents = []


def display_chat_message(role: Literal["user", "assistant"], content: str):
    with st.chat_message(role):
        st.markdown(content)


def display_chat_history():
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])


def process_user_input(user_input: str):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    display_chat_message("user", user_input)

    # Show a spinner while getting the response
    with st.spinner("Librarian is searching the void..."):
        # Get librarian response
        librarian_response = get_librarian_response(user_input)

    # Add librarian response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": librarian_response}
    )

    # Display librarian response
    display_chat_message("assistant", librarian_response)


def get_librarian_response(user_input: str) -> str:
    # Here you would implement the actual call to your vector database
    # For now, we're just forwarding the input to the agent
    librarian_output = st.session_state.librarian.run(
        BaseAgentInputSchema(chat_message=user_input)
    )
    st.session_state.librarian.memory.add_message("assistant", librarian_output)
    return librarian_output.chat_message


def clear_chat_history():
    st.session_state.messages = []
    st.session_state.librarian = create_chat_agent()


def add_document():
    file_path = st.session_state.file_path_input
    if file_path and file_path.strip():
        # In a real implementation, you would validate the path and process the file
        st.session_state.documents.append(file_path)
        st.session_state.file_path_input = ""
        st.success(f"Document added: {file_path}")


def remove_document(doc_idx):
    if 0 <= doc_idx < len(st.session_state.documents):
        removed = st.session_state.documents.pop(doc_idx)
        st.success(f"Removed: {removed}")


def run_chat_interface():

    # Webpage setup
    setup_page_config()

    # Apply Voidex CSS
    apply_custom_css()

    st.markdown(
        "<h1 class='main-header'>Voidex</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<p class='sub-header'>Peer into the void and beckon for it's secrets</p>",
        unsafe_allow_html=True,
    )

    # Initialize session state
    initialize_session_state()

    # Display chat history
    display_chat_history()

    # Chat input
    user_input = st.chat_input(
        "What knowledge do you seek from the Voidex?",
        key="chat_input",
    )

    if user_input:
        process_user_input(user_input)

    # Create sidebar for document management
    with st.sidebar:
        st.markdown(
            "<h3>Document Management</h3>",
            unsafe_allow_html=True,
        )

        # File management section
        with st.container(border=True):
            st.text_input("Enter file path:", key="file_path_input")
            st.button("Add Document", on_click=add_document, use_container_width=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h4>Current Documents</h4>", unsafe_allow_html=True)

            if "documents" not in st.session_state:
                st.info("No documents loaded")
            else:
                for i, doc in enumerate(st.session_state.documents):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.text(f"{i + 1}. {doc}")
                    with col2:
                        if st.button("🗑️", key=f"remove_{i}"):
                            remove_document(i)

        # Settings and info
        with st.container(border=True):
            st.markdown("<h4>Settings</h4>", unsafe_allow_html=True)
            st.button(
                "Clear Chat History",
                on_click=clear_chat_history,
                use_container_width=True,
            )

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(
                """
            <div style='font-size: 0.8rem; color: #a9a9a9;'>
            Voidex provides semantic search across your document collection.
            </div>
            """,
                unsafe_allow_html=True,
            )
