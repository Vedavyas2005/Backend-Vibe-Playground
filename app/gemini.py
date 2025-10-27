import os
import httpx

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

async def generate_code(prompt: str) -> str:
    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    json_data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(GEMINI_API_URL, headers=headers, json=json_data)

    response.raise_for_status()
    data = response.json()
    # Extract generated text from response candidates
    candidates = data.get("candidates", [])
    if not candidates:
        return ""

    text_parts = candidates[0].get("content", {}).get("parts", [])
    # Join all text parts into a single string
    generated_text = "".join(part.get("text", "") for part in text_parts)
    return generated_text
