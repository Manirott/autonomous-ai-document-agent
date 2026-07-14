# 🤖 Autonomous AI Document Generation Agent

An intelligent multi-stage AI agent built with **FastAPI**, **Groq LLM**, and **python-docx** that autonomously plans, reflects, executes, reviews, and generates professional Microsoft Word documents from a simple natural language request.

Instead of directly generating text, the system follows an **Agentic AI workflow** where each stage has a dedicated responsibility, producing higher-quality and more structured documents.

---

## ✨ Features

- ✅ Natural language document requests
- ✅ Autonomous task planning
- ✅ Reflection-based plan validation
- ✅ Step-by-step document generation
- ✅ Automatic document review
- ✅ Microsoft Word (.docx) export
- ✅ REST API built using FastAPI
- ✅ Interactive frontend
- ✅ Execution trace for every stage

---

# 🏗 Architecture

```
                User Request
                     │
                     ▼
           Request Validation
                     │
                     ▼
              Planner Agent
                     │
             Creates Task Plan
                     │
                     ▼
            Reflection Agent
        Reviews & Corrects Plan
                     │
                     ▼
             Executor Agent
      Executes One Task At A Time
                     │
                     ▼
              Review Agent
      Checks Completeness & Quality
                     │
                     ▼
          Word Document Generator
                     │
                     ▼
              Download DOCX
```

---

# ⚙ Tech Stack

### Backend

- FastAPI
- Python 3.10+
- Uvicorn

### AI

- Groq API
- Llama 3.3 70B Versatile

### Document Generation

- python-docx

### Frontend

- HTML
- CSS
- JavaScript

---

# 🧠 Agent Workflow

## 1. Request Validation

Validates the incoming request before any processing begins.

Checks include:

- Empty request
- Invalid input
- Request normalization

---

## 2. Planner Agent

Uses the LLM to understand the user's objective.

Produces:

- Document Type
- Topic
- Audience
- Assumptions
- Ordered execution tasks

Example:

```json
{
  "document_type":"Project Proposal",
  "tasks":[
      {
         "id":1,
         "name":"Analyze user request",
         "tool":"analysis"
      }
  ]
}
```

---

## 3. Reflection Agent

Reviews the Planner output.

Checks for:

- Missing assumptions
- Duplicate tasks
- Incorrect ordering
- Missing business sections
- Reviewer task existence

If necessary, it automatically fixes the execution plan.

---

## 4. Executor Agent

Executes **one task at a time**.

Rather than generating the entire document in one prompt, each task is completed independently.

Example:

```
Task 1
↓

Generate only Executive Summary

↓

Task 2

Generate only Objectives

↓

Task 3

Generate only Timeline
```

This improves consistency and keeps the generated content focused.

---

## 5. Review Agent

After all sections are completed, the Review Agent evaluates the assembled document.

Checks include:

- Completeness
- Logical flow
- Missing sections
- Consistency
- Professional quality

---

## 6. Document Generator

Finally, all generated sections are combined into a professional Microsoft Word document using **python-docx**.

---

# 📁 Project Structure

```
.
├── agent.py
├── app.py
├── prompts.py
├── models.py
├── document_generator.py
├── generated_docs/
├── static/
│   └── index.html
├── requirements.txt
└── README.md
```

---

# 🚀 API Endpoint

### Generate Document

```
POST /agent
```

### Request

```json
{
    "request":"Create a project proposal for an AI Resume Analyzer."
}
```

### Response

```json
{
    "status":"Success",
    "document_type":"Project Proposal",
    "document_path":"generated_docs/ai_resume_analyzer.docx",
    "tasks":[...],
    "execution_trace":[...]
}
```

---

# 💻 Installation

Clone the repository

```bash
git clone https://github.com/Manirott/autonomous-ai-document-agent.git
```

Navigate into the project

```bash
cd autonomous-ai-document-agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key_here
```

Run the server

```bash
uvicorn app:app --reload
```

Open

```
http://127.0.0.1:8000
```

---

# 🎥 Demo Workflow

1. Enter a document request.
2. Planner creates execution tasks.
3. Reflection validates the plan.
4. Executor generates each section.
5. Review Agent checks the document.
6. Download the generated DOCX file.

---

# 📸 Sample Output

### Request

```
Create a Project Proposal for an AI Resume Analyzer.
```

Generated:

- Executive Summary
- Project Objectives
- Technical Approach
- Timeline
- Pricing
- Final Review

↓

Microsoft Word Document (.docx)

---

# 🔮 Future Improvements

- PDF export
- Streaming execution updates
- Multi-user authentication
- Memory-enabled agents
- RAG integration
- Tool calling
- Multi-agent collaboration
- Vector database support
- Web search integration

---

# 👨‍💻 Author

**Manikandan D**

- Python Developer
- FastAPI Developer
- AI & Agentic AI Enthusiast

GitHub: https://github.com/Manirott

---

## ⭐ If you found this project interesting, consider giving it a Star!
