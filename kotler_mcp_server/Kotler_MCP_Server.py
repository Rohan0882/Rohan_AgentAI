# This file hosts the Kotler MCP Server.
# It exposes the Kotlerian frameworks as callable code APIs using Flask.

from flask import Flask, request, jsonify
from .func_Kotler_RAG import query_rag

app = Flask(__name__)

# --- Core Kotlerian Framework Functions (with Error Handling) ---

def SWOT_Analyzer(case_data):
    """
    Parses text into classified Strengths, Weaknesses, Opportunities, and Threats.
    Includes basic error handling for incomplete data.
    """
    try:
        text = case_data.get("text", "").lower()
        if not text:
            return {"error": "Input text for SWOT analysis cannot be empty."}

        return {
            "strengths": ["strong brand recognition"] if "strong brand" in text else [],
            "weaknesses": ["high production costs"] if "cost" in text else [],
            "opportunities": ["emerging markets"] if "emerging" in text else [],
            "threats": ["new competitors"] if "competitor" in text else []
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred in SWOT_Analyzer: {e}"}

def Market_Segmenter(demographics):
    """
    Applies segmentation bases to raw data.
    Includes basic error handling for missing keys.
    """
    try:
        age = demographics.get("age")
        income = demographics.get("income")

        if age is None or income is None:
            return {"error": "Missing 'age' or 'income' in demographics data."}

        if age > 40 and income > 75000:
            return {"segments": ["High-Income Mature Consumers"]}
        elif age < 30:
            return {"segments": ["Young Professionals"]}
        return {"segments": ["General Audience"]}
    except TypeError:
        return {"error": "Invalid data type for age or income. Integers are required."}
    except Exception as e:
        return {"error": f"An unexpected error occurred in Market_Segmenter: {e}"}

def FourPs_Mix(strategy_goals):
    """
    Generates a draft 4P (Product, Price, Place, Promotion) recommendation.
    Includes basic error handling.
    """
    try:
        goal = strategy_goals.get("goal", "").lower()
        if not goal:
            return {"error": "Strategy goal cannot be empty."}

        if "market share" in goal:
            return {
                "product": "Develop a new, feature-rich product variant.",
                "price": "Implement competitive pricing strategy.",
                "place": "Expand distribution channels to new regions.",
                "promotion": "Launch an aggressive advertising campaign."
            }
        return {
            "product": "Maintain current product line.",
            "price": "Standard pricing.",
            "place": "Existing distribution channels.",
            "promotion": "Standard marketing efforts."
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred in FourPs_Mix: {e}"}

# --- API Endpoints ---

@app.route('/swot_analyzer', methods=['POST'])
def api_swot_analyzer():
    """API endpoint for SWOT analysis."""
    if not request.json or 'case_data' not in request.json:
        return jsonify({"error": "Missing 'case_data' in request body"}), 400

    result = SWOT_Analyzer(request.json['case_data'])
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/market_segmenter', methods=['POST'])
def api_market_segmenter():
    """API endpoint for Market Segmentation."""
    if not request.json or 'demographics' not in request.json:
        return jsonify({"error": "Missing 'demographics' in request body"}), 400

    result = Market_Segmenter(request.json['demographics'])
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/fourps_mix', methods=['POST'])
def api_fourps_mix():
    """API endpoint for 4Ps Mix recommendation."""
    if not request.json or 'strategy_goals' not in request.json:
        return jsonify({"error": "Missing 'strategy_goals' in request body"}), 400

    result = FourPs_Mix(request.json['strategy_goals'])
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/rag_query', methods=['POST'])
def api_rag_query():
    """API endpoint for the RAG tool."""
    if not request.json or 'question' not in request.json:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    question = request.json['question']
    answer = query_rag(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    # Note: In a production environment, use a proper WSGI server like Gunicorn.
    # Disable debug mode for automated tests by checking an environment variable.
    import os
    debug_mode = os.environ.get("FLASK_ENV") != "testing"
    app.run(debug=debug_mode, port=5000)
