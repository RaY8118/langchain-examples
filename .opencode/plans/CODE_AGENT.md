# Code Helper Agent - Implementation Plan

## Goal
Build an agentic code helper that can explore, search, and explain code from local repositories.

---

## 1. Project Structure

```
langchain/
├── PLAN.md                      # This file
├── requirements.txt
├── main.py                      # Entry point
├── src/
│   ├── __init__.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── code_agent.py        # Agent setup & tools
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── explore.py        # Explore repo structure
│   │       ├── read_file.py     # Read file contents
│   │       ├── search.py         # Search code patterns
│   │       └── explain.py        # Explain code using LLM
│   └── loaders/
│       ├── __init__.py
│       └── python_loader.py     # Python code loader
├── test_repo/                   # Sample repo for testing
│   ├── app.py
│   ├── utils.py
│   └── models/
│       └── user.py
```

---

## 2. Tools Definition

### Tool 1: explore_repo
- **Purpose**: Get directory structure of a repository
- **Input**: Root directory path (string)
- **Output**: Tree structure showing files/folders
- **Use case**: Agent decides which files to examine

### Tool 2: read_file
- **Purpose**: Read contents of a specific file
- **Input**: File path (string)
- **Output**: File content (first 500 lines if too large)
- **Use case**: Agent reads key files based on user question

### Tool 3: search_code
- **Purpose**: Find code patterns (functions, classes, imports)
- **Input**: Search query (e.g., "function login", "class User")
- **Output**: List of matching files with line numbers and context
- **Use case**: Agent finds relevant code across repo

### Tool 4: explain_code
- **Purpose**: Explain what a file or function does
- **Input**: File path + specific question
- **Output**: Human-readable explanation
- **Use case**: Final answer to user's question

---

## 3. Agent Architecture

### Framework: Tool Calling Agent
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
```
- Simple, well-documented
- Modern LangChain approach
- Good for hackathon demos

### LLM Choice
- Primary: Ollama (llama3.2:1b or codellama)
- Fallback: OpenRouter (gpt-oss-120b:free)

---

## 4. Implementation Steps

### Phase 1: Foundation
- [ ] Create project structure (src/, agent/, tools/, loaders/)
- [ ] Create requirements.txt
- [ ] Create test_repo with sample Python files

### Phase 2: Tools Implementation
- [ ] explore_repo - directory tree
- [ ] read_file - file reading with truncation
- [ ] search_code - pattern matching
- [ ] explain_code - LLM-based explanation

### Phase 3: Agent Integration
- [ ] Set up Ollama LLM
- [ ] Create agent with tools
- [ ] Wire AgentExecutor
- [ ] Test end-to-end

### Phase 4: Refinement
- [ ] Error handling
- [ ] Handle large files
- [ ] Test with sample questions

---

## 5. Sample Conversation Flow

```
User: "How does authentication work in this repo?"

Agent: "I'll explore the repo structure to find auth-related files"
→ explore_repo("./test_repo")
→ Sees: app.py, utils.py, models/user.py

Agent: "Let me search for auth patterns"
→ search_code("auth login")
→ Finds: utils.py (login function), models/user.py (User class)

Agent: "I'll read the relevant files"
→ read_file("utils.py")
→ read_file("models/user.py")

Agent: "Now I can explain how authentication works"
→ explain_code with context
→ Returns: "The authentication uses JWT tokens..."
```

---

## 6. Decisions Made

- **Max file size**: Read first 500 lines or 10KB (whichever comes first)
- **Languages**: Python only initially
- **LLM**: Ollama with llama3.2:1b (local, free)
- **Search**: Recursive by default

---

## 7. Future Expansions (Post-Hackathon)

- GitHub repo cloning tool
- JavaScript/TypeScript support
- Multi-file comparison
- Code suggestion/improvement
- Memory of previous queries

---

## 8. Dependencies

```
langchain>=0.3
langchain-core
langchain-community
langchain-ollama
langchain-text-splitters
```
