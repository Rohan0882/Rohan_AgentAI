# func_External_Context.py
# Placeholder for simulated web search functionality.

import json

def get_external_context(search_query):
    """
    Simulates a web search to find supplementary information for a case study.
    In a real implementation, this would use a tool like Google Search.
    """
    query = search_query.lower()

    # Mock database of external context
    mock_database = {
        "nokia market share 2007": {
            "source": "Simulated TechCrunch Article",
            "data": "In 2007, Nokia's global market share in the mobile phone market was approximately 49.4%."
        },
        "apple iphone launch date": {
            "source": "Simulated Wikipedia Entry",
            "data": "The first generation iPhone was announced by Apple co-founder Steve Jobs on January 9, 2007."
        }
    }

    result = mock_database.get(query)

    if not result:
        return {"error": "No supplementary information found for the given query."}

    return {"external_context": result}

if __name__ == '__main__':
    # Example usage
    test_query = "nokia market share 2007"
    context = get_external_context(test_query)
    print("--- External Context Search ---")
    print(json.dumps(context, indent=2))
