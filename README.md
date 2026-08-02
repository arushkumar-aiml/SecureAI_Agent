# 🛡️ SecureAI Agent — AI Firewall for Multimodal Threat Detection

> **"Don't secure the AI — secure what reaches the AI."**

SecureAI Agent is a **pre-AI screening layer** — a firewall that sits *in front of* your AI system and inspects every upload before it ever reaches your model. It doesn't try to make the AI smarter. It makes sure the AI never sees the attack in the first place.

Built by **Cyber Guard Nexus** @ Arush Labs.

[![Status](https://img.shields.io/badge/status-early--access-orange)]()
[![Backend](https://img.shields.io/badge/backend-FastAPI-009688)]()
[![License](https://img.shields.io/badge/license-proprietary-lightgrey)]()

---

## The Problem

AI systems trust their inputs by default. That's a liability:

- **Hidden prompt injections in images** — text buried in a picture can silently hijack an LLM's instructions the moment it's processed.
- **Malicious or malformed uploads** — files crafted to break or manipulate a downstream AI pipeline.
- **No screening layer** — most AI products pass user uploads straight to the model with zero risk assessment.

By the time a compromised input reaches your AI, the damage is already done.

## The Solution

```
User Upload → SecureAI Agent → Risk Verdict → AI Model (protected)
```

SecureAI Agent scans every upload, scores its risk, and returns a clear verdict — **SAFE / FLAGGED / BLOCKED** — before the file goes anywhere near your AI system.

---

## What's Actually Real (and what isn't — yet)

We'd rather under-promise than have a customer or a judge open the code and find a gap. Here's the honest breakdown:

| Capability | Status |
|---|---|
| OCR-based hidden-text extraction from images | ✅ **Real, live** — uses Tesseract OCR |
| Prompt-injection phrase matching on extracted text | ✅ **Real, live** |
| File-size / resolution sanity checks | ✅ **Real, live** (basic signal, not deep analysis) |
| Weighted multimodal risk fusion engine | ✅ **Real, live** |
| Audio deepfake / voice-clone detection | 🚧 **Roadmap** — current audio check is a basic file-safety heuristic, not acoustic ML |
| Trained ML-based visual deepfake detection | 🚧 **Roadmap** |

If you need real prompt-injection screening on images today, **this genuinely works.** If you need true audio deepfake detection, that model isn't built yet — we say so, out loud, everywhere this product is shown.

---

## How It Works

1. User uploads an image (or audio file) via the frontend.
2. The **Image Detector** runs real OCR (Tesseract) on the image, extracts any embedded text, and checks it against a list of known prompt-injection phrases ("ignore previous instructions," "jailbreak," "reveal your prompt," etc.). It also runs a lightweight file-size/resolution sanity check.
3. The **Audio Detector** currently runs a basic file-size heuristic (clearly labeled as not deepfake detection — see roadmap above).
4. The **Risk Fusion Engine** combines detector outputs into a single weighted score (0–100) and maps it to a verdict:
   - `< 40` → **SAFE**
   - `40–69` → **FLAGGED**
   - `≥ 70` → **BLOCKED**
5. The verdict is returned instantly to the frontend — before the file goes anywhere near a downstream AI model.

---

## Architecture

```
User Upload (Image / Audio)
        │
        ▼
┌─────────────────────────┐
│      SecureAI Agent     │
│  ┌────────┐ ┌────────┐  │
│  │ Audio  │ │ Image  │  │
│  │Detector│ │Detector│  │   ← OCR + prompt-injection matching
│  └───┬────┘ └───┬────┘  │
│      └────┬─────┘       │
│     ┌─────▼──────┐      │
│     │ Risk Fusion│      │
│     └─────┬──────┘      │
└───────────┼─────────────┘
            ▼
   SAFE / FLAGGED / BLOCKED
            ▼
   AI Model (protected)
```

## Tech Stack

**Backend** — FastAPI · Python · Tesseract OCR (`pytesseract`) · modular detector architecture (`audio_detector.py`, `image_detector.py`, `fusion.py`)

**Frontend** — Streamlit (interactive risk dashboard, live gauge, upload UI)

> **Note on detection approach:** image analysis uses real OCR + phrase matching, which is fast, explainable, and doesn't need a GPU. The architecture is ML-ready — a trained deepfake/audio-classifier model can be dropped into the audio detector without changing the API contract or the fusion pipeline.

## Project Structure

```
SecureAI_Agent/
│
├── backend/
│   ├── detectors/
│   │   ├── audio_detector.py
│   │   ├── image_detector.py
│   │   └── fusion.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/your-username/SecureAI-Agent.git
cd SecureAI-Agent

# Install dependencies
pip install -r requirements.txt

# Tesseract OCR is a system dependency — install it separately:
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract

# Start the backend
cd backend
uvicorn main:app --reload

# Start the frontend (in a new terminal)
cd frontend
streamlit run app.py
```

## Use Cases

- Pre-screening layer for AI chatbots and LLM-powered interfaces that accept image uploads
- Multimodal AI product pipelines that need an input-validation gate
- Startups shipping AI features fast who want a lightweight, explainable first line of defense
- Enterprise teams evaluating an early-access risk-screening approach before committing to a heavier ML pipeline

## Roadmap

- [ ] Trained ML-based audio deepfake / voice-clone detector
- [ ] Trained ML-based visual deepfake detector
- [ ] Live streaming audio analysis
- [ ] Video deepfake detection
- [ ] API-based firewall integration for third-party AI systems
- [ ] Enterprise security dashboard with logging & analytics
- [ ] Continuous-learning feedback loop

## Team — Cyber Guard Nexus

| Name | Role | Contribution |
|---|---|---|
| **Arush Kumar** *(Team Lead)* | Backend & AI Architecture | FastAPI backend, detector modules, overall system design |
| **Adeel Ahmad** | Frontend Developer | Streamlit UI, cybersecurity theme, visual design |
| **Hamza Hasan** | AI & Integration | OCR-based image analysis, risk fusion logic, end-to-end testing |
| **Ayushi Shukla** | Documentation & Demo | Project documentation, demo video, use case research, presentation |

## Conclusion

SecureAI Agent is a working, honestly-labeled first step toward AI input security — not a finished enterprise product, and not pretending to be one. What's live is genuinely live. What isn't is on the roadmap, clearly marked, until it's real.

---

*Built by Cyber Guard Nexus — part of [Arush Labs](https://arushlabs.vercel.app).*
