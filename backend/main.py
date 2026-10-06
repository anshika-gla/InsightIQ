
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.query_models import QueryRequest
from services.query_service import QueryService


# Initialize FastAPI application
app = FastAPI(
    title="InsightIQ",
    description="Intelligent Analytics Query Engine",
    version="1.0.0",
)


# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize query service
query_service = QueryService()


# Health check endpoint
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "InsightIQ",
    }


# Natural language analytics endpoint
@app.post("/api/query")
async def query_endpoint(request: QueryRequest):
    try:
        result = await query_service.process_query(request.query)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    except Exception as error:
        raise HTTPException(
           status_code=500,
           detail=str(error),
        ) from error

 