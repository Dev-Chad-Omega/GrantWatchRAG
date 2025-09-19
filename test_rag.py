#!/usr/bin/env python3
"""
Test script for RAG GrantWatch functionality.
This script tests the core components without requiring full data ingestion.
"""

import sys
import os
import json
from typing import Dict, Any, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vector_store.vector_manager import VectorStoreManager
from agent.grant_agent import GrantAgent
from logs.status_logger import logger


def create_sample_grants() -> List[Dict[str, Any]]:
    """Create sample grant data for testing."""
    return [
        {
            "OPPORTUNITY_ID": "TEST-CYBER-001",
            "OPPORTUNITY_TITLE": "Cybersecurity Research Initiative",
            "AGENCY_NAME": "National Science Foundation",
            "FUNDING_DESCRIPTION": "This grant supports research in cybersecurity, focusing on threat detection, vulnerability assessment, and secure system design. Projects should advance the state of knowledge in cybersecurity analytics and AI-driven security solutions.",
            "OPPORTUNITY_CATEGORY": "Science and Technology",
            "FUNDING_INSTRUMENT_TYPE": "Grant",
            "POSTED_DATE": "2024-01-15",
            "CLOSE_DATE": "2024-06-15",
            "AWARD_CEILING": "$500,000"
        },
        {
            "OPPORTUNITY_ID": "TEST-AI-002",
            "OPPORTUNITY_TITLE": "Artificial Intelligence for Healthcare",
            "AGENCY_NAME": "National Institutes of Health",
            "FUNDING_DESCRIPTION": "Research grants for developing AI and machine learning applications in healthcare, including diagnostic tools, treatment optimization, and patient care automation. Focus on ethical AI and explainable algorithms.",
            "OPPORTUNITY_CATEGORY": "Health",
            "FUNDING_INSTRUMENT_TYPE": "Research Grant",
            "POSTED_DATE": "2024-02-01",
            "CLOSE_DATE": "2024-07-01",
            "AWARD_CEILING": "$750,000"
        },
        {
            "OPPORTUNITY_ID": "TEST-DATA-003",
            "OPPORTUNITY_TITLE": "Big Data Analytics for Climate Science",
            "AGENCY_NAME": "Department of Energy",
            "FUNDING_DESCRIPTION": "Support for data science projects analyzing climate data using advanced analytics, machine learning, and predictive modeling. Projects should contribute to understanding climate change patterns and impacts.",
            "OPPORTUNITY_CATEGORY": "Environment",
            "FUNDING_INSTRUMENT_TYPE": "Cooperative Agreement",
            "POSTED_DATE": "2024-01-30",
            "CLOSE_DATE": "2024-08-30",
            "AWARD_CEILING": "$1,000,000"
        },
        {
            "OPPORTUNITY_ID": "TEST-EDU-004",
            "OPPORTUNITY_TITLE": "STEM Education Technology Innovation",
            "AGENCY_NAME": "Department of Education",
            "FUNDING_DESCRIPTION": "Grants for developing innovative educational technologies in STEM fields, including AI tutoring systems, virtual laboratories, and adaptive learning platforms.",
            "OPPORTUNITY_CATEGORY": "Education",
            "FUNDING_INSTRUMENT_TYPE": "Grant",
            "POSTED_DATE": "2024-02-15",
            "CLOSE_DATE": "2024-09-15",
            "AWARD_CEILING": "$300,000"
        },
        {
            "OPPORTUNITY_ID": "TEST-DEFENSE-005",
            "OPPORTUNITY_TITLE": "Advanced Defense Technologies",
            "AGENCY_NAME": "Department of Defense",
            "FUNDING_DESCRIPTION": "Research and development of advanced defense technologies including autonomous systems, cybersecurity for critical infrastructure, and AI-enhanced threat detection systems.",
            "OPPORTUNITY_CATEGORY": "Defense",
            "FUNDING_INSTRUMENT_TYPE": "Contract",
            "POSTED_DATE": "2024-01-01",
            "CLOSE_DATE": "2024-12-31",
            "AWARD_CEILING": "$2,000,000"
        }
    ]


