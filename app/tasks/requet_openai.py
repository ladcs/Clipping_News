from openai import OpenAI
from enum import Enum
from core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

class TaskType(str, Enum):
    CLASSIFICATION = "classification"
    SUMMARY = "summary"

def request_openai(
    prompt: str,
    task: TaskType = TaskType.CLASSIFICATION,  # "classification" | "summary"
) -> str:
    if task == TaskType.CLASSIFICATION:
        args = {
            "input": prompt,
            "model": "gpt-4.1-nano",
            "max_output_tokens": 16,
            "temperature": 0.1,
        }
    elif task == TaskType.SUMMARY:
        args = {
            "model": "gpt-5-nano",
            "input": prompt,
            "max_output_tokens": 700,
            "reasoning": {
                "effort": "low"
            }
        }
    else:
        raise ValueError(f"Invalid task type {task}")

    response = client.responses.create(**args)
    return response.output_text.strip()
