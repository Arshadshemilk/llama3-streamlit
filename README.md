
# 🦙 Llama-3.1 Chatbot 🤖 Powered by Groq Hosted on Streamlit

In this tutorial, we will build and deploy a personalized AI-powered chat application using Streamlit, leveraging the latest AI model, `llama-3.1-8b-instant`, with Groq for faster inference. Plus, we will show you how to **deploy it for free!** This guide will take you through the code step-by-step, explaining each section and providing useful tips for customization.

## Getting Started

To begin, sign in to [Groq](https://groq.com/) and click on `Start Building`.

Once logged in, create your API key by clicking on `Create API Key`. Ensure to copy this key and store it securely, as you will need it for your application.

### Install Necessary Libraries

Next, you need to create a `requirements.txt` file with the following contents:

```txt
groq==0.9.0
streamlit==1.37.0
python-dotenv
```

Install these dependencies using the following command:

```bash
pip install -r requirements.txt
```

### Create the Main Application File

Now, create a file named `main.py` and import the required libraries:

```python
import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq
```

Here, Streamlit will be used to build the chat interface, dotenv will help manage environment variables, and Groq will facilitate fast inference from the AI model.

## Configuring the Page

Set up the page configuration for your Streamlit application as follows:

```python
st.set_page_config(
    page_title="The Tech Buddy",
    page_icon="",
    layout="centered",
)
```

This configuration will enhance the professional look and feel of your chat application.

## Handling Environment Variables

We will use environment variables to store sensitive information, such as API keys and application-specific prompts. Create a `.env` file in your root folder with the following content:

```env
GROQ_API_KEY='YOUR_GROQ_API_KEY'

INITIAL_RESPONSE="Enter what you want to show as the first response of your bot, example: Hello! my friend I am a painter from the 70's. What's up?"

CHAT_CONTEXT="Enter how do you want to personalize your chatbot, example: You are a painter from the 70's and you respond with sentences containing painting references. (This is for the system)"

INITIAL_MSG="Enter the first message from the assistant to initiate the chat history, example: Hey there! I know everything about painting, ask me anything. (This is for the assistant)"
```

This setup is essential for personalizing your application. Feel free to modify these values to suit your needs.

Next, configure these environment variables in your Python file:

```python
try:
    secrets = dotenv_values(".env")  # for development environment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # for Streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# Save the API key to an environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]
```

In the `try block`, we fetch the environment variables from the `.env` file for local testing. When deploying with Streamlit, we won’t have access to the `.env` file; hence, we will store our secrets using `st.secrets`, which returns a Python dictionary similar to `dotenv_values(".env")`.

## Initializing the Chat Application

Next, let’s set up the chat history and initialize the AI model:

1. Copy your preferred AI model's `Model ID` from the Groq console: [Groq Supported Models](https://console.groq.com/docs/models).

2. Initialize your model:

```python
# Initialize the chat history if it is not already present in the Streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]

client = Groq()
```

We will store the chat history in the `st.session_state` object, which allows us to persist data across session refreshes.

## Displaying the Chat Application

Let’s create the chat interface using Streamlit:

```python
# Page title
st.title("Hey Buddy!")
st.caption("Let's go back in time...")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar=''):
        st.markdown(message["content"])
```

The `st.chat_message` function will be used to display each message in the chat history.

## User Input Field

Next, we will create a text input field for user interaction:

```python
user_prompt = st.chat_input("Let's chat!")
```

When the user submits their prompt, we will append it to the chat history and generate a response from the AI model.

## Generating a Response from the AI Model

Now, let's generate a response from the AI model using the Groq library:

```python
def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

if user_prompt:
    with st.chat_message("user", avatar=""):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        stream=True  # for streaming the response
    )
    response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})
```

We use the `client.chat.completions.create()` method to generate a stream and then parse it to get the actual response from the AI model. This response is then appended to the chat history.

## Running the Application Locally

Congratulations! You’ve successfully built a personalized AI-powered chat application using Streamlit, Groq, and the `llama-3.1-8b-instant` model.

Here is the complete code for your `main.py` file:

```python
import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq


def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


# Streamlit page configuration
st.set_page_config(
    page_title="The 70's Painter",
    page_icon="🎨",
    layout="centered",
)


try:
    secrets = dotenv_values(".env")  # for development environment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # for Streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# Save the API key to an environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]


client = Groq()

# Initialize the chat history if present in the Streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]

# Page title
st.title("Hey Buddy!")
st.caption("Let's go back in time...")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar='🤖'):
        st.markdown(message["content"])


# User input field
user_prompt = st.chat_input("Ask me")

if user_prompt:
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # Get a response from the AI model
    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='🤖'):
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            stream=True  # for streaming the response
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})

```

To run your application locally, enter the following command in your terminal:

```bash
streamlit run main.py
```

## Deployment

You are now ready to deploy your application! First, upload your codebase to a [GitHub](https://github.com/) repository. Then, sign in to your Streamlit account and navigate to the `My Apps` section:

1. Click on `Create App` at

 the upper right corner.
2. Select the first option to connect to your GitHub repository.
3. Locate your GitHub repository and select the appropriate repository.
4. Locate your `main.py` file.
5. (Optional) Create a custom URL for your deployed app.
6. Click on `Additional Settings` and paste everything from your `.env` file (these will be your `st.secrets`).
7. Finally, click on `Deploy`.

Congratulations! You have successfully deployed your personalized AI chat application for free.

--- 

Feel free to use this formatted text directly on your GitHub page!
