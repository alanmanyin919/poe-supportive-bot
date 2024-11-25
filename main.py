"""

Sample bot that shows the query sent to the bot.

"""

from __future__ import annotations
import os
from typing import AsyncIterable

import fastapi_poe as fp
from devtools import PrettyFormat
from modal import App, Image, asgi_app, Secret
from open_ai.emotional_support_bot import EmotionalSupportBot
import logging

pformat = PrettyFormat(width=85)


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# class SupportiveBot(fp.PoeBot):
#     async def get_response(
#         self, request: fp.QueryRequest
#     ) -> AsyncIterable[fp.PartialResponse]:
#         yield fp.PartialResponse(text="```python\n" + pformat(request) + "\n```")

class SupportiveBot(fp.PoeBot):

    async def get_response(self, request: fp.QueryRequest) -> AsyncIterable[fp.PartialResponse]:
        logging.info("creating supportive bot training...")
        last_message = request.query[-1].content
        emotional_supportive_bot = EmotionalSupportBot()
        assistant_response = emotional_supportive_bot.get_response(last_message)
        yield fp.PartialResponse(text=assistant_response)

    # async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
    #     # Declare dependencies and additional AI models if required
    #     return fp.SettingsResponse(
    #         server_bot_dependencies={"GPT-4-Turbo": 1}  # Declare the AI model provided by Poe
    #     )



REQUIREMENTS = ["fastapi-poe==0.0.48", "devtools", "openai"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
app = App("supportive-bot-poe")


@app.function(image=image, secrets=[Secret.from_name("custom_secret")])
@asgi_app()
def fastapi_app():
    bot = SupportiveBot()
    app = fp.make_app(bot, access_key=os.environ["POE_ACCESS_KEY"], bot_name=os.environ["POE_BOT_NAME"])
    return app



