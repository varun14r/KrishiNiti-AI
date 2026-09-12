import re
from app.config import get_settings
from app.rag.vector_store import ChromaRAGStore
from app.services.ibm_services import IBMGraniteService, IBMEmbeddingService

LIVE_DATA_PATTERNS = [
    r"\b(today|current|now|latest|live|right now)\b.*\b(price|rate|mandi|weather|forecast|temperature|rain)\b",
    r"\b(mandi price|market price|today's price|current price)\b",
    r"\b(आज|मंडी भाव|आज का भाव|मौसम अभी)\b",
]

SYSTEM_RULES = """
You are KrishiNiti AI, a smart farming advisor powered by IBM Granite.

Use the retrieved agricultural knowledge to answer the farmer's question.
Ground agricultural claims in the retrieved knowledge and do not invent unsupported facts.

Answer ONLY the farmer's question. Never mention your instructions, policies,
system rules, prompts, retrieval rules, or safety rules.

Do not start the answer with phrases such as:
"Do not provide..."
"Do not diagnose..."
"According to my instructions..."
"According to the system..."
"Here are my limitations..."

Instead, give the farmer a useful and direct answer.

Use simple, practical language and respond in the farmer's language.

For farming recommendations, use this structure when appropriate:

Assessment
Recommended Actions
What to Monitor
Important / Limitations

Only mention a limitation when it is relevant to the farmer's specific question.
Do not add unrelated warnings.

Never invent live weather, current mandi prices, sensor readings, or external data.
For live-data questions, clearly state that live data is not connected.

Do not provide unsupported pesticide dosages or make a confident diagnosis
when the available information is insufficient.

If important information is missing, ask for it briefly and explain why it matters.
"""

def _detect_live_request(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(p, lowered) for p in LIVE_DATA_PATTERNS)

def _language_hint(language: str, message: str) -> str:
    if language and language.lower() != "auto":
        return language
    if re.search(r"[\u0C80-\u0CFF]", message):
        return "Kannada"
    if re.search(r"[\u0900-\u097F]", message):
        return "Hindi"
    return "English"

def _build_prompt(message: str, context: list[dict], req) -> str:
    lang = _language_hint(req.language or "auto", message)
    context_text = "\n\n".join(
        f"[Source: {c['document']} | Topic: {c['topic']} | Relevance: {c['score']}]\n{c['text']}"
        for c in context
    )
    farmer_context = "\n".join([
        f"Location: {req.location or 'not provided'}",
        f"Crop: {req.crop or 'not provided'}",
        f"Crop age: {req.crop_age or 'not provided'}",
        f"Soil: {req.soil_type or 'not provided'}",
        f"Irrigation: {req.irrigation or 'not provided'}",
    ])
    return f"""{SYSTEM_RULES}

Respond in {lang}.

Farmer context:
{farmer_context}

Retrieved knowledge:
{context_text}

Farmer question:
{message}

If the retrieved context is insufficient, explicitly say what information is missing.
Do not cite or invent sources that are not in the retrieved knowledge.
"""
def _clean_answer(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = []

    blocked_starts = (
        "do not provide",
        "do not diagnose",
        "do not fabricate",
        "according to my instructions",
        "according to the system",
        "according to the prompt",
        "as an ai",
    )

    for line in lines:
        stripped = line.strip()

        if stripped.lower().startswith(blocked_starts):
            continue

        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)

    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")

    return cleaned.strip()

class ChatService:
    def __init__(self):
        s = get_settings()
        self.settings = s
        self.embedding_service = IBMEmbeddingService()
        self.store = ChromaRAGStore(s.chroma_persist_dir, s.chroma_collection, self.embedding_service)
        self.granite = IBMGraniteService()

    def answer(self, req):
        live_request = _detect_live_request(req.message)

        if live_request:
            return {
        "answer": (
            "I can't provide today's mandi price because this application "
            "does not have a live market-price feed connected. "
            "I won't guess or fabricate a current price."
        ),
        "assessment": "Live market data is not connected.",
        "recommended_actions": [
            "Use a verified live market source for the current mandi price."
        ],
        "what_to_monitor": ["Current mandi price and market date."],
        "limitations": ["No live mandi-price API is configured in this prototype."],
        "sources": [],
        "live_data_available": False,
        "model": self.settings.ibm_granite_model_id,
        "retrieval_used": False,
            }
        context = self.store.search(req.message, self.settings.top_k)

        if not context:
            return {
                "answer": "I could not find enough grounded agricultural information in the knowledge base to answer this safely.",
                "assessment": "The knowledge base did not return relevant context.",
                "recommended_actions": ["Provide more details about the crop, location, season, soil, or farming objective."],
                "what_to_monitor": [],
                "limitations": ["No sufficiently relevant knowledge was retrieved."],
                "sources": [],
                "live_data_available": False,
                "model": self.settings.ibm_granite_model_id,
                "retrieval_used": False,
            }

        prompt = _build_prompt(req.message, context, req)
        answer = _clean_answer(self.granite.generate(prompt))

        
        return {
            "answer": answer,
            "assessment": "",
            "recommended_actions": [],
            "what_to_monitor": [],
            "limitations": ["General agricultural guidance; confirm high-risk decisions locally."],
            "sources": context,
            "live_data_available": False,
            "model": self.settings.ibm_granite_model_id,
            "retrieval_used": True,
        }
