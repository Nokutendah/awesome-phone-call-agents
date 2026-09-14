import json
import re
from typing import Dict, Any, List
from google import genai
from google.genai import types
from app.config import get_settings
from app.models.investigation import InvestigationStatus

settings = get_settings()

SYSTEM_PLANNER_PROMPT = """
You are an expert AI mission planner for CallBot Detective, an autonomous AI phone investigator.
Your job is to analyze a natural-language mission from a user who wants an AI agent to call a business or customer service line to gather information.

Rules & Safety Guidelines:
1. Strictly information gathering ONLY.
2. No financial purchases, credit card sharing, binding commitments, or legal agreements.
3. Identify the target business name, target phone number (if mentioned or inferable), and the specific questions the AI call bot should ask.
4. Assess target_confidence ("high", "medium", "low"). If the phone number or business target is missing or ambiguous, target_confidence must be "low" or "medium".

QUESTION EXTRACTION RULES:
5. Every distinct piece of information requested by the user MUST become its own separate planned question.
6. NEVER combine multiple requested questions or topics into one question.
7. Preserve the user's intended meaning when converting requests into natural spoken questions.
8. If the user requests multiple topics joined by "and", split them into separate questions when each topic could be answered independently.
9. If one question naturally asks a follow-up about the answer to a previous question, keep it as a separate question.
10. Do not invent additional questions that the user did not request.
11. Keep each question concise and suitable for a natural phone conversation.
12. Return questions in the same logical order as the user's mission.

EXAMPLE:
If the mission asks:
"Ask how they are doing today, what they enjoy doing in their free time, what they usually talk about with friends, and whether there is anything else they would like to tell me."

The planned_questions MUST be:
[
  "How are you doing today?",
  "What is one thing you enjoy doing in your free time?",
  "What do you usually talk about with your friends?",
  "Is there anything else you'd like to tell me?"
]

Return JSON ONLY matching this exact schema:
{
  "target_name": "Name of business or null",
  "phone_number": "Phone number string or null",
  "planned_questions": ["Question 1", "Question 2"],
  "target_confidence": "high|medium|low"
}
"""

def heuristic_plan_mission(mission: str) -> Dict[str, Any]:
    """Fallback planner using regex/heuristics if API key is not supplied or fails."""

    phone_match = re.search(
        r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        mission
    )
    phone_number = phone_match.group(0) if phone_match else None

    target_name = None

    call_match = re.search(
        r'(?:call|contact|reach)\s+([A-Z0-9][A-Za-z0-9\s\'\&]+?)(?:\s+at|\s+and|\s+to|\s+if|\.|$)',
        mission,
        re.IGNORECASE
    )

    if call_match:
        target_name = call_match.group(1).strip()

    questions = []

    if "ask" in mission.lower():
        ask_part = re.split(
            r'\bask\b',
            mission,
            flags=re.IGNORECASE
        )[-1].strip()

        parts = [
            p.strip()
            for p in re.split(r'\band\b|\.|\?', ask_part)
            if p.strip()
        ]

        for p in parts:
            p_clean = p.strip()

            if not p_clean:
                continue

            if not p_clean.lower().startswith(
                ("if ", "whether ", "what ", "how ", "can ", "do ", "is ", "are ")
            ):
                q = f"Ask {p_clean}?"
            else:
                q = p_clean[0].upper() + p_clean[1:]

                if not q.endswith("?"):
                    q += "?"

            questions.append(q)

    if not questions:
        questions = [
            f"Inquiry regarding: {mission[:50]}?",
            "What are your standard business operating hours?"
        ]

    confidence = (
        "high"
        if target_name and phone_number
        else "medium"
        if target_name
        else "low"
    )

    return {
        "target_name": target_name or "Target Business",
        "phone_number": phone_number,
        "planned_questions": questions,
        "target_confidence": confidence
    }

def plan_mission(mission: str) -> Dict[str, Any]:
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return heuristic_plan_mission(mission)

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"{SYSTEM_PLANNER_PROMPT}\n\nUser Mission: {mission}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(f"[Planner Warning] Gemini API call failed or unconfigured, using heuristic: {e}")
        return heuristic_plan_mission(mission)
