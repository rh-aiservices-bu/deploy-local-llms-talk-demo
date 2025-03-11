import streamlit as st
import requests
import os

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

def check_api_status():
    """Check if the backend API is up and running."""
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        return "🟢 API Status: Ready" if response.status_code == 200 else "🔴 API Status: Down"
    except Exception:
        return "🔴 API Status: Unreachable"

def get_enabled_tools():
    """Fetch the list of enabled tools from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/tools")
        return response.json().get("tools", []) if response.status_code == 200 else ["Failed to fetch tools"]
    except Exception as e:
        return [f"Error: {e}"]

def get_model_name():
    """Fetch the model name from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/config")
        return response.json().get("model_name", "Unknown Model") if response.status_code == 200 else "Failed to fetch model"
    except Exception as e:
        return f"Error: {e}"

# Initialize session state for logs
if "logs" not in st.session_state:
    st.session_state["logs"] = []

# Streamlit UI
st.set_page_config(page_title="Agentic AI App", page_icon="🤖", layout="wide")
st.title("🤖 Agentic AI App")

# Sidebar
with st.sidebar:
    # API Status
    api_status = check_api_status()
    st.subheader(api_status)

    # Model in Use
    st.subheader("📌 Model in Use")
    st.write(f"**{get_model_name()}**")

    # Enabled Tools
    st.subheader("🔧 Enabled Tools")
    tools = get_enabled_tools()
    for tool in tools:
        st.write(f"✅ {tool}")

    # Logs
    with st.expander("📜 Execution Logs", expanded=False):
        if st.session_state["logs"]:
            for log in st.session_state["logs"]:
                st.write(log)
        else:
            st.write("No logs yet.")

# Chat input and response display
st.subheader("💬 Ask a Question")
user_query = st.text_input("Enter your query:")

if st.button("Ask"):
    if user_query.strip():
        with st.spinner("Processing..."):
            response = requests.post(f"{BACKEND_URL}/ask", json={"query": user_query}).json()
            
            # ✅ Store logs dynamically
            st.session_state["logs"] = response.get("logs", [])

            # Display agent's response in the main UI
            st.write("### 📝 Agentic Response:")
            agent_response = response.get("response", "No response")
            st.write(agent_response)

# Footer
st.markdown("---")
st.caption("Built with ❤️ by the Red Hat AI Business Unit")
