from db.config import SessionLocal
from fastapi import APIRouter

async def create_session():
    async with SessionLocal() as session:
        yield session


def router(router: APIRouter, prefix: str, tag: str):
    return (router, f'/fast-api{prefix}', tag)