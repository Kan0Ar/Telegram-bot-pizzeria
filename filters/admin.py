from aiogram.types import Message
import os
from aiogram.filters import BaseFilter
from dotenv import load_dotenv


load_dotenv()
ADMINS = [int(os.getenv("ADMINID"))]


class IsAdmin(BaseFilter):

    async def check(self, message: Message):
        return message.from_user.id in ADMINS