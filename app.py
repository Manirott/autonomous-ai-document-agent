from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from agent import AutonomousAgent
from models import AgentRequest, AgentResponse

app = FastAPI(
    title="Autonomous AI Document Agent",
    description="An AI Agent that autonomously plans, executes tasks, and generates professional Word documents.",
    version="1.0.0"
)

# Allow the frontend (whether opened as a local file, served from a different
# port, or hosted elsewhere) to call this API. Tighten allow_origins to your
# actual frontend origin(s) before deploying this publicly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = AutonomousAgent()


@app.get("/health")
def health_check():
    return {
        "status": "running",
        "service": "Autonomous AI Document Agent"
    }


@app.post(
    "/agent",
    response_model=AgentResponse
)
def run_agent(request: AgentRequest):

    try:

        response = agent.run(request.request)

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/download")
def download_document(path: str):

    return FileResponse(
        path=path,
        filename=path.split("/")[-1].split("\\")[-1],
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


# Serve the frontend (index.html + any other static assets) at "/".
# This is mounted LAST so it doesn't shadow the /agent, /download, or /health
# routes above. Put index.html inside a "static" folder next to this file.
app.mount("/", StaticFiles(directory="static", html=True), name="static")