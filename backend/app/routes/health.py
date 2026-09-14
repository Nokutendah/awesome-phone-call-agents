from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CallBot Detective API",
        "version": "0.1.0"
    }
