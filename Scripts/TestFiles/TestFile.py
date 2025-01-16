# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

# LCEL 文档
url = "https://python.langchain.com/docs/concepts/lcel/"
loader = RecursiveUrlLoader(
    url=url, max_depth=20, extractor=lambda x: Soup(x, "html.parser").text
)
docs = loader.load()

# 根据URL排序列表并获取文本
d_sorted = sorted(docs, key=lambda x: x.metadata["source"])
d_reversed = list(reversed(d_sorted))
concatenated_content = "\n\n\n --- \n\n\n".join(
    [doc.page_content for doc in d_reversed]
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')
default_model = os.getenv('Deepseek_Default_Model')


### OpenAI

# 评分提示
code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """你是一个具有LCEL（LangChain expression language）专业知识的编码助手。\n 
    这里是一整套LCEL文档：\n ------- \n  {context} \n ------- \n 根据上述提供的文档回答用户问题。确保你提供的任何代码都可以执行，\n 
    并且定义了所有需要的导入和变量。将你的答案结构化为代码解决方案的描述。\n
    然后列出导入。最后列出功能代码块。这里是用户的问题：""",
        ),
        ("placeholder", "{messages}"),
    ]
)


# 数据模型
class code(BaseModel):
    """关于LCEL问题的代码解决方案的模式。"""

    prefix: str = Field(description="问题和方法的描述")
    imports: str = Field(description="代码块的import语句")
    code: str = Field(description="不包括import语句的代码块")

llm = ChatOpenAI(model="deepseek-chat", api_key=api_key, base_url=api_url)
code_gen_chain_oai = code_gen_prompt | llm.with_structured_output(code)
question = "如何在LCEL中构建RAG链？"
solution = code_gen_chain_oai.invoke(
    {"context": concatenated_content, "messages": [("user", question)]}
)
# solution

print(solution)