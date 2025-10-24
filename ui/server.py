"""
FastAPI Server for AI Retail Agent Team UI
Implements Server-Sent Events (SSE) streaming for real-time agent communication
"""

import os
import sys
import asyncio
import json
from pathlib import Path
from typing import AsyncGenerator, Dict, Any
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path to import agents
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import helper for loading retail-agents-team
try:
    from importlib import util
    
    # Load retail-agents-team module dynamically (handles hyphens in directory name)
    retail_agents_path = parent_dir / "retail-agents-team"
    
    if not retail_agents_path.exists():
        raise FileNotFoundError(f"retail-agents-team directory not found at {retail_agents_path}")
    
    # Create package structure for retail_agents_team
    sys.modules['retail_agents_team'] = type(sys)('retail_agents_team')
    sys.modules['retail_agents_team'].__path__ = [str(retail_agents_path)]
    
    # Import all sub-agents first
    sub_agent_names = [
        "product_search_agent",
        "review_text_analysis_agent", 
        "inventory_agent",
        "shopping_agent",
        "customer_support_agent"
    ]
    
    for sub_agent_name in sub_agent_names:
        # Create sub-agent package
        sub_pkg_name = f"retail_agents_team.{sub_agent_name}"
        sys.modules[sub_pkg_name] = type(sys)(sub_pkg_name)
        sys.modules[sub_pkg_name].__path__ = [str(retail_agents_path / sub_agent_name)]
        
        # Load agent.py
        sub_agent_path = retail_agents_path / sub_agent_name / "agent.py"
        if not sub_agent_path.exists():
            raise FileNotFoundError(f"Agent file not found: {sub_agent_path}")
            
        spec = util.spec_from_file_location(f"{sub_pkg_name}.agent", sub_agent_path)
        module = util.module_from_spec(spec)
        sys.modules[f"{sub_pkg_name}.agent"] = module
        spec.loader.exec_module(module)
    
    # Now import main agent
    main_agent_path = retail_agents_path / "agent.py"
    if not main_agent_path.exists():
        raise FileNotFoundError(f"Main agent file not found: {main_agent_path}")
        
    spec = util.spec_from_file_location("retail_agents_team.agent", main_agent_path)
    agent_module = util.module_from_spec(spec)
    sys.modules["retail_agents_team.agent"] = agent_module
    spec.loader.exec_module(agent_module)
    
    root_agent = agent_module.root_agent
    print("✅ Successfully loaded root_agent:", root_agent.name)
    
except Exception as e:
    print(f"❌ Error loading agent: {e}")
    print(f"   Retail agents path: {retail_agents_path}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import ADK components
try:
    from google.adk.runners import InMemoryRunner
    from google.genai import types  # Import types for Content creation
    print("✅ ADK imports successful")
except ImportError as e:
    print(f"❌ Error importing ADK: {e}")
    print("   Install with: pip install google-adk")
    sys.exit(1)

# Configuration
APP_NAME = "retail_agent_team_ui"
PORT = 8082

# Global runner instance - shared across all sessions
global_runner = None

# Session management
sessions: Dict[str, Dict[str, Any]] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    global global_runner
    
    print(f"🚀 AI Retail Agent Team UI Server Starting")
    print(f"   App Name: {APP_NAME}")
    print(f"   Starting server at http://127.0.0.1:{PORT}")
    
    # Initialize global runner
    global_runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    print("✅ Global runner initialized")
    
    yield
    print("👋 Server shutting down")

# Initialize FastAPI
app = FastAPI(title="AI Retail Agent Team UI", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve main HTML page"""
    index_path = Path(__file__).parent / "index.html"
    return FileResponse(index_path)

@app.get("/events/{session_id}")
async def event_stream(session_id: str):
    """Server-Sent Events endpoint for streaming agent responses"""
    
    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events"""
        
        # Initialize session if not exists
        if session_id not in sessions:
            sessions[session_id] = {
                "messages": []
            }
            
        try:
            # Send connection established event
            yield f"data: {json.dumps({'type': 'connected', 'session_id': session_id})}\n\n"
            
            # Keep connection alive
            while True:
                # Check for new messages
                session = sessions.get(session_id)
                if session and "pending_message" in session:
                    message = session.pop("pending_message")
                    
                    # Process with agent
                    async for chunk in process_agent_response(session_id, message):
                        yield f"data: {json.dumps(chunk)}\n\n"
                
                await asyncio.sleep(0.1)
                
        except asyncio.CancelledError:
            print(f"Client disconnected: {session_id}")
        except Exception as e:
            print(f"Error in event stream: {e}")
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/send/{session_id}")
async def send_message(session_id: str, request: Request):
    """Receive message from client"""
    data = await request.json()
    message = data.get("message", "")
    
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": []
        }
    
    # Store message for processing
    sessions[session_id]["pending_message"] = message
    sessions[session_id]["messages"].append({"role": "user", "content": message})
    
    return {"status": "ok", "session_id": session_id}

async def process_agent_response(session_id: str, message: str) -> AsyncGenerator[Dict[str, Any], None]:
    """Process message through agent and stream response"""
    
    session = sessions.get(session_id)
    if not session:
        yield {"type": "error", "error": "Session not found"}
        return
    
    try:
        # Send start event
        yield {
            "type": "start",
            "message": message
        }
        
        # Create session in runner if this is the first message
        if "adk_session_created" not in session:
            # Create session in the runner's session service
            adk_session = await global_runner.session_service.create_session(
                app_name=APP_NAME,
                user_id="user_123",
                session_id=session_id
            )
            session["adk_session_created"] = True
            print(f"✅ Created ADK session: {session_id}")
        
        # Create Content object from string message
        user_content = types.Content(
            parts=[types.Part(text=message)],
            role="user"
        )
        
        # Stream response from agent using run_async
        full_response = ""
        async for turn in global_runner.run_async(
            session_id=session_id,
            user_id="user_123",
            new_message=user_content
        ):
            # Each turn contains the agent's response
            if hasattr(turn, 'content'):
                content = turn.content
                if hasattr(content, 'parts'):
                    for part in content.parts:
                        if hasattr(part, 'text') and part.text:
                            text = part.text
                            full_response += text
                            
                            # Yield chunks for streaming effect
                            yield {
                                "type": "chunk",
                                "content": text,
                                "author": root_agent.name
                            }
                elif hasattr(content, 'text'):
                    text = content.text
                    full_response += text
                    yield {
                        "type": "chunk",
                        "content": text,
                        "author": root_agent.name
                    }
        
        # Send completion event
        yield {
            "type": "complete",
            "full_response": full_response,
            "author": root_agent.name
        }
        
        # Store in session
        session["messages"].append({
            "role": "assistant",
            "content": full_response,
            "author": root_agent.name
        })
        
    except Exception as e:
        print(f"Error processing agent response: {e}")
        import traceback
        traceback.print_exc()
        yield {
            "type": "error",
            "error": str(e)
        }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": root_agent.name,
        "sessions": len(sessions)
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 AI Retail Agent Team - Web UI")
    print("=" * 60)
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=PORT,
        log_level="info"
    )
