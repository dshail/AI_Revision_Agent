# 🤖 AI Revision Agent

[![Tests](https://github.com/dshail/ai-revision-agent/workflows/Tests/badge.svg)](https://github.com/dshail/Ai-Revision-Agent/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

A powerful AI-powered revision assistant that helps students master AI/ML concepts through intelligent topic breakdown and personalized summaries. Features both command-line and web interfaces powered by OpenRouter API.

## 📚 Use Case

Designed to assist learners who are preparing for exams. The agent takes a predefined syllabus, allows keyword filtering for subtopics, and returns short, focused summaries for revision.

---

## 🧠 Features

- ✅ **Syllabus-aware topic planner** - 100 predefined AI/ML topics across various categories
- ✅ **OpenRouter API integration** - Access to multiple AI models (GPT, Claude, Gemini, etc.)
- ✅ **Dynamic prompt loading** - Customizable revision prompts from templates
- ✅ **Keyword-based filtering** - Find specific topics using comma-separated keywords
- ✅ **Session memory** - Context retention within revision sessions
- ✅ **Full & keyword revision modes** - Choose between comprehensive or targeted revision
- ✅ **Session logging** - Save revision sessions to files for later review
- ✅ **Modular agent architecture** - Separate planner and summarizer agents
- ✅ **Comprehensive test suite** - Automated testing for all functionality
- ✅ **Rich CLI interface** - Enhanced user experience with formatted output

---

## 🗂️ Project Structure

```
AI_Revision_Agent/
├── 3_Agent_Code/                    # Core application code
│   ├── planner_agent.py            # Syllabus-aware topic planning
│   ├── summarizer_agent.py         # AI-powered summary generation
│   ├── cli_interface.py            # Command-line interface
│   ├── utils.py                    # Shared utility functions
│   ├── test_runner.py              # Comprehensive test suite
│   ├── syllabus.json               # 57 AI/ML topics across 5 categories
│   ├── prompts/
│   │   └── revision_prompt.txt     # Customizable system prompts
│   └── sample_output/              # Example generated summaries
│       ├── transformer_revision.txt
│       └── agent_ai_revision.txt
├── streamlit_app.py                # Web interface
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── .env                           # API keys (create this file)
```

---

## 🚀 How It Works

1. **Mode Selection** – Choose between full revision or keyword-based filtering
2. **Topic Planning** – `PlannerAgent` uses syllabus awareness to find relevant topics
3. **Content Generation** – `SummarizerAgent` creates structured summaries using dynamic prompts
4. **Session Management** – Maintains context and offers session saving
5. **Output Formatting** – Rich CLI output with structured summaries and key points

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-revision-agent.git
cd ai-revision-agent/3_Agent_Code

2. Install dependencies

pip install -r requirements.txt
Required packages: openai, requests, python-dotenv

3. Add your API key
Create a .env file in the root directory:

ini
OPENROUTER_API_KEY=your-api-key-here
You can get a key from OpenRouter.ai.

## 🧪 Sample Run

```bash
$ python cli_interface.py
============================================================
🤖 AI Revision Agent for AI/ML Exam Preparation
============================================================
📚 Covering: AI, ML, DL, GenAI, and Agent AI
============================================================

🔍 Choose your revision mode:
1. Full revision (all topics)
2. Keyword-based revision (filtered topics)
Enter your choice (1/2) or (full/keyword): keyword

📝 Enter keywords (comma-separated): transformer, attention

🎯 Found 2 topics matching your keywords:
  1. Transformer Architecture
  2. Attention Mechanisms

📝 Generating summaries for 2 topic(s)...
--------------------------------------------------

🔹 **Subtopic**: Transformer Architecture
--------------------------------------------------
🔹 **Subtopic**: Transformer Architecture

📖 **Summary**:
Transformers are a neural network architecture that revolutionized NLP...

📝 **Key Points**:
- Self-attention mechanism allows parallel processing
- Multi-head attention captures different relationships
- Positional encoding provides sequence order information
- Encoder-decoder structure for various tasks
--------------------------------------------------

💾 Save this revision session to file? (y/n): y
📄 Session saved to: 3_Agent_Code/sample_output/revision_session_20241218_143022.txt

✅ Revision session completed! Happy studying! 📚
```

📝 See `sample_output/transformer_revision.txt` for complete examples.

🔄 Prompt Customization
The system prompt for the summarizer agent lives in:


prompts/revision_prompt.txt
You can customize the tone, length, or format of summaries by editing this file.

## 🧪 Testing

Run the comprehensive test suite to validate all functionality:

```bash
cd 3_Agent_Code
python test_runner.py
```

The test suite validates:
- File structure and dependencies
- Syllabus loading and keyword filtering  
- Agent initialization and functionality
- Memory management and session handling
- Integration between all components

## 🧩 Extend the Agent

**Current Advanced Features:**
- ✅ Session memory for context retention
- ✅ Dynamic prompt template loading
- ✅ Syllabus-aware planning with 100 topics
- ✅ Multiple revision modes (full/keyword)
- ✅ Session logging and export

**Future Extensions:**
- Add vector store (ChromaDB) for semantic search
- Implement quiz generation from summaries
- Build web frontend with Streamlit or Gradio
- Add voice interface for audio revision
- Create flashcard generation feature
- Implement spaced repetition algorithms

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Start for Contributors
1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/ai-revision-agent.git`
3. Run setup: `python setup.py`
4. Make your changes
5. Run tests: `python 3_Agent_Code/test_runner.py`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Author

**Shailendra Dhakad**
- GitHub: [@your-dshail](https://github.com/dshail)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/shailendra-dhakad-dshail/)

## ⭐ Support

If you find this project helpful, please give it a star! ⭐

## 📊 Project Stats

- **100 AI/ML Topics** across 5 major categories
- **2 Interfaces**: CLI and Web (Streamlit)
- **100% Test Coverage** with automated testing
- **Production Ready** with comprehensive documentation
