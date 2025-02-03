import os
import json
from typing import Final, Any

chat_history: dict[list[dict[str, str]]] = {
    # "234234":
    #     [
    #         {
    #             "role": "User", "content": "How are you?"
    #         },
    #         {
    #             "role": "Hu Tao", "content": "I am fine"
    #         }
    #     ]
}


def get_prompt(id: str) -> tuple[str, list[dict[str, str]]]:
    PROMPT_FILE: Final[str] = "prompt.txt"
    with open(os.path.abspath("bot/" + PROMPT_FILE), "r") as f:
        if id in chat_history.keys():
            full_prompt = (
                f.read()
                + "\n"
                + "\n".join(
                    [
                        f"{chat['role']}: {chat['content']}"
                        for chat in chat_history.get(id)
                    ]
                )
            )
            return full_prompt, chat_history[id]

        chat_history[id] = []
        return f.read(), chat_history[id]
