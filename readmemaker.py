from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

with open("readmemaker.md", "r") as f:
    prompt = f.read()

def make_readme(content: str) -> str:
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}

    )
    return response.choices[0].message.content