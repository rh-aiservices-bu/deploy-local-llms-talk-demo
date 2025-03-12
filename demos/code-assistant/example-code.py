### FastAPI Endpoints ###
@app.get("/health")
def read_health():
    """Health check endpoint to verify the API is running."""
    return {"message": "Status:OK"}

@app.get("/config")
def get_config():
    """Expose backend configuration like the model name."""
    return {
        "model_name": MODEL_NAME
    }