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
| Audio deepfake / voice-clone detection | 🧪 **Built, not yet live** — real wav2vec2 ML classifier is coded (`backend_ml/`), pending Hugging Face Spaces deployment. Production backend still runs the old file-size heuristic until this is deployed and verified. |
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

## Deploying the Backend (Free)

The frontend is static and lives on the Arush Labs Vercel site. The backend (FastAPI + Tesseract) needs an actual server — Vercel serverless can't install system binaries like `tesseract`, so pick one of these instead:

### Option A — Render.com (good for the current OCR-only backend)

1. Push `backend/` to a GitHub repo (or the `backend/` folder of this repo).
2. On [render.com](https://render.com) → **New → Web Service** → connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Add a `render-build.sh` (or use Render's native Dockerfile support) that also installs `tesseract-ocr` — Render's default Python image doesn't ship it, so either:
   - switch the service type to **Docker** and use a Dockerfile that does `apt-get install -y tesseract-ocr`, or
   - use a `render.yaml`/native buildpack with an `aptfile` if your plan supports it.
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Free tier: 512 MB RAM — fine for OCR + keyword matching, **not enough** once a transformer-based ML model is added (see Option B).
7. Copy the deployed URL and set it in `secureai.html`:
   ```javascript
   const API_BASE = "https://YOUR-BACKEND-URL.onrender.com";
   ```

### Option B — Hugging Face Spaces (needed now that the audio detector uses real ML)

Render's free 512 MB tier will not hold a wav2vec2 / transformer model in memory. Hugging Face Spaces gives a free 16 GB RAM CPU tier (GPU tiers available paid), which is the standard free home for ML-backed FastAPI apps. Use the **`backend_ml/`** folder for this deploy — it already has the ML-upgraded `audio_detector.py`, a matching `requirements.txt` (torch/transformers/librosa), and a `Dockerfile` that pre-downloads the model at build time.

1. Create a new Space → SDK: **Docker**.
2. Push the contents of `backend_ml/` to the Space's git repo (the `Dockerfile` in there is already set up — no manual editing needed).
3. Hugging Face builds and hosts it automatically at `https://YOUR-USERNAME-SPACE-NAME.hf.space`. First build takes longer than the OCR-only backend (~5-8 min) since it installs torch + downloads the ~380MB model — that only happens once, at build time, not per-request.
4. Point `API_BASE` in `secureai.html` at that URL instead of the Render one.
5. Test a real audio upload against `/analyze` and confirm the `audio` field in the response is coming from the model, not the old heuristic (check the Space's logs — the fallback heuristic logs a `[audio_detector] ML inference failed` line if it's ever silently falling back).
6. Only once that's verified live: flip the honesty table on `secureai.html` and in this README from 🧪 to ✅ for audio deepfake detection, and re-enable audio upload in the frontend (`accept="audio/wav,audio/mpeg"` on the file input, currently image-only).

**Recommendation:** keep Render for the OCR-only backend if you want a fast, always-simple fallback. Point production at Hugging Face Spaces once the ML audio detector is verified working — don't try to fit the transformer model into Render's free tier.

## Use Cases

- Pre-screening layer for AI chatbots and LLM-powered interfaces that accept image uploads
- Multimodal AI product pipelines that need an input-validation gate
- Startups shipping AI features fast who want a lightweight, explainable first line of defense
- Enterprise teams evaluating an early-access risk-screening approach before committing to a heavier ML pipeline

## Roadmap — Planned ML Upgrades

Priority order for turning the remaining heuristics into real ML, easiest/highest-impact first:

1. **Audio deepfake / voice-clone detector** — ✅ built. `backend_ml/detectors/audio_detector.py` replaces the file-size heuristic with `MelodyMachine/Deepfake-audio-detection-V2`, a wav2vec2-base model fine-tuned for deepfake/voice-clone classification (Apache-2.0, commercial use permitted, ~95M params, CPU-friendly). Falls back to the old heuristic only if ML inference errors out, so `/analyze` never hard-crashes. **Not yet live** — needs deploying via Hugging Face Spaces (see Deployment below) and verifying before the honesty table flips to ✅.
2. **Transformer-based prompt-injection classifier** — the current OCR pipeline is real, but the risk scoring after OCR is still keyword matching. Replace/augment it with a fine-tuned lightweight text classifier (e.g., a DistilBERT-style model fine-tuned on prompt-injection/jailbreak datasets) so paraphrased attacks that don't match the keyword list still get caught.
3. **Visual deepfake / image-manipulation detector** — add a lightweight CNN classifier (e.g., an EfficientNet-B0 fine-tuned on a public deepfake-detection dataset) alongside OCR, so the image path checks both hidden text *and* whether the image itself has been manipulated.
4. Live streaming audio analysis
5. Video deepfake detection
6. API-based firewall integration for third-party AI systems
7. Enterprise security dashboard with logging & analytics
8. Continuous-learning feedback loop

Each item moves from 🚧 to ✅ in the honesty table (and on `secureai.html`) the same day it actually ships — not before.

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
