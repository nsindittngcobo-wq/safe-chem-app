# 🛡️ SafeChem – AI-Powered Household Chemical Hazard Detector

SafeChem is an intelligent computer vision application designed to identify household chemical containers, assess hazards, and provide immediate safety guidance using multimodal vision models.

🌐 **Live Production App:** [View SafeChem on Streamlit Community Cloud](https://safe-chem-app.streamlit.app/)


## ✨ Key Features & Capabilities
* **📸 Live Camera Capture & Vision Analysis:** Seamlessly switch between snapping a live photo directly from a mobile/desktop camera (`st.camera_input`) or uploading an image file of any container label.
* **🔎 Dynamic AI Text Search:** Type any open-ended chemical or product name to instantly generate a comprehensive AI safety profile without needing a static database.
* **⚠️ Automated Risk Severity Banners:** Dynamically parses model outputs to render clear, color-coded visual alerts (`HIGH`, `MEDIUM`, or `LOW` risk) for immediate hazard recognition.
* **📱 Fully Responsive Mobile-First Design:** Optimized out-of-the-box for mobile browsers, allowing users to scan product bottles in real-time straight from their phones.

## 🧱 Architecture & Design (5-Stage Pipeline)
1. **Stage 1: Environment & Security Setup** – Encapsulates API keys via `.env` and `python-dotenv`.
2. **Stage 2: Local File Processing** – Encodes image inputs to Base64 for HTTP payload packaging.
3. **Stage 3: Pre-flight Verification** – Validates local file existence before issuing API requests.
4. **Stage 4: Multimodal Execution** – Sends concurrent image and prompt context to the Vision model endpoint.
5. **Stage 5: Response Parsing** – Extracts structured insights from the API response payload.

## 🚀 Tech Stack
* **Language:** Python 3.x
* **Framework:** [Streamlit](https://streamlit.io/)
* **AI Model:** Multimodal Vision LLM (`qwen/qwen3.8-27b`) via [Groq API](https://groq.com/)
* **Libraries:** `groq`, `python-dotenv`, `pillow`, `streamlit`
* **Version Control:** Git & GitHub

## ⚠️ Known Limitations & Disclaimers
1. **AI Hallucination Risk:** Large Language Models can occasionally misidentify rare chemical brands or ambiguous labels. **SafeChem is not a certified medical or toxicological advisory tool.**
2. **First-Aid Limitations:** Emergency guidance is for general informational purposes only and must never supersede official medical advice or instructions from a local poison control center.
3. **Free Tier & Rate Limits:** Because the app runs on free developer tiers, heavy concurrent traffic can temporarily trigger API rate limits (TPM thresholds).
4. **Visual Obstructions:** Vision analysis depends entirely on image clarity, lighting, and label legibility.

## 🔧 Setup & Execution
1. Clone the repository:
   ```bash
   git clone [SafeChem Repository](https://github.com/nsindittngcobo-wq/safe-chem-app.git)
   cd safe-chem-app