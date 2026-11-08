# 🛡️ SafeChem – AI-Powered Household Chemical Hazard Detector

SafeChem is an intelligent computer vision application designed to identify household chemical containers, assess hazards, and provide immediate safety guidance using multimodal vision models.

## 🧱 Architecture & Design (5-Stage Pipeline)
1. **Stage 1: Environment & Security Setup** – Encapsulates API keys via `.env` and `python-dotenv`.
2. **Stage 2: Local File Processing** – Encodes image inputs to Base64 for HTTP payload packaging.
3. **Stage 3: Pre-flight Verification** – Validates local file existence before issuing API requests.
4. **Stage 4: Multimodal Execution** – Sends concurrent image and prompt context to the Vision model endpoint.
5. **Stage 5: Response Parsing** – Extracts structured insights from the API response payload.

## 🚀 Tech Stack
* **Language:** Python 3.x
* **AI Model:** Multimodal Vision LLM (`qwen/qwen3.8-27b`)
* **Libraries:** `groq`, `python-dotenv`

## 🔧 Setup & Execution

1. Clone the repository:
   ```bash
   git clone [https://github.com/nsindittngcobo-wq/safe-chem-app.git](https://github.com/nsindittngcobo-wq/safe-chem-app.git)
   cd safe-chem-app