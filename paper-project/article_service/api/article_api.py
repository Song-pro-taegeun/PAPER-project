from fastapi import APIRouter
from article_service.api.user import UserRequest, UserResponse
from article_service.app.agent import run_langchain
import logging

router = APIRouter(prefix="/article_service")

@router.post("/input")
async def input(input_request: UserRequest) -> UserResponse:
    logging.info(f"query : {input_request.query}, content: {input_request.content}")
    return run_langchain(input_request)

@router.get("/test")
async def get_test():
    return {"message" : "응답확인"}