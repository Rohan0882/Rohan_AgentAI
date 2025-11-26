# tests/test_kotler_v2.py
# Refactored test suite for the Kotler MCP Server using Flask's test client.

import unittest
import json
import os
import shutil

# Add the project root to the Python path to allow for direct import of the app
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kotler_mcp_server.Kotler_MCP_Server import app
from kotler_mcp_server.func_Kotler_RAG import get_rag_retriever

class TestKotlerMCPServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment. Creates the RAG index."""
        print("Ensuring RAG index exists for tests...")
        # Clean up any old index first
        if os.path.exists("kotler_index.faiss"):
            shutil.rmtree("kotler_index.faiss")
        # Directly call the function to create the index
        get_rag_retriever()
        print("RAG index created.")

    @classmethod
    def tearDownClass(cls):
        """Tear down the test environment. Cleans up the RAG index."""
        if os.path.exists("kotler_index.faiss"):
            shutil.rmtree("kotler_index.faiss")
            print("\\nCleaned up RAG index.")

    def setUp(self):
        """Create a new test client for each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_swot_analyzer_success(self):
        """Test the /swot_analyzer endpoint with valid data."""
        payload = {"case_data": {"text": "Our company has a strong brand but high cost."}}
        response = self.client.post('/swot_analyzer', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["strengths"], ["strong brand recognition"])
        self.assertEqual(data["weaknesses"], ["high production costs"])

    def test_swot_analyzer_error(self):
        """Test the /swot_analyzer endpoint with empty data."""
        payload = {"case_data": {"text": ""}}
        response = self.client.post('/swot_analyzer', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data["error"], "Input text for SWOT analysis cannot be empty.")

    def test_market_segmenter_success(self):
        """Test the /market_segmenter endpoint with valid data."""
        payload = {"demographics": {"age": 25, "income": 60000}}
        response = self.client.post('/market_segmenter', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["segments"], ["Young Professionals"])

    def test_market_segmenter_error(self):
        """Test the /market_segmenter endpoint with missing data."""
        payload = {"demographics": {"age": 45}}
        response = self.client.post('/market_segmenter', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data["error"], "Missing 'age' or 'income' in demographics data.")

    def test_fourps_mix_success(self):
        """Test the /fourps_mix endpoint with valid data."""
        payload = {"strategy_goals": {"goal": "gain market share"}}
        response = self.client.post('/fourps_mix', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("product", data)
        self.assertIn("price", data)

    def test_rag_query_success(self):
        """Test the /rag_query endpoint."""
        payload = {"question": "What are the 4Ps of marketing?"}
        response = self.client.post('/rag_query', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("answer", data)
        self.assertIn("Product, Price, Place, and Promotion", data["answer"])

if __name__ == '__main__':
    unittest.main()
