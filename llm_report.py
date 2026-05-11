import subprocess
from config import Config


class LLMReportGenerator:
    def generate(self, summary, df):
        vehicle_results = df[["vehicle_id", "health_score", "status", "maintenance_recommendation"]].to_string(index=False)

        prompt = f"""
You are an automotive data analyst AI.

Analyze the following vehicle dataset summary and health results.

Dataset summary:
{summary}

Vehicle results:
{vehicle_results}

Provide the report in TWO parts: First in English, then in Turkish.
For both languages, include:
- important technical findings (önemli teknik bulgular)
- risky vehicles (riskli araçlar)
- maintenance suggestions (bakım önerileri)

Keep the report short, clear and technical.
"""

        try:
            config = Config()

            result = subprocess.run(
                ["ollama", "run", config.model_name],
                input=prompt,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace"
            )

            return result.stdout.strip()

        except Exception as e:
            return f"AI report generation failed: {e}"