# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ Codrago, 2024-2025
# This file is a part of Heroku Userbot
# 🌐 https://github.com/coddrago/Heroku
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import logging
import os
import random

import herokutl
from herokutl.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from herokutl.tl.types import Message
from herokutl.utils import get_display_name

from .. import loader, log, main, utils
from .._internal import fw_protect, restart
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

@loader.tds
class HerokuWebMod(loader.Module):
    """Web mode add account"""

    strings = {"name": "HerokuWeb"}

    @loader.command()
    async def weburl(self, message: Message, force: bool = False):
        if "LAVHOST" in os.environ:
            form = await self.inline.form(
                self.strings("lavhost_web"),
                message=message,
                reply_markup={"text": self.strings("web_btn"), "url": "http://127.0.0.1"},
                photo="https://imgur.com/a/yOoHsa2.png",
            )
            return

        if (
            not force
            and not message.is_private
            and "force_insecure" not in message.raw_text.lower()
        ):
            try:
                if not await self.inline.form(
                    self.strings("privacy_leak_nowarn").format(self._client.tg_id),
                    message=message,
                    reply_markup=[
                        {
                            "text": self.strings("btn_yes"),
                            "callback": self.weburl,
                            "args": (True,),
                        },
                        {"text": self.strings("btn_no"), "action": "close"},
                    ],
                    photo="https://imgur.com/a/NumfPGa.png",
                ):
                    raise Exception
            except Exception:
                await utils.answer(
                    message,
                    self.strings("privacy_leak").format(
                        self._client.tg_id,
                        utils.escape_html(self.get_prefix()),
                    ),
                )
            return

        form = await self.inline.form(
            self.strings("opening_tunnel"),
            message=message,
            reply_markup={"text": "🕔 Wait...", "data": "https://..."},
            photo="https://imgur.com/a/MQJGI0w.png",
        )

       # await asyncio.sleep(5)  # Задержка в 5 секунд

        await form.edit(
            self.strings("tunnel_opened"),
            reply_markup={"text": self.strings("web_btn"), "url": "http://127.0.0.1"},
            photo="https://imgur.com/a/lgmzCpj.png",
        )
