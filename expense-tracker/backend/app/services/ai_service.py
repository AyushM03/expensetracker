from anthropic import Anthropic
from app.core.config import settings


def get_ai_advice(summary: dict, question: str = None) -> str:
    """
    Takes monthly summary and returns AI financial advice.
    Uses Claude API (Anthropic).
    """
    if not settings.ANTHROPIC_API_KEY:
        return "AI advisor not configured. Add ANTHROPIC_API_KEY to .env"

    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    prompt = f"""
You are a personal finance advisor for a young Indian professional.

Here is their expense summary for {summary['month']}:
- Total spent: ₹{summary['total']:,.0f}
- Number of transactions: {summary['count']}
- Breakdown by category: {summary['by_category']}

{f"User question: {question}" if question else "Give them a brief, practical 3-point analysis of their spending with actionable suggestions to save money."}

Keep your response short, friendly, and specific to their numbers. Use ₹ symbol for amounts.
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
