import tanjun
import requests
import os
from typing import Final
import time

from .prompt import get_prompt

component = tanjun.Component().load_from_scope()


def get_reponse(id: str, user_prompt: str) -> str:
    OLLAMA_API_URL: Final[str] = os.environ.get("LLM_URL")

    prompt = get_prompt(id)

    user_message = {"role": "user", "content": user_prompt}
    prompt["messages"].append(user_message)

    prompt["prompt"] = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in prompt["messages"]]
    )

    response = requests.post(OLLAMA_API_URL, json=prompt)

    if response.status_code != 200:
        raise Exception("LLM not loaded yet")

    data = response.json()
    data["response"] = data["response"].split("</think>")[-1].strip()

    assistant_message = {"role": "assistant", "content": data["response"]}
    prompt["messages"].append(assistant_message)

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
    data = get_reponse(str(ctx.author.id), prompt)
    t2 = time.time()

    await msg.delete()
    await ctx.edit(f"> {(t2 - t1):.2f} seconds\n" + data["response"])


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component)


@tanjun.as_unloader
def unload(client: tanjun.Client) -> None:
    client.remove_component(component)
