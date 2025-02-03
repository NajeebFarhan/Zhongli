import os
import json
from typing import Final, Any

prompts: dict[str, dict[str, Any]] = {
    # "234234":
    #     {
    #         "model": "llm model",
    #         "messages": [
    #             {
    #                 "role": "user", "content": "be a nice assistant"
    #             }
    #         ],
    #         "stream": False
    #     }
}


def get_prompt(id: str) -> dict[str, dict[str, Any]]:
    if id in prompts.keys():
        return prompts[id]

    else:
        prompt = create_prompt()

        prompts[id] = prompt
        prompts[id]["model"] = os.environ.get("LLM")

        return prompts[id]


def create_prompt() -> dict[str, dict[str, Any]]:
    PROMPT_FILE: Final[str] = "prompt.json"

    with open(os.path.abspath("bot/" + PROMPT_FILE), "r") as f:
        prompt: dict[str, dict[str, Any]] = json.load(f)

    return prompt
