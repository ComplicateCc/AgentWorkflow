# -*- coding: utf-8 -*-

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')

llm = ChatOpenAI(
    model = 'deepseek-chat', 
    openai_api_key = api_key, 
    openai_api_base = api_url,
    max_tokens = 4096
)

messages = [
    HumanMessage(content="介绍一下你的能力?")
]

ret = llm.invoke(messages)

print(ret.content)