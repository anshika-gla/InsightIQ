from fastapi import APIRouter, HTTPException
from models.query_models import QueryRequest
from services.query_service import process_query

router = APIRouter(prefix="/api", tags=["Analytics"])


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "InsightIQ"
    }


@router.post("/query")
def query(request: QueryRequest):
    try:
        response = process_query(request.query)

        return {
            "query": response["query"],
            "status": response.get("status", "success"),
            "plan": response.get("plan", {}),
            "result": response.get("result"),
            "generated_logic": response.get(
                "generated_logic",
                response.get("logic", {})
            ),
            "confidence_score": response.get(
                "confidence_score",
                response.get("confidence", 0.0)
            ),
            "explanation": response.get(
                "explanation",
                "Query processed successfully."
            )
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )