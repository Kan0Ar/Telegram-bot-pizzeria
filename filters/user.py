from aiogram.types import Message
import os
from aiogram.filters import BaseFilter
from dotenv import load_dotenv


load_dotenv()
notADMINS = [int(os.getenv("ADMINID"))]


class NotAdmin(BaseFilter):

    async def check(self, message: Message):
        return message.from_user.id not in notADMINS