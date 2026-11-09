# ==========================================
# SAFECHEM - WEB APPLICATION (UI & MULTIMODAL INTEGRATIN)
#
# GOAL: Provide a clean, user-friendly web interface for uploading household chemical containers and viewing real-time AI hazard assessments. 
#
# ARCHITECTURAL RATIONALE & TRADE-OFFS (Interview Prep Notes):
# 1. Framework Choice (Streamlit): Chosen over Flask/FastAPI + React to maximize 
#    speed-to-MVP for an AI portfolio project. It eliminates boilerplate HTML/CSS/JS,
#    allowing focus entirely on core multimodal vision logic while keeping code in pure Python.
# 2. File Handling (In-Memory Buffer): Utilizes `.getvalue()` instead of writing files to local disk. This keeps the application stateless, secure, and performant by avoiding unnecessary disk I/O and server storage cleanups.
# ==========================================

import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# =============================================
# STAGE 1: Security & Session Initialization
#
# WHAT: Load environment variables and set up the page layout.
# WHY: Keeps API keys safe while configuring Streamlit page data.
# =============================================
load_dotenv()

st.set_page_config(
    page_title="SafeChem - Household Chemical Hazard Detector",
    page_icon="🛡️",
    layout="centered"
)

# Initialise Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Helper function to encode user-uploaded bytes to Base64
def encode_uploaded_file(uploaded_file):
    """Convert an in-memory uploaded file buffer into a Base64 string."""
    bytes_data = uploaded_file.getvalue()
    return base64.b64encode(bytes_data).decode("utf-8")

# =============================================
# STAGE 2: User Interface (UI) Header & Multi-Tab Layout
#
# WHAT: Render interactive titles, descriptions, a file drag-and-drop widget, and a search text box.
# WHY: Replaces hardcoded local files (like 'test.png') with a dynamic user interface.
# ============================================
st.title("🛡️ SafeChem - Household Chemical Hazard Detector")
st.write(
    "Your intelligent assistant for household chemical hazard identification, "
    "safety precautions, and emergency first-aid."
)

# Let's do two clean tabs for Vision vs Text Search
tab1, tab2 = st.tabs(["📸 AI Vision Scan", "🔎 Dynamic Text Search"])

with tab1:
    st.header("Container Vision Analysis")
    st.write("Upload an image of a household product or container to analyse potential hazards.")
    
    uploaded_file = st.file_uploader(
     "Choose an image...",
     type = ["png", "jpg", "jpeg", "webp"],
     key ="vision upload"
     )

# =========================================
# STAGE 3: Image Preview & Multimodal Analysis Execution
# 
# WHAT: Display the image on screen and trigger the vision API upon button click.
# WHY: Ensures user consent before making API requests, preventing unintended token usage.
# =========================================
    if uploaded_file is not None:
        #Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Container", use_column_width=True)

        if st.button("🔍 Analyse Hazard", type="primary"):
            with st.spinner("Analysing container with AI Vision..."):
                try:
                    # Encode file buffer to Base64
                    base64_image = encode_uploaded_file(uploaded_file)

                    # Executive API Call
                    completion = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        max_tokens= 600, # Limits the response length to prevent TPM rate limits
                        messages=[
                            {
                                "role": "system",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": (
                                            "You are an expert chemical safety and hazard analysis assistant. "
                                            "Start your response with a line stating the RISK LEVEL formatted exactly as one of: "
                                            "'[RISK: HIGH]', '[RISK: MEDIUM]', or '[RISK: LOW]'. "
                                            "Always provide a concise, clear and direct analysis of household containers, "
                                            "identifying the product type, potential toxicities, handling precautions,"
                                            "and focus mostly on emergency first-aid measures. Never reply with single-letter answers."
                                        )
                                    }
                                ]
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": (
                                            "Analyze this image in detail. Provide: \n"
                                            "1. Identification of the item/chemical.\n"
                                            "2. Classification (Household chemical, food, beverage, etc.).\n"
                                            "3. Potential health or safety hazards.\n"
                                            "4. Recommended safety precautions.\n"
                                            "5. Emergency first-aid measures."
                                        )
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

                    full_response = completion.choices[0].message.content

