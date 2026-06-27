# Gmail RAG Assistant

A retrieval-augmented generation (RAG) system that enables natural language querying of your Gmail inbox. It fetches emails, indexes them using FAISS, and answers questions via a Groq-powered LLM.

## Features

- Authenticates with Gmail using IMAP
- Fetches recent emails based on configurable days and count
- Creates semantic embeddings using Sentence Transformers
- Indexes emails in a FAISS vector store
- Answers natural language questions about your emails
- Uses Groq LLM (Llama 3.3 70B) for generation
- Credentials are not stored or logged
---
## Tech Stack

- Streamlit (frontend)
- FAISS (vector search)
- Sentence Transformers (embeddings)
- Groq API (LLM)
- Python (backend)
---
## Installation

### Clone the repository:

```bash
git clone https://github.com/your-username/gmail-rag-assistant.git
cd gmail-rag-assistant
```

### Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```
### Install dependencies:
```bash
pip install -r requirements.txt
```
### Create a .env file in the root directory:
#### GMAIL_EMAIL=your_email@gmail.com
#### GMAIL_APP_PASSWORD=your_app_password
#### GROQ_API_KEY=your_groq_api_key

### Run the application
```bash
streamlit run app.py
```
---
## Requirements
### streamlit==1.37.1
### sentence-transformers==3.0.1
### torch==2.3.1
### torchvision==0.18.1
### faiss-cpu==1.8.0
### requests==2.32.3
### python-dotenv==1.0.1
---
## Usage
### 1.Enter your Gmail and Groq credentials in the sidebar

### 2.Select number of days and maximum emails to fetch

### 3.Click "Load Emails"

### 4.Ask questions in natural language

### 5.View answers with source attribution
---
## Security
### Credentials are only used during the session

### No data is stored or logged

### Gmail App Password is recommended over regular password


---

## .gitignore

```txt
venv/
.env
__pycache__/
*.pyc
.DS_Store
*.log
