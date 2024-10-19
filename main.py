import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq


def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


# streamlit page configuration
st.set_page_config(
    page_title="Iron-llama",
    page_icon=".src/loki.png",
    layout="wide",
)

class ModelSelector:
    """Allows the user to select a model from a predefined list."""
    def __init__(self):
        # List of available models to choose from
        self.models = ["llama3-70b-8192","llama3-8b-8192","mixtral-8x7b-32768","gemma-7b-it"]

# Display model selection in a sidebar with a title
    def select(self):
        with st.sidebar:
            st.sidebar.title("Chat with Llama3 + α")
            return st.selectbox("Select a model:", self.models)


try:
    secrets = dotenv_values(".env")  # for dev env
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # for streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# save the api_key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]


client = Groq()

# initialize the chat history if present as streamlit session
if "chat_history" not in st.session_state:
    # print("message not in chat session")
    st.session_state.chat_history = [
        {"role": "assistant",
         "content": INITIAL_RESPONSE
         },
    ]

# page title
st.title("Hi E-ling")
st.caption("Let's go back in to future...")
# the messages in chat_history will be stored as {"role":"user/assistant", "content":"msg}
# display chat history
for message in st.session_state.chat_history:
    # print("message in chat session")
    with st.chat_message("role", avatar='.src/loki.png'):
        st.markdown(message["content"])


# user input field
user_prompt = st.chat_input("Ask me")
model = ModelSelector()
selected_model = model.select()

if user_prompt:
    # st.chat_message("user").markdown
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # get a response from the LLM
    messages = [
        {"role": "system", "content": CHAT_CONTEXT
         },
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='.src/loki.png'):
        stream = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            temperature=0,
            max_tokens=4096,
            stream=True,
            stop=None,
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})
