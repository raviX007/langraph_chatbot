# LangGraph Groq Chat Assistant

An interactive chatbot implementation using LangGraph, Groq's Gemma-2-9b-IT model, and Streamlit. The chatbot features a streaming interface and LangSmith integration for conversation monitoring.

## 🌟 Features

- 🔄 Streaming responses using LangGraph
- 🤖 Powered by Groq's Gemma-2-9b-IT model
- 📊 LangSmith integration for monitoring
- 💬 Interactive Streamlit chat interface
- 🔍 Session state management
- 🚀 Real-time response streaming

## 🏗️ Architecture

![alt text](<Screenshot 2025-01-06 at 3.13.07 AM.png>)

## 🛠️ Technical Stack

- **LangGraph**: State management and graph-based conversation flow
- **Groq**: Large Language Model API (Gemma-2-9b-IT)
- **Streamlit**: Web interface and UI components
- **LangSmith**: Conversation monitoring and tracing

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/langgraph-groq-chatbot.git
cd langgraph-groq-chatbot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a requirements.txt with:

```
streamlit
langgraph
langchain-groq
typing-extensions
```

## 🔑 Required API Keys

- **Groq API Key**: For accessing the LLM
- **LangSmith API Key**: For conversation monitoring

## 🚀 Usage

1. Start the application:

```bash
streamlit run app.py
```

2. In the web interface:
   - Enter your API keys in the sidebar
   - Start chatting in the main interface
   - View streaming responses in real-time

## 🔍 Key Components

### StateGraph Implementation

- Manages conversation state
- Handles message flow between components
- Integrates with Groq LLM

### Streamlit Interface

- Real-time chat UI
- Streaming response display
- Session state management
- API key management

### Error Handling

- API validation
- Exception management
- User feedback

## 🏗️ Project Structure

```
langgraph-groq-chatbot/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── README.md          # Documentation
└── .gitignore         # Git ignore file
```

## ⚠️ Limitations

- Requires valid Groq API key
- Requires valid LangSmith API key
- Internet connection needed
- Response time depends on Groq API latency
