# import datetime
# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage
# import openai

# # 加载.env文件中的环境变量
# load_dotenv()

# api_key = os.getenv('Doubao_API_Key')
# api_url = os.getenv('Doubao_API_URL')

# model_name = "Doubao-1.5-vision-pro"

# # 创建一个OpenAI客户端
# client = ChatOpenAI(model=model_name,
#                  api_key=api_key, 
#                  base_url=api_url,
#                  max_tokens = 4096)

# # 加载一张图片
# image_path = r"G:\Project\AgentWorkflow\Scripts\TestFiles\test.jpg"
# image = open(image_path, 'rb')

# # #展示图片
# # from PIL import Image
# # import matplotlib.pyplot as plt

# # img = Image.open(image_path)
# # plt.imshow(img)
# # plt.axis('off')
# # plt.show()

# prompt = """
# 请回答图片中的问题
# """

# # # 记录请求发送时间
# # start_time = datetime.datetime.now()

# # response = client.chat.completions.create(
# #     model=model_name,
# #     messages=[
# #         {"role": "system", "content": "你是一个数学家，请用中文思考和输出。"},
# #         {"role": "user", "content": prompt},
# #         {"role": "user", "content": image},
# #     ],
# #     stream=False
# # )

# # # 记录响应接收时间
# # end_time = datetime.datetime.now()

# # # 计算时间间隔
# # time_interval = end_time - start_time
# # print("Response time interval:", time_interval)

# # 打印响应  
# # print(response)


# import openai
# import base64

# # # 设置你的 OpenAI API 密钥
# # openai.api_key = "your_openai_api_key"

# def encode_image(image_path):
#     """
#     对图片进行 Base64 编码
#     """
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# def main():
#     # 图片文件路径
#     image_path = r"G:\Project\AgentWorkflow\Scripts\TestFiles\test.jpg"
#     # 对图片进行编码
#     base64_image = encode_image(image_path)

#     # 构建请求消息
#     messages = [
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": prompt},
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}"
#                     }
#                 }
#             ]
#         }
#     ]

#     # 创建一个OpenAI客户端
#     client = ChatOpenAI(model=model_name,
#                     api_key=api_key, 
#                     base_url=api_url,
#                     max_tokens = 4096)
    
#     # messages = [
#     #     HumanMessage(content="介绍一下你的能力?")
#     # ]

#     response = client.invoke(messages)

#     # 输出模型的回复
#     print(response.content)

# if __name__ == "__main__":
#     main()


# import base64
# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from PIL import Image
# import matplotlib.pyplot as plt

# # 加载.env文件中的环境变量
# load_dotenv()

# api_key = os.getenv('Doubao_API_Key')
# api_url = os.getenv('Doubao_API_URL')

# model_name = "Doubao-1.5-vision-pro"

# # 创建一个OpenAI客户端
# client = ChatOpenAI(model=model_name,
#                     api_key=api_key, 
#                     base_url=api_url,
#                     max_tokens=4096)

# # 加载一张图片
# image_path = r"G:\Project\AgentWorkflow\Scripts\TestFiles\test.jpg"
# with open(image_path, 'rb') as image:
#     image_data = image.read()
    
# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')

# # 展示图片
# img = Image.open(image_path)
# plt.imshow(img)
# plt.axis('off')
# plt.show()

# # 将图片转为Base64编码
# base64_image = encode_image(image_path)

# # 示例消息
# messages = [
#     {"role": "system", "content": "你是一个经验丰富的图像分析师，请用中文思考和输出。"},
#     {"role": "user", "content": "请分析这张图片。"}
# ]

# # 调用 API，传递图像数据
# response = client.invoke(messages, files={"image": image_data})
# print(response)






import base64
import os
# 通过 pip install volcengine-python-sdk[ark] 安装方舟SDK
from volcenginesdkarkruntime import Ark
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from PIL import Image
import matplotlib.pyplot as plt

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Doubao_API_Key')
api_url = os.getenv('Doubao_API_URL')

model_name = "Doubao-1.5-vision-pro"

# 初始化一个Client对象，从环境变量中获取API Key
client = Ark(
    api_key=api_key,
    )

# 定义方法将指定路径图片转为Base64编码
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# 需要传给大模型的图片
image_path = r"G:\Project\AgentWorkflow\Scripts\TestFiles\UI_Test1.png"
image_path3 = r"G:\Project\AgentWorkflow\Scripts\TestFiles\test3.jpeg"

image_url = r"https://img0.baidu.com/it/u=1723120327,1267441483&fm=253&fmt=auto&app=138&f=JPEG?w=864&h=486"
image_url2 = r"https://pics2.baidu.com/feed/b03533fa828ba61e6584d8147ee5170e314e59fc.jpeg?token=44bb54bfcba7607dd1c2fadeb08ee67b&s=F1950B74A6B56D8A4AFE71C2030030B9"

