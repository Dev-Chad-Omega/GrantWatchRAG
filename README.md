# GrantWatch
GrantWatch is an intelligent Python-based grant monitoring system that has evolved from a simple scraper-notifier bot into an LLM-backed AI agent with Retrieval-Augmented Generation (RAG) capabilities. It continuously downloads, filters, indexes, and intelligently searches grant opportunities using semantic similarity and natural language processing.

---

## Core Features

### Traditional Pipeline
- **Automated Scraping** of grant listings (JSON)  
- **Date Filtering**  
  - Discards entries missing or past their `POSTED_DATE`  
  - Optionally removes "Forecasted" opportunities  
- **Keyword Filtering** via LLM-generated keywords on `FUNDING_DESCRIPTION`  
- **LLM Summarization** of filtered grants into concise descriptions  
- **Sorting** by most-recent `POSTED_DATE`  
- **Gmail Notification** of final results  

### RAG-Enhanced Features
- **Vector Database Integration** using FAISS for semantic search
- **Intelligent Query Processing** with natural language understanding
- **AI Agent Framework** with specialized tools for grant discovery
- **Semantic Search** across grant titles, descriptions, and metadata
- **Automated Workflows** for daily digests and targeted searches
- **Advanced Filtering** by agency, category, funding type, and dates

---

## Installation & Usage

### Prerequisites
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables** in `.env` file:
   ```bash
   WEB_UI_TOKEN=your_llm_token
   LLM_URL=your_llm_endpoint
   ```

3. **Check and edit** your `config.yaml`.

### Traditional Mode
Run the original grant processing pipeline:
```bash
cd src
python main.py
```

### RAG-Enhanced Mode
Run the intelligent RAG-enabled system:

#### Basic Mode (processes grants and runs example queries)
```bash
cd src
python rag_main.py
```

#### Interactive Mode (chat with the AI agent)
```bash
python rag_main.py --interactive
```

#### Single Query Mode
```bash
python rag_main.py --query "Find cybersecurity grants from NSF"
```

#### Workflow Execution
```bash
python rag_main.py --workflow daily_digest
```

### Testing
Run the test suite to verify RAG functionality:
```bash
python test_rag.py
```

### Example RAG Queries
- "Find grants related to artificial intelligence and machine learning"
- "Search for cybersecurity funding opportunities"
- "Show me grants from the National Science Foundation"
- "Summarize grant OPPORTUNITY-ID-123"
- "Find grants closing in the next 30 days"
## 📝 Logging & Debugging

* All pipeline steps log to the console (and optionally to `logs/`).
* On error, the bot exits with a descriptive message.
* Check `logs/` for history of runs and retained percentages.


## Flowchat
![Mermaid Chart_GrantWatch](https://github.com/user-attachments/assets/2cada1ec-d5ce-4e27-b87f-af1f8363abd1)
