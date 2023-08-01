import config.globals as g
from config.enums import ChatModels
from fastapi.encoders import jsonable_encoder
# from app.chatgpt.asyncChatbotV1 import AsyncChatbot
from app.chatgpt.V1 import AsyncChatbot
import asyncio
from utils.common import get_conversation_model


class ChatGPTManager:
    """A non-Official chat function, using token to interact with the openai api. You have to use some proxy url to make
        sure that your system is running correctly.

    """

    def __init__(self):
        """initialize function.

        """
        self.chatbot = AsyncChatbot({
            "access_token": g.config.get("chatgpt_access_token"),
            "paid": g.config.get("chatgpt_paid"),
        })
        self.semaphore = asyncio.Semaphore(1)

    def is_busy(self):
        return self.semaphore.locked()

    async def get_conversations(self):
        """get all conversation histories of a user.

        :return: conversations
        """

        conversations = await self.chatbot.get_conversations()
        return conversations

    async def get_conversation_messages(self, conversation_id: str):
        """get a concrete conversation with the given conversation_id

        :param conversation_id: id of the conversation
        :return: Conversation Model
        """
        # TODO: 使用 redis 缓存
        messages = await self.chatbot.get_msg_history(conversation_id)
        messages = jsonable_encoder(messages)
        model_name = get_conversation_model(messages)
        messages["model_name"] = model_name or ChatModels.unknown.value
        return messages

    async def clear_conversations(self):
        """clear all conversations

        :return: None
        """
        await self.chatbot.clear_conversations()

    def ask(self, message, conversation_id: str = None, parent_id: str = None,
            timeout=360, model_name: ChatModels = None):
        """ask problem

        :param message: the problem user asked for
        :param conversation_id: id of the conversation
        :param parent_id: id of the parent conversation
        :param timeout: time threshold to wait for
        :param model_name: name of the model chatgpt used
        """

        if model_name is not None and model_name != ChatModels.unknown:
            self.chatbot.config["model"] = model_name.value
        return self.chatbot.ask(message, conversation_id, parent_id, timeout=timeout)

    async def delete_conversation(self, conversation_id: str):
        """delete a conversation with conversation_id

        :param conversation_id: id of the conversation
        :return:
        """

        await self.chatbot.delete_conversation(conversation_id)

    async def set_conversation_title(self, conversation_id: str, title: str):
        """Hack change_title to set title in utf-8"""
        await self.chatbot.change_title(conversation_id, title)

    async def generate_conversation_title(self, conversation_id: str, message_id: str):
        """Hack gen_title to get title"""
        await self.chatbot.gen_title(conversation_id, message_id)

    def reset_chat(self):
        self.chatbot.reset_chat()
        if self.chatbot.config.get("model"):
            self.chatbot.config["model"] = None