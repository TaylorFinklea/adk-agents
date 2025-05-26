from google.adk.agents import Agent
from google.adk.tools import google_search
import vertexai
import os
from dotenv import load_dotenv
from vertexai.preview import reasoning_engines

# Load environment variables from .env file
load_dotenv()


vertexai.init(
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION"),
    staging_bucket=os.getenv("STAGING_BUCKET"),
)

# Deployment mode from .env file
DEPLOYMENT_MODE = os.getenv("DEPLOYMENT_MODE", "cloudrun").lower()  # "agent_engine" or "cloudrun"

# Shared agent configuration
AGENT_NAME = "basic_search_agent"
AGENT_MODEL = "gemini-2.5-flash-preview-05-20"
AGENT_DESCRIPTION = "Agent to answer questions using Google Search."
AGENT_INSTRUCTION = "You are an expert researcher. You always stick to the facts."
AGENT_TOOLS = [google_search]

# Initialize agent with appropriate callbacks based on deployment mode
if DEPLOYMENT_MODE == "cloudrun":
    # Cloud Run: Full Opik observability
    try:
        from opik.integrations.adk import OpikTracer
        opik_tracer = OpikTracer()

        root_agent = Agent(
            name=AGENT_NAME,
            model=AGENT_MODEL,
            description=AGENT_DESCRIPTION,
            instruction=AGENT_INSTRUCTION,
            tools=AGENT_TOOLS,
            before_agent_callback=opik_tracer.before_agent_callback,
            after_agent_callback=opik_tracer.after_agent_callback,
            before_model_callback=opik_tracer.before_model_callback,
            after_model_callback=opik_tracer.after_model_callback,
            before_tool_callback=opik_tracer.before_tool_callback,
            after_tool_callback=opik_tracer.after_tool_callback,
        )
        print("✓ Agent initialized with Opik observability for Cloud Run")
    except ImportError:
        # Fallback without Opik
        root_agent = Agent(
            name=AGENT_NAME,
            model=AGENT_MODEL,
            description=AGENT_DESCRIPTION,
            instruction=AGENT_INSTRUCTION,
            tools=AGENT_TOOLS,
        )
        print("⚠ Opik not available, using agent without callbacks")
else:
    # Agent Engine: Native tracing only (no Opik callbacks due to serialization)
    root_agent = Agent(
        name=AGENT_NAME,
        model=AGENT_MODEL,
        description=AGENT_DESCRIPTION,
        instruction=AGENT_INSTRUCTION,
        tools=AGENT_TOOLS,
    )
    print("✓ Agent initialized for Agent Engine (native tracing)")

# Wrap agent for tracing (for local testing and deployment)
app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

def deploy_to_agent_engine():
    """Deploy to Google Cloud Agent Engine with native monitoring and tracing"""
    from vertexai import agent_engines

    print("Deploying agent to Agent Engine...")
    print("This may take several minutes...")

    # Create deployment app with tracing
    deployment_app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    remote_app = agent_engines.create(
        agent_engine=deployment_app,
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]",
        ]
    )

    print(f"✓ Agent deployed successfully!")
    print(f"Resource name: {remote_app.resource_name}")
    print(f"Monitor at: https://console.cloud.google.com/vertex-ai/agent-engine")
    print(f"Traces at: https://console.cloud.google.com/traces/list")

    return remote_app

def deploy_to_cloudrun():
    """Deploy to Google Cloud Run with full observability"""
    import subprocess

    print("Deploying agent to Cloud Run...")
    print("This deployment includes full Opik observability!")

    # Set environment variable for Cloud Run deployment
    env = os.environ.copy()
    env["DEPLOYMENT_MODE"] = "cloudrun"

    try:
        cmd = [
            "adk", "deploy", "cloud_run",
            "--project", PROJECT_ID,
            "--region", LOCATION,
            "."
        ]

        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd="..", env=env, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Cloud Run deployment successful!")
            print(result.stdout)
            print("\nFeatures enabled:")
            print("✓ Full Opik observability")
            print("✓ Google Search capabilities")
            print("✓ Auto-scaling")
        else:
            print("✗ Deployment failed!")
            print("Error:", result.stderr)
            print("Output:", result.stdout)

    except Exception as e:
        print(f"Error during deployment: {e}")

if __name__ == "__main__":
    import sys

    print(f"Google Search Agent (Mode: {DEPLOYMENT_MODE.upper()})")
    print("=" * 50)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "deploy-agent-engine":
            deploy_to_agent_engine()
        elif command == "deploy-cloudrun":
            deploy_to_cloudrun()
        else:
            print("Unknown command. Use 'deploy-agent-engine' or 'deploy-cloudrun'")
    else:
        print("Usage:")
        print("  Local testing:")
        print("    adk run google-search-agent")
        print("    adk web .")
        print()
        print("  Deploy to Agent Engine (native tracing):")
        print("    python agent.py deploy-agent-engine")
        print()
        print("  Deploy to Cloud Run (with Opik):")
        print("    python agent.py deploy-cloudrun")
        print()
        print(f"Current mode from .env: {DEPLOYMENT_MODE}")
        print("Change DEPLOYMENT_MODE in .env file to switch modes")
