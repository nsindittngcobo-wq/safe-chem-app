# ====================================================================================
# MENTAL MAP: Vision API Test Script
#
# GOAL: Send an image of a household item to a Vision Model and recieve a textual description to verify that our API setup works.
# =====================================================================================

#from http import client
import os
import base64
from dotenv import load_dotenv
from groq import Groq

# ==================================================================================
#STAGE 1: Environemnt Setup & API Key Security
#
# WHAT: Load hidden credentials from the local '.env' file into Python.
# WHY: Keeps sensitive keys out of public code repositories (like GitHub).
# ALTERNIVE: Hardcoding the API key string directly into this file.
# WHY WE CHOSE THIS: Security best practice. Hardcoding keys leads to leak riskd and account basn if pushed to GitHub.  
# ==================================================================================
load_dotenv()

# Initialise the Groq software client using the loaded key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ==================================================================================
# STAGE 2: Image Processing (File to Network Payload)
#
# WHAT: Read an image file from disk, convert it to a Base64 string, and prepare it for sending to the Vision API.  
# WHY: APIs operate over HTTP web protocola. Sending standard text bytes encoded as Base64 ensures the image survives web transmission safely.
# ALTERNATIVE: Uploading the image to a public cloud bucket, like AWS S3, and sendind the image URL to the API.
# WHY WE CHOSE THIS: Base64 encoding is simple, fast, and avoids the need for external cloud storage.
# ==================================================================================
def encode_image(image_path):
    """Encode a local image file to a Base64 string for API transmission."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# ==================================================================================
# STAGE 3: Local File Check & Dat Preparation
# 
# WHAT: Confirm the target file exists before making an expensive network call.
# WHY: Prevents unnecessary crash errors if the user forgot to add 'test.jpg'.
# ALTERNATIVE: Letting the scrips fail with a raw Python FileNotFoundError.
# WHY WE CHOSE THIS: Graceful error handling makes debugging easier and improves user experience.
# ==================================================================================  
image_filename = "test.png"

if not os.path.isfile(image_filename):
    print(f"Error: '{image_filename}' not found in the current directory. Please add a test image and rerun.")
else: 
    print(f"'{image_filename}' found. Encoding image to Base64 format...")
    base64_image = encode_image(image_filename)

# ==================================================================================
# STAGE 4: API Request & Multimodal Execution
#
# WHAT: Package both text (the prompt) and image data into an array, sending it to Groq's multimodal vision model.
# WHY: Vision LLMs accept arrays containing both text and image data, allowing for rich concurrent analysis.
# ALTERNATIVE 1: Gemini API (femini-2.0-flash via Google AI Studio).
# ALTERNATIVE 2: OpenAI API (gpt-4o-mini).
# WHY WE CHOSE THIS: Groq's API is fast, cost-effective, and easy to integrate with Python.
# ==================================================================================    
print("Sending request to Groq Vision API...")

completion = client.chat.completions.create(
    # We specift the vision-instruct model capable of reading images
    model = "qwen/qwen3.8-27b", # Ensure current model
    messages = [ 
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe what is in this image and tell me if it appears to be a household chemical or beverage container."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)

# =============================================================
# STAGE 5: Parsing and Displaying the API Response
#
# WHAT: Extract the text response from the API's JSON output and print it to the console.
# WHY: The raw API response contains metadata (tokens used, model version, completion reason). We extract `choice[0].message.content` to get just the generated response text.
# ALTERNATIVE: Printing `completion` raw (outputs messy JSON metadata).
# WHY WE CHOSE THIS: Extracting the specific key gives clean readable text.
# =============================================================
print("\n=== API Response ===")
print(completion.choices[0].message.content)