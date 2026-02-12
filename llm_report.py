import subprocess


def generate_llm_report(summary):

    prompt = f"""
You are an automotive data analyst AI.

Analyze the vehicle dataset summary and provide insights.

Dataset summary:
{summary}

Give:
- potential risks
- abnormal patterns
- maintenance suggestions
Keep it short and technical.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "gemma3:4b"],
            input=prompt,
            text=True,
            capture_output=True
        )

        return result.stdout

    except Exception as e:
        return f"AI report generation failed: {e}"
