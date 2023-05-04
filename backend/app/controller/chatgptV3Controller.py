import asyncio
from app.chatgpt.V3 import AsyncChatGptV3Bot
from config.enums import ChatModels


class ChatGPTV3Manager:
    """
        ChatGPT Official Manager, containing basic ask function which supports multi-wheeled chats and basic functions
        which supports the async system.
    """

    def __init__(self, api_key):
        """initialize function

        :param api_key: api_key of openai
        """
        self.chatbot = AsyncChatGptV3Bot(api_key=api_key)
        self.semaphore = asyncio.Semaphore(1)
        self.image_keywords = ["image", "图片", "create image", "生成图片"]

    def is_busy(self):
        """是否在对话中

        :return:
        """
        return self.semaphore.locked()

    def get_conversations(self):
        """获取历史对话

        """
        conversations = self.chatbot.get_conversations()
        return conversations

    def load_chats(self, messages: list[dict[str, str]], chat_id: str = "default"):
        """加载历史对话

        """
        if len(self.chatbot.conversation.get(chat_id, [])) <= 1:
            for message in messages:
                self.chatbot.transfer_message_to_conversation(message=message['content'], role=message['role'],
                                                              chat_id=chat_id)

    async def clear_conversations(self):
        """清空对话

        """
        self.chatbot.reset()

    def ask(self, message, role: str = "user", chat_id: str = None, timeout=360, model_name: ChatModels = None):
        """对话

        """
        if model_name is not None and model_name != ChatModels.unknown:
            self.chatbot.engine = model_name.value
        for keyword in self.image_keywords:
            if keyword in message:
                return self.chatbot.get_image(prompt=message, convo_id=chat_id)
        return self.chatbot.ask(message, role, chat_id, timeout=timeout)

    def reset_chat(self, chat_id: str = None):
        """重置对话

        """
        self.chatbot.clear_chats(chat_id)

    async def verify_api_key(self):
        """verify api key, check whether it is valid.

        :return: int: Response.status_code
        """
        return await self.chatbot.verify_api_key()

    async def billing_info(self):
        return self.chatbot.billing_info()

    async def get_image(self, message, chat_id, number: int = 1, size: str = "512x512"):
        return self.chatbot.get_image(message, chat_id, number, size)

