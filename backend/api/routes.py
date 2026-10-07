from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)


@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Analytics Query Engine is running"
    })


@api.route("/query", methods=["POST"])
def query():
    data = request.get_json()

    query_text = data.get("query", "").strip()

    if not query_text:
        return jsonify({
            "error": "Query is required"
        }), 400

    # Query engine yahan call hoga
    # Abhi temporary response
    return jsonify({
        "query": query_text,
        "generated_logic": "",
        "result": "",
        "confidence_score": 0.0,
        "explanation": "Query received successfully."
    })