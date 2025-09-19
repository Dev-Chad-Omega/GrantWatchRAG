# GrantWatch RAG Implementation

## Overview

This document describes the implementation of Retrieval-Augmented Generation (RAG) capabilities in GrantWatch, transforming it from a simple scraper-notifier bot into an intelligent AI agent with semantic search and natural language query processing.

## Architecture

### 1. Data Ingestion & Storage Layer

**File**: `src/vector_store/vector_manager.py`

The vector store manager handles:
- **Grant Text Processing**: Combines title, agency, description, category, and funding type into searchable text
- **Embedding Generation**: Uses sentence-transformers (all-MiniLM-L6-v2) to create 384-dimensional embeddings
- **Vector Indexing**: Stores embeddings in FAISS index with cosine similarity search
- **Metadata Storage**: Preserves original grant data alongside vector representations

**Key Features**:
- Automatic text preprocessing and cleaning
- Efficient FAISS indexing with normalized embeddings
- Persistent storage of index and metadata
- Support for filtering by agency, category, and other attributes

### 2. Retrieval Layer

**Integration**: Built into `VectorStoreManager.search_grants()`

The retrieval system provides:
- **Semantic Search**: Natural language queries are embedded and matched against grant vectors
- **Similarity Scoring**: Returns relevance scores for each match
- **Filtering Support**: Apply additional filters (agency, category, date ranges)
- **Top-K Results**: Configurable number of results with similarity thresholds

### 3. Agent Core (LLM + Planner)

**File**: `src/agent/grant_agent.py`

The agent framework includes:

#### Tools Available:
1. **search_grants(query, top_k, filters)**: Semantic search over vector index
2. **summarize_grant(opportunity_id)**: Generate detailed grant summaries using LLM
3. **notify(channel, payload)**: Send notifications via email or other channels

#### Agent Capabilities:
- **Query Processing**: Natural language understanding for user requests
- **Workflow Execution**: Predefined workflows for common tasks
- **Tool Orchestration**: Intelligent selection and chaining of tools

### 4. Main RAG Application

**File**: `src/rag_main.py`

The main application provides:
- **System Initialization**: Coordinates all components
- **Data Pipeline Integration**: Connects with existing grant processing
- **Query Interface**: Handles user interactions
- **Workflow Management**: Executes complex multi-step operations

## Usage

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure environment variables are set:
```bash
# .env file
WEB_UI_TOKEN=your_llm_token
LLM_URL=your_llm_endpoint
```

### Running the System

#### Basic Mode
```bash
cd GrantWatch/src
python rag_main.py
```

#### Interactive Mode
```bash
python rag_main.py --interactive
```

#### Single Query
```bash
python rag_main.py --query "Find cybersecurity grants from NSF"
```

#### Execute Workflow
```bash
python rag_main.py --workflow daily_digest
```

### Example Queries

The system supports natural language queries such as:

- **Search Queries**:
  - "Find cybersecurity grants"
  - "Search for AI and machine learning funding opportunities"
  - "Show grants from NSF closing in the next 30 days"

- **Summary Queries**:
  - "Summarize grant GRANT-2024-001"
  - "Give me details about opportunity OPP-NSF-2024-AI"

- **Workflow Commands**:
  - "workflow: daily_digest"
  - "workflow: targeted_search"
  - "workflow: deadline_alerts"

## Configuration

### RAG Settings in `config.yaml`

```yaml
rag:
  vector_store:
    model_name: "all-MiniLM-L6-v2"
    storage_path: "src/vector_store/data"
    dimension: 384
    similarity_threshold: 0.7
  
  agent:
    max_results: 20
    default_top_k: 10
    enable_workflows: true
    
  search:
    enable_filters: true
    enable_date_filtering: true
    enable_agency_filtering: true
    enable_category_filtering: true
```

## Workflows

### 1. Daily Digest
Automatically searches for recent grants and sends email notifications.

### 2. Targeted Search
Executes specific searches with custom filters and parameters.