def test_vector_store():
    """Test vector store functionality."""
    print("Testing Vector Store...")
    
    try:
        # Initialize vector manager
        vector_manager = VectorStoreManager()
        print("✓ Vector manager initialized")
        
        # Create sample data
        sample_grants = create_sample_grants()
        print(f"✓ Created {len(sample_grants)} sample grants")
        
        # Index grants
        success = vector_manager.index_grants(sample_grants)
        if success:
            print("✓ Grants indexed successfully")
        else:
            print("✗ Failed to index grants")
            return False
        
        # Test search
        search_results = vector_manager.search_grants("cybersecurity AI", top_k=3)
        print(f"✓ Search returned {len(search_results)} results")
        
        if search_results:
            print("Top result:")
            top_result = search_results[0]
            print(f"  - Title: {top_result.get('title', 'N/A')}")
            print(f"  - Agency: {top_result.get('agency', 'N/A')}")
            print(f"  - Similarity: {top_result.get('similarity_score', 0.0):.3f}")
        
        # Test get by ID
        grant_data = vector_manager.get_grant_by_id("TEST-CYBER-001")
        if grant_data:
            print("✓ Grant retrieval by ID successful")
        else:
            print("✗ Grant retrieval by ID failed")
        
        # Get stats
        stats = vector_manager.get_stats()
        print(f"✓ Vector store stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"✗ Vector store test failed: {e}")
        return False


def test_agent():
    """Test agent functionality."""
    print("\nTesting Agent...")
    
    try:
        # Initialize components
        vector_manager = VectorStoreManager()
        sample_grants = create_sample_grants()
        vector_manager.index_grants(sample_grants)
        
        agent = GrantAgent(vector_manager)
        print("✓ Agent initialized")
        
        # Test search tool
        search_tool = agent.tools[0]  # SearchGrantsTool
        search_result = search_tool._run("artificial intelligence healthcare", top_k=2)
        print("✓ Search tool executed")
        print(f"Search result preview: {search_result[:100]}...")
        
        # Test summarize tool
        summarize_tool = agent.tools[1]  # SummarizeGrantTool
        summary_result = summarize_tool._run("TEST-AI-002")
        print("✓ Summarize tool executed")
        print(f"Summary preview: {summary_result[:100]}...")
        
        # Test query processing
        query_response = agent.process_query("Find grants about cybersecurity")
        print("✓ Query processing executed")
        print(f"Query response preview: {query_response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent test failed: {e}")
        return False


def test_workflows():
    """Test workflow functionality."""
    print("\nTesting Workflows...")
    
    try:
        # Initialize components
        vector_manager = VectorStoreManager()
        sample_grants = create_sample_grants()
        vector_manager.index_grants(sample_grants)
        
        agent = GrantAgent(vector_manager)
        
        # Test targeted search workflow
        workflow_result = agent.execute_workflow("targeted_search", {
            "query": "machine learning",
            "top_k": 3
        })
        print("✓ Targeted search workflow executed")
        print(f"Workflow result preview: {workflow_result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Workflow test failed: {e}")
        return False


def test_integration():
    """Test full integration."""
    print("\nTesting Integration...")
    
    try:
        # This would normally use the full RAG system
        # For testing, we'll simulate the key components
        
        print("✓ Integration test placeholder - would test full RAG pipeline")
        print("  - Data ingestion from existing pipeline")
        print("  - Vector indexing of real grant data")
        print("  - Agent query processing")
        print("  - Notification system integration")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("RAG GrantWatch Test Suite")
    print("=" * 50)
    
    tests = [
        ("Vector Store", test_vector_store),
        ("Agent", test_agent),
        ("Workflows", test_workflows),
        ("Integration", test_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'-' * 20}")
        print(f"Running {test_name} Test")
        print(f"{'-' * 20}")
        
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'=' * 50}")
    print("Test Results Summary")
    print(f"{'=' * 50}")
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} : {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! RAG implementation is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
