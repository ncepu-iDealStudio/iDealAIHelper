import enum


class ChatStatus(enum.Enum):
    asking = "asking"
    queueing = "queueing"
    idling = "idling"


class ChatModels(enum.Enum):
    gpt4 = "gpt-4"
    default = "text-davinci-002-render-sha"
    paid = "text-davinci-002-render-paid"
    unknown = ""
    gpt3_base = "gpt-3.5-turbo"
    gpt3_pro = "gpt-3.5-turbo-0301"
    gpt4_0314 = "gpt-4-0314"
    gpt4_32k = "gpt-4-32k"
    gpt4_32k_0314 = "gpt-4-32k-0314"
