import os
import streamlit as st
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

def initialize_chatbot(groq_api_key: str, langsmith_api_key: str):
    os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "StreamlitLanggraph"

    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

    class State(TypedDict):
        messages: Annotated[list, add_messages]

    graph_builder = StateGraph(State)

    def chatbot(state: State):
        return {"messages": llm.invoke(state['messages'])}

    graph_builder.add_node("chatbot", chatbot)

    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    return graph_builder.compile()

def main():
    st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖")
   
    st.title("🤖 LangGraph Groq Chat Assistant")
   
    st.sidebar.header("🔑 API Credentials")
   
    groq_api_key = st.sidebar.text_input(
        "Groq API Key",
        type="password",
        help="You can get your Groq API key from the Groq platform"
    )
   
    langsmith_api_key = st.sidebar.text_input(
        "LangSmith API Key",
        type="password",
        help="You can get your LangSmith API key from the LangSmith platform"
    )
   
    if "messages" not in st.session_state:
        st.session_state.messages = []
   
    if groq_api_key and langsmith_api_key:
        try:
            graph = initialize_chatbot(groq_api_key, langsmith_api_key)
           
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
           
            if prompt := st.chat_input("What would you like to chat about?"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt
                })
               
                with st.chat_message("user"):
                    st.markdown(prompt)
               
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                   
                    for event in graph.stream({'messages': ("user", prompt)}):
                        for value in event.values():
                            full_response += value["messages"].content
                            message_placeholder.markdown(full_response + "▌")
                   
                    message_placeholder.markdown(full_response)
               
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })
       
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Please check your API keys and try again.")
    else:
        st.info("Please enter your Groq and LangSmith API keys in the sidebar.")

if __name__ == "__main__":
    main()