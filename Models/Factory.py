import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

deepseek_api_key = os.getenv('Deepseek_API_Key')
deepseek_api_url = os.getenv('Deepseek_API_URL')

from langchain_openai import ChatOpenAI, OpenAIEmbeddings, AzureChatOpenAI, AzureOpenAIEmbeddings


class ChatModelFactory:
    model_params = {
        # https://api-docs.deepseek.com/zh-cn/quick_start/parameter_settings
        "temperature": 0,
        # "seed": 42,
    }

    @classmethod
    def get_model(cls, model_name: str, use_azure: bool = False):
        if model_name == "DeepSeek" or model_name == "deepseek":
            # 开源模型替换
            # DeepSeek-V3-Base
            return ChatOpenAI(
                model="DeepSeek",  # 模型名称
                openai_api_key= deepseek_api_key,   # api key
                openai_api_base= deepseek_api_url,  # 平台 API 地址
                **cls.model_params,
            )
        elif "gpt" in model_name:
            if not use_azure:
                return ChatOpenAI(model=model_name, **cls.model_params)
            else:
                return AzureChatOpenAI(
                    azure_deployment=model_name,
                    api_version="2024-05-01-preview",
                    **cls.model_params,
                )

    @classmethod
    def get_default_model(cls):
        return cls.get_model("DeepSeek")


class EmbeddingModelFactory:

    @classmethod
    def get_model(cls, model_name: str, use_azure: bool = False):
        if model_name.startswith("text-embedding"):
            if not use_azure:
                return OpenAIEmbeddings(model=model_name)
            else:
                return AzureOpenAIEmbeddings(
                    azure_deployment=model_name,
                    openai_api_version="2024-05-01-preview",
                )
        else:
            raise NotImplementedError(f"Model {model_name} not implemented.")

    @classmethod
    def get_default_model(cls):
        return cls.get_model("text-embedding-ada-002")
