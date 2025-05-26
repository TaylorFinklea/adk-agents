import vertexai
from vertexai import agent_engines
import json
from datetime import datetime

PROJECT_ID = "novalark-prod"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://novalark-ai-testing-bucket-202505"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

def print_event_details(event):
    """Debug function to see event structure"""
    print(f"\nDEBUG - Event structure: {json.dumps(event, indent=2)}")

def extract_text_from_event(event):
    """Extract text from various event formats"""
    text_content = ""
    
    # Print full event for debugging
    # print(f"DEBUG - Full event: {json.dumps(event, indent=2)}")
    
    if isinstance(event, dict):
        # Check for 'parts' structure
        if 'parts' in event:
            for part in event['parts']:
                if isinstance(part, dict):
                    # Standard text part
                    if 'text' in part:
                        text_content += part['text']
                    # Function call part
                    elif 'function_call' in part:
                        func_call = part['function_call']
                        print(f"\n[Function Call: {func_call.get('name', 'unknown')}]", end="")
                    # Function response part
                    elif 'function_response' in part:
                        func_resp = part['function_response']
                        print(f"\n[Function Response: {func_resp.get('name', 'unknown')}]", end="")
        
        # Check for direct 'text' field
        elif 'text' in event:
            text_content += event['text']
        
        # Check for 'content' field
        elif 'content' in event:
            content = event['content']
            if isinstance(content, dict) and 'parts' in content:
                for part in content['parts']:
                    if isinstance(part, dict) and 'text' in part:
                        text_content += part['text']
            elif isinstance(content, str):
                text_content += content
        
        # Check for role-based structure
        elif 'role' in event and event.get('role') == 'model':
            # This might be a chat-style response
            if 'parts' in event:
                for part in event['parts']:
                    if isinstance(part, dict) and 'text' in part:
                        text_content += part['text']
    
    return text_content

def interact_with_agent(resource_name):
    """Interactive session with deployed Agent Engine agent"""
    remote_app = agent_engines.AgentEngine(resource_name)
    
    print(f"Connected to Agent: {resource_name}")
    print("Type 'quit' to exit, 'new' for new session, 'debug' to toggle debug mode")
    print(f"View traces at: https://console.cloud.google.com/traces/list?project={PROJECT_ID}")
    print("=" * 60)
    
    debug_mode = False
    
    # Create initial session
    user_id = input("Enter your user ID (or press Enter for default): ").strip() or "user_123"
    session = remote_app.create_session(user_id=user_id)
    session_id = session["id"]
    
    print(f"Created session: {session_id}")
    print(f"User: {user_id}")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            if user_input.lower() == 'debug':
                debug_mode = not debug_mode
                print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
                continue
            
            if user_input.lower() == 'new':
                session = remote_app.create_session(user_id=user_id)
                session_id = session["id"]
                print(f"Created new session: {session_id}")
                continue
            
            if user_input.lower() == 'sessions':
                sessions = remote_app.list_sessions(user_id=user_id)
                print(f"Your sessions: {sessions}")
                continue
            
            if not user_input:
                continue
            
            print("Agent: ", end="", flush=True)
            
            # Stream the response
            full_response = ""
            event_count = 0
            start_time = datetime.now()
            
            for event in remote_app.stream_query(
                user_id=user_id,
                session_id=session_id,
                message=user_input,
            ):
                event_count += 1
                
                if debug_mode:
                    print(f"\n[DEBUG Event {event_count}]:")
                    print_event_details(event)
                    print("[/DEBUG]\n", end="")
                
                # Extract and print text
                text = extract_text_from_event(event)
                if text:
                    print(text, end="", flush=True)
                    full_response += text
            
            if not full_response.strip():
                print("[No text response received]")
                if not debug_mode:
                    print("Try typing 'debug' to see raw event data")
            
            # Show timing and trace info
            duration = (datetime.now() - start_time).total_seconds()
            print(f"\n[Response time: {duration:.2f}s | Events: {event_count} | Traces: https://console.cloud.google.com/traces/list?project={PROJECT_ID}]")
            print()  # New line after response
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()

def batch_test(resource_name, queries):
    """Test multiple queries in batch"""
    remote_app = agent_engines.AgentEngine(resource_name)
    
    user_id = "batch_test_user"
    session = remote_app.create_session(user_id=user_id)
    session_id = session["id"]
    
    print(f"Running batch test with {len(queries)} queries...")
    
    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] Query: {query}")
        print("Response: ", end="")
        
        start_time = datetime.now()
        response_text = ""
        
        for event in remote_app.stream_query(
            user_id=user_id,
            session_id=session_id,
            message=query,
        ):
            text = extract_text_from_event(event)
            if text:
                response_text += text
                print(text, end="", flush=True)
        
        duration = (datetime.now() - start_time).total_seconds()
        if not response_text.strip():
            print("[No response]")
        print(f"\nDuration: {duration:.2f}s")

if __name__ == "__main__":
    resource_name = input("Enter your agent resource name: ").strip()
    
    if not resource_name:
        print("Resource name is required")
        exit(1)
    
    mode = input("Choose mode - (i)nteractive or (b)atch test: ").strip().lower()
    
    if mode.startswith('b'):
        test_queries = [
            "What is machine learning?",
            "Tell me about recent AI developments", 
            "How does neural network training work?",
            "What are the applications of AI in healthcare?"
        ]
        batch_test(resource_name, test_queries)
    else:
        interact_with_agent(resource_name)