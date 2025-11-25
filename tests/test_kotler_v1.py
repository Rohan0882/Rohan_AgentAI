import sys
import os
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kotler_mcp_server.Kotler_MCP_Server import SWOT_Analyzer

def test_swot_analyzer():
    """
    Tests the SWOT_Analyzer function.
    """
    sample_text = "This is a sample text for SWOT analysis."
    result = SWOT_Analyzer(sample_text)

    # Verify the output structure
    expected_keys = ["strengths", "weaknesses", "opportunities", "threats"]
    assert all(key in result for key in expected_keys)

    # Save the test result as a JSON artifact
    os.makedirs('artifacts', exist_ok=True)
    with open('artifacts/test_Kotler_V1.json', 'w') as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    test_swot_analyzer()
    print("Test passed.")
