# ==============================================================================
# J.A.R.V.I.S. Assistant (Optimized Speed - Internal Knowledge Only)
#
# This script is optimized for low latency by disabling Google Search grounding.
# The AI will respond quickly based on its vast, pre-trained internal knowledge.
#
# Dependencies: requests (pip install requests)
# Environment: Designed to run fast in environments like Pydroid 3.
# ==============================================================================
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')  # put your HTML in 'templates' folder

# Route to serve frontend
@app.route("/")
def home():
    return render_template("index.html")  # your chatbot HTML file

# Route for chatbot messages
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    
    # Replace this with your chatbot function call
    bot_reply = f"Bot says: {user_msg}"  
    
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)  # Runs at http://127.0.0.1:5000 locally





import requests
import json
import time
import sys

# --- CONFIGURATION ---

# API Key is sensitive. It has been placed here as requested.
API_KEY = "AIzaSyBwouSEYCymxZAmP9AqjPCj4ph41WbsJYM"

# API Endpoint and Model Selection
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
MODEL = "gemini-2.5-flash-preview-05-20"

# Retry settings for API calls
MAX_RETRIES = 3
INITIAL_DELAY_SECONDS = 1

# --- PERSONA & INSTRUCTION ---

# Note: Removed mandatory grounding instruction for speed optimization.
SYSTEM_PROMPT = """
You are 'VISION', a highly sophisticated artificial intelligence, modeled after a futuristic operating system (like J.A.R.V.I.S. or F.R.I.D.A.Y.).
Your primary function is to serve as a fast and intelligent assistant, providing concise, factual, and visually attractive answers based on your internal knowledge.

RULES:
1. Tone: Professional, highly succinct, and always helpful. Prioritize speed.
2. Formatting: Use Markdown for all output text.
3. Acknowledge and execute. Do not engage in lengthy intros or pleasantries.
"""

# --- UTILITY FUNCTIONS ---

def get_base_payload(user_query):
    """
    Constructs the base request payload.
    The 'tools' property for Google Search is omitted to improve speed.
    """
    return {
        "contents": [{
            "parts": [{"text": user_query}]
        }],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        }
        # NOTE: Google Search grounding (tools property) is intentionally REMOVED
        # here to achieve maximum response speed.
    }

def call_gemini_api(user_query):
    """
    Handles the API call with exponential backoff for retry attempts.
    Returns the generated text.
    """
    url_with_key = f"{API_URL}?key={API_KEY}"
    payload = get_base_payload(user_query)

    headers = {'Content-Type': 'application/json'}
    
    # Exponential Backoff Implementation
    for attempt in range(MAX_RETRIES):
        delay = INITIAL_DELAY_SECONDS * (2 ** attempt)
        try:
            print(f"[{MODEL.upper()}] | Initializing sequence... (Attempt {attempt + 1}/{MAX_RETRIES})")
            # Force flush output to ensure print statements appear immediately in console environments
            sys.stdout.flush() 
            
            response = requests.post(
                url_with_key,
                headers=headers,
                data=json.dumps(payload),
                timeout=15 # Reduced timeout to 15 seconds, matching the focus on speed
            )
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            result = response.json()
            candidate = result.get('candidates', [None])[0]

            if not candidate:
                return 'Error: API response contained no candidates.', []
            
            # Extract Generated Text
            text = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'Error: Text content not found.')

            # Since grounding is disabled, sources will be empty
            sources = [] 
                
            return text, sources

        except requests.exceptions.RequestException as e:
            print(f"Connection error on attempt {attempt + 1}: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
            else:
                return f"Error: Failed to connect to the AI system after {MAX_RETRIES} attempts.", []
        except Exception as e:
            return f"Critical Error: An unexpected issue occurred: {e}", []
            

def main_assistant_loop():
    """Main loop for the interactive assistant."""
    print("=" * 70)
    print("J.A.R.V.I.S. ASSISTANT - VISION PROTOCOL INITIALIZED (SPEED MODE)")
    print(f"Model: {MODEL} | Search Grounding: DISABLED (FOR SPEED)")
    print("Enter 'exit' or 'quit' to terminate the assistant.")
    print("-" * 70)

    while True:
        try:
            user_input = input("USER QUERY >>> ")
            
            if user_input.lower() in ['exit', 'quit']:
                print("\n[VISION] | System shutting down. Have a productive day.")
                break
            
            if not user_input.strip():
                continue

            # API Call
            generated_text, sources = call_gemini_api(user_input)

            # Output Formatting
            print("\n" + "=" * 70)
            print("[VISION] | RESPONSE GENERATED:")
            
            if generated_text:
                print(generated_text)
            
            # Since sources are always empty in this optimized mode, we don't display them.
            
            print("-" * 70)
            
        except EOFError:
            print("\n[VISION] | Input stream closed. Terminating.")
            break
        except KeyboardInterrupt:
            print("\n[VISION] | Sequence interrupted. Terminating.")
            break

# --- EXECUTION START ---

if __name__ == "__main__":
    main_assistant_loop()
  