# ================================
# STAGE 4: Displaying Formatted Analysis Results
# 
# WHAT: Render the response text in a formatted Streamlit container.
# WHY: Replaces plain text print() calls with a stuctured web display.
# ================================
                    st.success("Analysis Complete!")
                    st.subheader("Hazard Assessment & Safety Guidance")

                    # Convert response to uppercase for easier matching
                    response_upper = full_response.upper()

                    # Check for risk levels flexibility (handles bolding)
                    if "HIGH" in response_upper and "RISK" in response_upper and ("HIGH" in response_upper.split("RISK")[0] or "HIGH" in response_upper.split("RISK")[1][:10]):
                        # Fallback cleaner check
                        pass 

                    # Robust risk parsing using flexible string checks
                    if "[RISK: HIGH]" in full_response or "**[RISK: HIGH]**" in full_response or "RISK LEVEL: HIGH" in response_upper:
                        st.error("⚠️ HIGH RISK DETECTED: Hazardous/Toxic Substance")
                    elif "[RISK: MEDIUM]" in full_response or "**[RISK: MEDIUM]**" in full_response or "RISK LEVEL: MEDIUM" in response_upper:
                        st.warning("⚡ MODERATE RISK DETECTED: Exercise Caution & Read Precautions")
                    elif "[RISK: LOW]" in full_response or "**[RISK: LOW]**" in full_response or "RISK LEVEL: LOW" in response_upper:
                        st.info("✅ LOW RISK DETECTED: Standard Handling Precautions Apply")
                    else:
                        # Default fallback banner if the model missed the tag entirely
                        st.info("ℹ️ Risk Level Not Explicitly Detected: Review Full Analysis Below")

                    # Clean uo the response by removing the risk tags before display
                    cleaned_response = (
                        full_response
                        .replace("[RISK: HIGH]", "")
                    .replace("[RISK: MEDIUM]", "")
                    .replace("[RISK: LOW]", "")
                    .replace("**[RISK: HIGH]**", "")
                    .replace("**[RISK: MEDIUM]**", "") 
                    .replace("**[RISK: LOW]**", "")
                    )

                    # Render full textual analysis below the visual alerts
                    st.write(cleaned_response)

                    # Debug expander: Allows us to inspect the raw model output if formatting acts up
                    with st.expander("View Raw Model Output"):
                        st.code(full_response)

                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")


# ====================================================================================
# TAB 2: Dynamic AI Text Search (Groq LLM Lookup)
# ====================================================================================
with tab2:
    # =============================================
    # STAGE 2 (Tab 2): Text Search Header & Input
    # 
    # WHAT: Render a text input field for open-ended product and chemical queries.
    # WHY: Removes the restriction of a static dictionary, allowing users to look up 
    #      any chemical or product dynamically.
    # =============================================
    st.header("Chemical & Product Safety Lookup")
    st.write("Type any household product or chemical name to instantly generate a safety profile using AI.")

    search_query = st.text_input("Enter chemical or product name:", placeholder="e.g. hydrogen peroxide, dishwashing liquid, caustic soda", key="text_search_input").strip()

    # =============================================
    # STAGE 3 (Tab 2): Text Analysis Execution
    # 
    # WHAT: Trigger the Groq text completion API when the user clicks search.
    # WHY: Ensures user intent is explicitly captured before consuming API tokens.
    # =============================================
    if search_query:
        if st.button("🔎 Search Safety Profile", type="primary"):
            with st.spinner(f"Generating safety profile for '{search_query}'..."):
                try:
                    text_completion = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        max_tokens=600,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an expert chemical safety assistant. Start your response with a line "
                                    "stating the RISK LEVEL formatted exactly as one of: '[RISK: HIGH]', '[RISK: MEDIUM]', or '[RISK: LOW]'. "
                                    "Provide a concise, clear, and direct safety profile covering: 1. Identification 2. Classification 3. Hazards 4. Precautions 5. Emergency first-aid."
                                )
                            },
                            {
                                "role": "user",
                                "content": f"Provide a complete chemical safety and hazard analysis for: {search_query}"
                            }
                        ]
                    )

                    text_response = text_completion.choices[0].message.content

# ================================================================
# STAGE 4 (Tab 2): Displaying Formatted Text Results & Severity Banners
# 
# WHAT: Parse risk tags, render color-coded alerts, and clean the text output.
# WHY: Delivers a uniform visual experience matching the Vision Scan tab.
# ================================================================
                    st.success("Lookup Complete!")
                    st.subheader(f"Safety Profile: {search_query.title()}")

                    resp_upper = text_response.upper()

                    # Render Visual Severity Banners dynamically
                    if "[RISK: HIGH]" in text_response or "**[RISK: HIGH]**" in text_response or "RISK LEVEL: HIGH" in resp_upper:
                        st.error("⚠️ HIGH RISK DETECTED: Hazardous/Toxic Substance")
                    elif "[RISK: MEDIUM]" in text_response or "**[RISK: MEDIUM]**" in text_response or "RISK LEVEL: MEDIUM" in resp_upper:
                        st.warning("⚡ MODERATE RISK DETECTED: Exercise Caution & Read Precautions")
                    elif "[RISK: LOW]" in text_response or "**[RISK: LOW]**" in text_response or "RISK LEVEL: LOW" in resp_upper:
                        st.info("✅ LOW RISK DETECTED: Standard Handling Precautions Apply")
                    else:
                        st.info("ℹ️ Risk Level Not Explicitly Detected: Review Full Analysis Below")

                    cleaned_text_response = (
                        text_response
                        .replace("[RISK: HIGH]", "")
                        .replace("[RISK: MEDIUM]", "")
                        .replace("[RISK: LOW]", "")
                        .replace("**[RISK: HIGH]**", "")
                        .replace("**[RISK: MEDIUM]**", "")
                        .replace("**[RISK: LOW]**", "")
                    )

                    st.write(cleaned_text_response)

                    # Debug expander to inspect raw model output
                    with st.expander("View Raw Model Output"):
                        st.code(text_response)

                except Exception as e:
                    st.error(f"An error occurred during search: {str(e)}")