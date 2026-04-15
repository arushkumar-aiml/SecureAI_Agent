# SecureAI_Agent — AI Firewall for Multimodal Threat Detection

> **"Don't secure the AI — secure what reaches the AI."**

SecureAI_Agent is an AI-powered security layer that acts like a firewall for AI systems, protecting them from deepfake audio attacks, hidden prompt injection inside images, and multimodal threats — **before** the input reaches the AI model.

Modern AI systems blindly trust user inputs. SecureAI_Agent introduces a pre-processing security gate that scans, analyzes, and risk-scores inputs in real time.

---

## Problem Statement

AI systems today are vulnerable to:

* Deepfake and cloned voice attacks
* Hidden malicious text inside images (OCR prompt injection)
* Multimodal attacks combining audio + visual manipulation

Once such inputs reach an AI model, the damage is already done.

---

## Solution Overview

SecureAI_Agent works as a **pre-AI firewall**:

```
Input → SecureAI_Agent → AI Model
```

Before any file reaches the AI system, SecureAI_Agent:

* Analyzes audio for deepfake patterns
* Extracts hidden text from images using OCR
* Performs semantic risk analysis
* Generates a final risk decision: `SAFE` / `SUSPICIOUS` / `BLOCKED`

---

## Key Features

| Feature                        | Description                                  |
| ------------------------------ | -------------------------------------------- |
| Audio Deepfake Detection       | Heuristic-based analysis of audio patterns   |
| OCR Prompt Injection Detection | Extracts and scans hidden text from images   |
| Multimodal Risk Fusion Engine  | Combines scores from all detectors           |
| Fast & Lightweight             | Real-time analysis with no heavy ML overhead |
| AI Firewall Architecture       | Acts as a security gate before the AI model  |
| Real-time File Scanning        | Instant risk verdict on every upload         |

---

## System Architecture

```
User Upload (Audio / Image)
        ↓
┌─────────────────────────┐
│     SecureAI_Agent      │
│  ┌────────┐ ┌────────┐  │
│  │ Audio  │ │ Image  │  │
│  │Detector│ │Detector│  │
│  └───┬────┘ └───┬────┘  │
│      └────┬─────┘       │
│     ┌─────▼──────┐      │
│     │ Risk Fusion│      │
│     └─────┬──────┘      │
└───────────┼─────────────┘
            ↓
   SAFE / SUSPICIOUS / BLOCKED
            ↓
       AI Model (Protected)
```

---

## Tech Stack

### Backend

* FastAPI — REST API layer
* Python — Core logic
* Modular Detector Architecture — `audio.py`, `image.py`, `fusion.py`

### Frontend

* Streamlit — Interactive UI
* Custom cybersecurity theme

### AI Components

* Heuristic-based Audio Risk Detection
* OCR-based Image Analysis
* Risk Fusion Logic

> **Note on Detection Approach:** This project uses lightweight heuristic-based risk analysis for fast and stable real-time detection. The architecture is ML-ready — advanced PyTorch-based deepfake models can be integrated in future versions without changing the pipeline.

---

## Project Structure

```
SecureAI-Agent/
│
├── backend/
│   ├── detectors/
│   │   ├── audio.py
│   │   ├── image.py
│   │   └── fusion.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── bg.png
├── requirements.txt
└── README.md
```

---

## Demo Video

Watch Demo on Google Drive:
[https://drive.google.com/file/d/1u7k9hQp7qG69NiPw6Wmo3CWeiq0koU4x/view?usp=drive_link](https://drive.google.com/file/d/1u7k9hQp7qG69NiPw6Wmo3CWeiq0koU4x/view?usp=drive_link)

### How It Works (Demo Flow)

1. Upload an audio or image file
2. SecureAI_Agent scans the file
3. Risk level is displayed instantly
4. File verdict:

   * SAFE — Allowed through to the AI model
   * SUSPICIOUS — Flagged for review
   * BLOCKED — High risk, rejected

---

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/your-username/SecureAI-Agent.git
cd SecureAI-Agent

# Install dependencies
pip install -r requirements.txt

# Start the backend
cd backend
uvicorn main:app --reload

# Start the frontend (in a new terminal)
cd frontend
streamlit run app.py
```

---

## Use Cases

* Voice assistants & smart speakers
* AI chatbots & LLM interfaces
* Multimodal AI systems
* Enterprise AI security pipelines
* AI input validation layers

---

## Future Enhancements

* Live streaming audio analysis
* Video deepfake detection
* API-based firewall integration for third-party AI systems
* Enterprise security dashboard
* Continuous learning models with feedback loop

---

## Team — Cyber Guard Nexus

| Name                          | Role                      | Contribution                                                                                   |
| ----------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------- |
| **Arush Kumar** *(Team Lead)* | Backend & AI Architecture | FastAPI backend, detector modules (`audio.py`, `image.py`, `fusion.py`), overall system design |
| **Adeel Ahmad**               | Frontend Developer        | Streamlit UI, cybersecurity theme, visual design                                               |
| **Hamza Hasan**               | AI & Integration          | OCR-based image analysis, risk fusion logic, end-to-end testing                                |
| **Ayushi Shukla**             | Documentation & Demo      | Project documentation, demo video, use case research, presentation                             |

---

## Conclusion

SecureAI_Agent introduces a new security layer for AI systems, ensuring that malicious inputs never reach the AI model. It is fast, modular, scalable, and designed for real-world AI security challenges.

---

