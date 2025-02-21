import os
from typing import Final

chat_history: dict[str, list[dict[str, str]]] = {
    # "234234":
    #     [
    #         {
    #             "role": "User", "content": "How are you?"
    #         },
    #         {
    #             "role": "Hu Tao(You)", "content": "I am fine"
    #         }
    #     ]
}


def get_chat(id: str) -> tuple[str, list[dict[str, str]]]:
    PROMPT_FILE: Final[str] = "bot/prompt.txt"
    with open(os.path.abspath(PROMPT_FILE), "r") as f:
        if id in chat_history.keys():
            context = (
                f.read()
                + "\n\n"
                + "\n".join(
                    [
                        f"{chat['role'].capitalize()}: \"{chat['content']}\""
                        for chat in chat_history[id]
                    ]
                )
                + "\n"
            )
            return context, chat_history[id]

        chat_history[id] = []
        return f.read(), chat_history[id]
