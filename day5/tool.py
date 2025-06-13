import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun

# 🔑 Hardcoded Gemini API key (⚠️ Not recommended for production)
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyB4IjWrszJ5c50JyBBSSy5CTcgNSvvHQEw"

# 🌐 DuckDuckGo Search Tool
search_tool = DuckDuckGoSearchRun()

# 🤖 Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

# 🧠 LangChain Agent with tools
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search_tool.run,
        description="Useful for answering questions about current events or general knowledge."
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False  # 👇 Disable verbose terminal logs
)

# 🚀 Streamlit UI
st.set_page_config(page_title="🧠 Real-Time Q&A with Gemini", layout="centered")
st.title("🧠 Ask Real-Time Questions with Gemini + DuckDuckGo")

st.markdown("Type your question about current events, news, or general facts. 🗞️🌐")

# 🧾 Input field
user_input = st.text_input("💬 What do you want to know?", placeholder="e.g., What's the latest news about SpaceX?")

# 🕹️ Button to trigger response
if st.button("🔍 Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a question to proceed.")
    else:
        try:
            with st.spinner("Thinking... 🤔"):
                response = agent.run(user_input)
            st.success("✅ Answer:")
            st.markdown(f"> {response}")
        except Exception as e:
            st.error("❌ An error occurred while generating a response.")