### 3. Deadline Alerts
Identifies grants with approaching deadlines (implementation pending).

## Technical Details

### Vector Database (FAISS)

- **Index Type**: IndexFlatIP (Inner Product for cosine similarity)
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Similarity Metric**: Cosine similarity with L2 normalization
- **Storage**: Persistent storage with automatic loading/saving

### LLM Integration

- **Connection**: Uses existing `llm_utils/conn.py` infrastructure
- **Model**: Configurable (default: gemma3:27b)
- **Tasks**: Grant summarization, query understanding, response generation

### Agent Framework

- **Base**: LangChain tools and agents (simplified implementation)
- **Tools**: Custom tools for grant-specific operations
- **Planning**: Rule-based query routing with extensible architecture

## Performance Considerations

### Embedding Generation
- **Batch Processing**: Processes multiple grants simultaneously
- **Caching**: Embeddings are cached to disk for reuse
- **Memory Usage**: Optimized for large grant datasets

### Search Performance
- **FAISS Optimization**: Uses efficient similarity search algorithms
- **Filtering**: Post-search filtering to maintain performance
- **Result Limiting**: Configurable result limits to control response time

## Extension Points

### Adding New Tools
1. Create tool class inheriting from `BaseTool`
2. Implement `_run()` method with tool logic
3. Add to agent's tool list in `GrantAgent.__init__()`

### Custom Workflows
1. Add workflow method to `GrantAgent` class
2. Implement workflow logic using available tools
3. Register in `execute_workflow()` method

### Alternative Vector Stores
1. Implement new vector store class with same interface
2. Update `VectorStoreManager` or create alternative
3. Configure in `config.yaml`

## Monitoring and Debugging

### Logging
- All operations are logged using the existing logging system
- Log levels: info, warning, error, critical
- Logs include performance metrics and error details

### System Statistics
```python
rag_system = RAGGrantWatch()
stats = rag_system.get_system_stats()
print(json.dumps(stats, indent=2))
```

### Interactive Debugging
Use interactive mode for testing and debugging:
```bash
python rag_main.py --interactive
```

## Future Enhancements

### Planned Features
1. **Advanced Date Filtering**: Parse and filter by specific date ranges
2. **Multi-modal Search**: Support for document attachments and images
3. **Conversation Memory**: Maintain context across multiple queries
4. **Advanced Analytics**: Grant trend analysis and recommendations
5. **API Interface**: REST API for external integrations

### Integration Opportunities
1. **Slack Bot**: Direct integration with Slack for team notifications
2. **Web Interface**: Browser-based query interface
3. **Mobile App**: Mobile access to grant search and notifications
4. **Calendar Integration**: Automatic deadline tracking and reminders

## Troubleshooting

### Common Issues

1. **Vector Store Not Found**
   - Run data ingestion first: `rag_system.run_data_ingestion()`
   - Check storage path in configuration

2. **LLM Connection Errors**
   - Verify environment variables (WEB_UI_TOKEN, LLM_URL)
   - Check LLM service availability

3. **Memory Issues**
   - Reduce batch size for embedding generation
   - Limit search results with top_k parameter

4. **Performance Issues**
   - Check FAISS index size and consider optimization
   - Monitor embedding model loading time
   - Verify sufficient system resources

### Debug Commands

```bash
# Check system status
python rag_main.py --query "stats"

# Test vector store
python -c "from vector_store.vector_manager import VectorStoreManager; vm = VectorStoreManager(); print(vm.get_stats())"

# Test agent tools
python -c "from agent.grant_agent import GrantAgent; from vector_store.vector_manager import VectorStoreManager; agent = GrantAgent(VectorStoreManager())"
```

## Contributing

When extending the RAG implementation:

1. Follow existing code patterns and documentation standards
2. Add comprehensive logging for new features
3. Include error handling and graceful degradation
4. Update configuration options as needed
5. Add tests for new functionality
6. Update this documentation

## License

This RAG implementation follows the same license as the main GrantWatch project.
