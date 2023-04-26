from fastapi import Depends, APIRouter

from app import ChatGPTManagerFactory
from app.models.userModel import User
from app.api.routers.system import check_users
from app.schemas.systemSchema import ServerStatusSchema
from app.controller.userController import current_active_user

router = APIRouter()


@router.get("/status", tags=["status"], response_model=ServerStatusSchema)
async def get_server_status(_user: User = Depends(current_active_user)):
    """
    Regular user get server status

    :param _user:

    :return:

    """
    refresh_cache = _user.is_superuser
    active_user_in_5m, active_user_in_1h, active_user_in_1d, queueing_count, _ = await check_users(refresh_cache)
    result = ServerStatusSchema(
        active_user_in_5m=active_user_in_5m,
        active_user_in_1h=active_user_in_1h,
        active_user_in_1d=active_user_in_1d,
        is_chatbot_busy=ChatGPTManagerFactory.get_chatgpt_manager().is_busy(),
        chatbot_waiting_count=queueing_count
    )
    return result
