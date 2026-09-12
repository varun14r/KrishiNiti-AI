# KrishiNiti AI

**AI-Powered Smart Farming Assistant**

KrishiNiti AI is a full-stack Retrieval-Augmented Generation (RAG) application for agricultural guidance. It uses a curated agricultural knowledge base, IBM Granite multilingual embeddings, ChromaDB semantic retrieval, and IBM Granite (`ibm/granite-4-h-small`) through IBM watsonx.ai.

## Architecture

Farmer Web App → React/TypeScript → FastAPI → ChatService → RAG Retrieval → ChromaDB → Retrieved Context → Prompt Builder → IBM Granite → Structured Farming Guidance.

Knowledge ingestion:

Agricultural knowledge → chunking → `ibm/granite-embedding-278m-multilingual` → ChromaDB.

## Features

- Crop and seasonal planning
- Soil and nutrient management
- Irrigation and water management
- Integrated Pest Management
- Safe crop-problem guidance
- Weather-aware farming guidance
- Market/mandi information with no fabricated live prices
- English, Kannada and Hindi interaction
- Retrieved knowledge/source visibility
- Responsive farmer-focused web UI

## Requirements

- Python 3.11+
- Node.js 18+
- IBM watsonx.ai project with access to IBM Granite
- IBM Cloud API key and watsonx project ID

## Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` at the repository root and fill in your own IBM credentials. Never commit `.env`.

Ingest the knowledge base:

```bash
python scripts/ingest_knowledge_base.py
```

Start the API:

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Demonstration questions

- What crop is suitable for this season in Karnataka?
- How can I reduce water use in vegetable cultivation?
- What information do you need before recommending fertilizer?
- What is today's mandi price of tomatoes in Karnataka?
- ಕರ್ನಾಟಕದಲ್ಲಿ ಈ ಋತುವಿನಲ್ಲಿ ಯಾವ ಬೆಳೆ ಬೆಳೆಯುವುದು ಸೂಕ್ತ?
- आज टमाटर की खेती के लिए क्या सावधानियां रखनी चाहिए?

The application must not invent current mandi prices or current weather when no live data source is connected.

## Testing

```bash
cd backend
pytest -q
```

## Limitations

The included knowledge base is general agricultural reference material. It is not a substitute for local agricultural officers, agronomists, soil laboratories, or qualified experts. Live weather and mandi feeds are intentionally not fabricated.

## Future scope

Live weather, live mandi prices, voice interaction, IoT/soil monitoring, image-based crop disease assistance, personalized farm profiles, and a mobile application.
