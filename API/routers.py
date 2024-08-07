from fastapi import APIRouter
from API.config import router

from API.views import send_message


def load_routers():
    return (
        router(send_message.router.router, '/send-message', ['send-message']),
    )