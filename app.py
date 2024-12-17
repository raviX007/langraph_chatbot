# -*- coding: utf-8 -*-
"""
Chatbots With LangGraph - Streamlit UI

An interactive chatbot implementation using LangGraph, Groq, and Streamlit.
"""

import os
import streamlit as st
from typing import Annotated
from typing_extensions import TypedDict

# LangGraph and LangChain imports
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

def initialize_chatbot(groq_api_key: str, langsmith_api_key: str):
    """
    Initialize the chatbot with given API keys.
    
    Args:
        groq_api_key (str): API key for Groq
        langsmith_api_key (str): API key for LangSmith
    
    Returns:
        Compiled LangGraph
    """
    # Set up environment variables for LangChain
    os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "StreamlitLanggraph"

    # Initialize the Language Model
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

    # Define the State for the chatbot
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    # Create the graph builder
    graph_builder = StateGraph(State)

    def chatbot(state: State):
        """
        Core chatbot function that processes messages using the LLM.
        
        Args:
            state (State): Current conversation state with messages
        
        Returns:
            dict: Updated state with LLM response
        """
        return {"messages": llm.invoke(state['messages'])}

    # Add the chatbot node to the graph
    graph_builder.add_node("chatbot", chatbot)

    # Define the graph edges
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    # Compile the graph
    return graph_builder.compile()

def main():
    """
    Streamlit application for the LangGraph Chatbot.
    """
    # Set page configuration
    st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖")
    
    # Title
    st.title("🤖 LangGraph Chatbot with Streamlit")
    
    # Sidebar for API Key inputs
    st.sidebar.header("🔑 API Credentials")
    
    # Input for Groq API Key
    groq_api_key = st.sidebar.text_input(
        "Groq API Key", 
        type="password", 
        help="You can get your Groq API key from the Groq platform"
    )
    
    # Input for LangSmith API Key
    langsmith_api_key = st.sidebar.text_input(
        "LangSmith API Key", 
        type="password", 
        help="You can get your LangSmith API key from the LangSmith platform"
    )
    
    # Initialize session state for messages if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Chat interface
    if groq_api_key and langsmith_api_key:
        try:
            # Initialize the chatbot graph
            graph = initialize_chatbot(groq_api_key, langsmith_api_key)
            
            # Display existing messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # User input
            if prompt := st.chat_input("What would you like to chat about?"):
                # Add user message to chat history
                st.session_state.messages.append({
                    "role": "user", 
                    "content": prompt
                })
                
                # Display user message
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Generate response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    # Stream response from LangGraph
                    for event in graph.stream({'messages': ("user", prompt)}):
                        for value in event.values():
                            full_response += value["messages"].content
                            message_placeholder.markdown(full_response + "▌")
                    
                    # Final display of full response
                    message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
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