from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
import streamlit as st
import requests
import time
import json
import os 

# Get the model service endpoint
model_service = os.getenv("MODEL_ENDPOINT", "http://localhost:57364")
model_service = f"{model_service}/v1"
model_service_bearer = os.getenv("MODEL_ENDPOINT_BEARER")

# Add authorization headers if needed
request_kwargs = {}
if model_service_bearer is not None:
    request_kwargs = {"headers": {"Authorization": f"Bearer {model_service_bearer}"}}

@st.cache_resource(show_spinner=False)
def checking_model_service():
    """Check if the model service is available."""
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    server = None

    while not ready:
        try:
            request_cpp = requests.get(f"{model_service}/models", **request_kwargs)
            if request_cpp.status_code == 200:
                server = "Llamacpp_Python"
                ready = True
        except Exception as e:
            print(f"Error checking model service: {e}")
        time.sleep(1)

    print(f"{server} Model Service Available in {time.time() - start} seconds")
    return server 

# Check model service availability
with st.spinner("Checking Model Service Availability..."):
    server = checking_model_service()

# Streamlit UI
st.title("💬 T3chFest Chatbot")  

# Initialize session states
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you in your T3chFest session?"}]
if "input_disabled" not in st.session_state:
    st.session_state["input_disabled"] = False

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

@st.cache_resource()
def memory():
    """Create a conversation buffer memory."""
    return ConversationBufferWindowMemory(return_messages=True, k=3)

# Get model name from environment variables
model_name = os.getenv("MODEL_NAME", "") 

# Initialize LLM
llm = ChatOpenAI(
    base_url=model_service, 
    api_key="sk-no-key-required" if model_service_bearer is None else model_service_bearer,
    model=model_name,
    streaming=True,
    callbacks=[StreamlitCallbackHandler(st.empty(),
                                        expand_new_thoughts=True,
                                        collapse_completed_thoughts=True)]
)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world-class technical advisor. Do NOT output GPT4 Correct User, only provide technical advice."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

# Create LLM chain
chain = LLMChain(
    llm=llm, 
    prompt=prompt,
    verbose=False,
    memory=memory()
)

# Handle user input
user_input = st.chat_input(disabled=st.session_state["input_disabled"])
if user_input:
    st.session_state["input_disabled"] = True  # Disable input while processing
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Generate response
    response = chain.invoke(user_input)
    st.chat_message("assistant").markdown(response["text"])    
    st.session_state.messages.append({"role": "assistant", "content": response["text"]})

    st.session_state["input_disabled"] = False  # Re-enable input
    st.rerun()
