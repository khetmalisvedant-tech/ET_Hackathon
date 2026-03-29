import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from services.orchestrator import run_workflow

# ✅ FIRST create app
app = FastAPI()

# ✅ THEN add CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES AFTER app is defined

@app.get("/")
def home():
    return {"message": "AutoFlow AI Backend Running 🚀"}

@app.post("/execute")
async def execute(request: Request):
    data = await request.json()

    user_input = data.get("input")
    location = data.get("location")

    result = run_workflow(user_input, location)

    return {"response": result}