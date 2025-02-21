import tanjun
import requests
import os
import json
from typing import Final
import time

from .prompt import get_chat

component = tanjun.Component().load_from_scope()


def get_reponse(id: str, user_prompt: str) -> str:
    OLLAMA_API_URL: Final[str] = os.environ.get("LLM_URL")
    config_path = "bot/config.json"

    chat, chat_history = get_chat(id)

    context = chat + f'\nUser: "{user_prompt}"\nAssistant: '

    chat_history.append({"role": "user", "content": user_prompt})

    with open(os.path.abspath(config_path), "r") as f:
        config = json.load(f)

    config["prompt"] = context

    response = requests.post(OLLAMA_API_URL, json=config)

    if response.status_code != 200:
        raise Exception("LLM not loaded yet")

    data = response.json()
    data["response"] = data["response"].split("</think>")[-1].strip()

    chat_history.append({"role": "assistant", "content": data["response"]})

    return data


@component.with_message_command
@tanjun.as_message_command("text", "txt")
async def text(ctx: tanjun.abc.MessageContext) -> None:
    if ctx.author.is_bot:
        return

    PREFIX: Final[str] = os.environ.get("BOT_PREFIX")
    prompt: str = " ".join(
        ctx.message.content.removeprefix(PREFIX).strip().split(" ")[1:]
    )

    msg = await ctx.respond("Hold on! Wait a minute!...")

    t1 = time.time()
    try:
        data = get_reponse(str(ctx.author.id), prompt)
        response = data["response"]
    except Exception:
        response = "Something went wrong! Try again."

    finally:
        await msg.delete()
        t2 = time.time()
        await ctx.respond(f"> {(t2 - t1):.2f} seconds\n" + response)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component)


@tanjun.as_unloader
def unload(client: tanjun.Client) -> None:
    client.remove_component(component)
