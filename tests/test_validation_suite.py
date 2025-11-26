# tests/test_validation_suite.py
# A validation suite to simulate a full agent workflow on a sample case study.

import unittest
import json
import os
import shutil

# Add the project root to the Python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kotler_mcp_server.Kotler_MCP_Server import app
from kotler_mcp_server.func_Kotler_RAG import get_rag_retriever

# --- Sample Case Study Data ---
SAMPLE_CASE_STUDY = {
    "name": "Nokia",
    "text": """
    Nokia, a Finnish company, was once the dominant market leader in the mobile phone industry.
    A key strength was its strong brand recognition and reputation for producing durable, high-quality hardware.
    However, the company faced high production costs, which squeezed margins.
    The emergence of the smartphone era, driven by Apple's iPhone and Google's Android, presented new emerging markets and opportunities.
    Unfortunately, Nokia's slow response to this paradigm shift and its reliance on the Symbian operating system
    became a major weakness, ultimately allowing a new competitor, Apple, to capture the market.
    """,
    "strategic_goal": "Regain market share in the smartphone era."
}

class TestValidationSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment. Creates the RAG index."""
        print("Ensuring RAG index exists for validation suite...")
        if not os.path.exists("kotler_index.faiss"):
            get_rag_retriever()
        print("RAG index is ready.")

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
        self.artifacts = {}

    def log_artifact(self, key, value):
        """Helper function to simulate the agent's artifact logging."""
        print(f"--- Logging Artifact: {key} ---")
        self.artifacts[key] = value

    def test_full_swot_analysis_workflow(self):
        """Simulates the full agent workflow for a SWOT analysis."""

        # Step 1: Deconstruct Request (Implicitly done by the test setup)
        user_request = {"case_name": SAMPLE_CASE_STUDY["name"], "framework_requested": "SWOT"}
        self.log_artifact("deconstructed_request", user_request)

        # Step 2: Gather Contextual Data (RAG)
        rag_payload = {"question": "What is a SWOT analysis?"}
        rag_response = self.client.post('/rag_query', data=json.dumps(rag_payload), content_type='application/json')
        self.assertEqual(rag_response.status_code, 200)
        rag_data = rag_response.get_json()
        self.log_artifact("framework_definition", rag_data)
        self.assertIn("answer", rag_data)

        # Step 3: Execute Core Analysis (SWOT)
        swot_payload = {"case_data": {"text": SAMPLE_CASE_STUDY["text"]}}
        swot_response = self.client.post('/swot_analyzer', data=json.dumps(swot_payload), content_type='application/json')
        self.assertEqual(swot_response.status_code, 200)
        swot_results = swot_response.get_json()
        self.log_artifact("raw_swot_analysis", swot_results)
        self.assertEqual(swot_results["strengths"], ["strong brand recognition"])
        self.assertEqual(swot_results["weaknesses"], ["high production costs"])
        self.assertEqual(swot_results["opportunities"], ["emerging markets"])
        self.assertEqual(swot_results["threats"], ["new competitors"])

        # Step 4: Synthesize and Present Findings
        summary = (
            f"Based on the SWOT analysis of {self.artifacts['deconstructed_request']['case_name']}, "
            f"the key strength identified was its {swot_results['strengths'][0]}. "
            f"However, a significant weakness was its {swot_results['weaknesses'][0]}. "
            f"The company should focus on the opportunity of {swot_results['opportunities'][0]} "
            f"while being mindful of the threat from at least one {swot_results['threats'][0]}."
        )
        self.log_artifact("final_summary", summary)

        # Final Verification
        self.assertIn("deconstructed_request", self.artifacts)
        self.assertIn("raw_swot_analysis", self.artifacts)
        self.assertIn("final_summary", self.artifacts)
        print("\\n--- Final Synthesized Summary ---")
        print(self.artifacts["final_summary"])

if __name__ == '__main__':
    unittest.main()
