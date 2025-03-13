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
5. **Text**：需要输出文本内容。

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
Text='测试文本' 

Name=btn_Submit  
CtrlType=CMyButton  
x=150  
y=400  
Width=100  
Height=40
Text='提交'
```

**注意**：  
1. 确保所有控件均为矩形控件。  
2. 如果无法确定控件的功能或类型，请使用默认值：`Name=Unknown`, `CtrlType=CMyText`。  
3. 如果无法确定控件的坐标或大小，请标记为 `x=0`, `y=0`, `Width=0`, `Height=0`。  
4. 输入的图片屏幕大小为：`1134 x 862`。
5. 请保证每个控件的实际大小和位置与UI设计图一致。
6. 控件可以存在折叠，忽略背景中的信息
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
