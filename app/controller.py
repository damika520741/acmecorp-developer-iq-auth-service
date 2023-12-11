from fastapi import APIRouter
from model import User

import service

router = APIRouter()

@router.post("/signup")
async def signup(user: User):
    return await service.signup(user)

@router.post("/signin")
async def signin(user: User):
    return await service.signin(user)