# -*- coding: utf-8 -*-

import os
import openai
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

### 环境部分
# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')
default_model = os.getenv('Deepseek_Default_Model')


### 模型部分
# 创建一个OpenAI客户端
client = openai.OpenAI(
    api_key=api_key,
    base_url=api_url
)

llm = ChatOpenAI(model="deepseek-chat", api_key=api_key, base_url=api_url)