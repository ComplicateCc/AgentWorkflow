# -*- coding: utf-8 -*-

# 尝试导入 ChatAnthropic 库
from anthropic import ChatAnthropic

# 创建 ChatAnthropic 的实例
llm = ChatAnthropic()

# 以下是一种可能的获取模型列表的假设方法，但实际情况可能不同，具体取决于 ChatAnthropic 的实现
# 可能需要查看 ChatAnthropic 的内部属性或方法，这里假设它有一个名为 get_supported_models 的方法
supported_models = llm.get_supported_models()
print(supported_models)