# 将图片转为Base64编码
base64_image = encode_image(image_path)

# # 展示图片
# img = Image.open(image_path)
# plt.imshow(img)
# plt.axis('off')
# plt.show()

prompt = """
**任务描述**：  
你是一个UI设计图解析工具，需要根据提供的UI设计图识别出所有控件的具体信息。每个控件均为矩形控件，输出格式如下：

```
Name=txt_Desc1  
CtrlType=CMyText  
x=320  
y=360  
Width=385  
Height=25  
```

**规则说明**：  
1. **Name**：根据控件的功能起名字，命名规则为：  
   - 如果是文本控件，前缀为 `txt_`，例如 `txt_Desc1`。  
   - 如果是按钮控件，前缀为 `btn_`，例如 `btn_Submit`。  
   - 如果是图片控件，前缀为 `img_`，例如 `img_Logo`。  
   - 如果是输入框控件，前缀为 `input_`，例如 `input_Username`。  
2. **CtrlType**：  
   - 如果控件可以点击，使用 `CMyButton`。  
   - 如果控件不可点击，使用 `CMyText`。  
3. **x, y**：控件矩形位置的左下角起始坐标。  
4. **Width, Height**：控件矩形的宽度和高度。  

**输入**：  
一张UI设计图。  

**输出**：  
按照上述格式输出所有控件的具体信息，每个控件单独输出，示例：  

```
Name=txt_Title  
CtrlType=CMyText  
x=100  
y=500  
Width=200  
Height=50  

Name=btn_Submit  
CtrlType=CMyButton  
x=150  
y=400  
Width=100  
Height=40  
```

**注意**：  
1. 确保所有控件均为矩形控件。  
2. 如果无法确定控件的功能或类型，请使用默认值：`Name=Unknown`, `CtrlType=CMyText`。  
3. 如果无法确定控件的坐标或大小，请标记为 `x=0`, `y=0`, `Width=0`, `Height=0`。  
4. 输入的图片屏幕大小为：`1000x500`。
"""

response = client.chat.completions.create(
  # 替换为您的
  model= 'ep-20250124142348-md7td',
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt,
        },
        {
          "type": "image_url",
          "image_url": {
          # 需要注意：传入Base64编码前需要增加前缀 data:image/{图片格式};base64,{Base64编码}：
          # PNG图片："url":  f"data:image/png;base64,{base64_image}"
          # JEPG图片："url":  f"data:image/jpeg;base64,{base64_image}"
          # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
            "url":  f"data:image/png;base64,{base64_image}"   #方式2
            # "url": image_url2                                #方式1
          },
        },
      ],
    }
  ],
)

print(response.choices[0])



# import os
# import base64
# from dotenv import load_dotenv
# from volcenginesdkarkruntime import Ark
# from PIL import Image
# import matplotlib.pyplot as plt
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage

# # 加载.env文件中的环境变量
# load_dotenv()

# api_key = os.getenv('Doubao_API_Key')
# api_url = os.getenv('Doubao_API_URL')

# model_name = 'ep-20250124142348-md7td'

# # 初始化一个Client对象，从环境变量中获取API Key
# client = ChatOpenAI(model=model_name,
#                  api_key=api_key, 
#                  base_url=api_url,
#                  max_tokens = 4096)

# # 定义方法将指定路径图片转为Base64编码
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# # 加载一张图片并编码为Base64
# image_path = r"G:\Project\AgentWorkflow\Scripts\TestFiles\test3.jpeg"

# image_url = r"https://pics2.baidu.com/feed/b03533fa828ba61e6584d8147ee5170e314e59fc.jpeg?token=44bb54bfcba7607dd1c2fadeb08ee67b&s=F1950B74A6B56D8A4AFE71C2030030B9"

# encoded_image = encode_image(image_path)

# # 确定图像格式并添加正确的 Base64 前缀
# image_format = "jpeg"  # 根据实际图像格式设置，例如 "png", "jpeg", "webp"
# base64_image = f"data:image/jpeg;base64,{encoded_image}"

# # 展示图片
# # img = Image.open(image_path)
# # plt.imshow(img)
# # plt.axis('off')
# # plt.show()

# # 示例消息
# messages = [
#     {"role": "system", "content": "你是一个经验丰富的图像分析师，请用中文思考和输出。"},
#     {"role": "user", "content": "请尝试解决图片中的问题。think step by step. 验证问题的每一个答案，找到最合适的答案。"},
#     {"role": "user", "content": [
#         {"type": "image_url", "image_url": base64_image}
#     ]}
# ]

# # 调用 API，传递图像数据
# response = client.invoke(
#     model=model_name,
#     input=messages
# )
# print(response)