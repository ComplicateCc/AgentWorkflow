from langgraph.graph import StateGraph, START, END

# def graph_to_mermaid(graph):
#     mermaid_code = "graph TD;\n"
#     for node_id, node in graph.nodes.items():
#         mermaid_code += f"    {node_id}[{node.name}];\n"
#     for edge in graph.edges:
#         if edge.conditional:
#             mermaid_code += f"    {edge.source} --{edge.data}--> {edge.target};\n"
#         else:
#             mermaid_code += f"    {edge.source} --> {edge.target};\n"
#     return mermaid_code


# 假设 graph 是你打印出的 app.get_graph() 的结果
# 以下是使用示例
# if __name__ == "__main__":
#     # 假设 graph 是你从 app.get_graph() 得到的结果
#     graph ="""
    
#     """  # 这里需要将你打印出的 app.get_graph() 的结果存储到 graph 变量中
#     mermaid_code = graph_to_mermaid(graph)
#     print(mermaid_code)


# 代码解释：
# 1. graph_to_mermaid 函数接收一个 graph 对象。
# 2. 首先添加 graph TD; 表示创建一个从上到下（Top Down）的流程图。
# 3. 遍历 graph 的节点，将节点添加到 Mermaid 图中，格式为 {node_id}[{node.name}];。
# 4. 遍历 graph 的边，根据边是否有条件添加不同的箭头表示，有条件的边使用 --{edge.data}-->，无条件的边使用 -->。


from langchain_core.runnables.graph import Graph, Node, Edge


def graph_to_mermaid(graph):
    mermaid_code = "graph TD;\n"
    for node_id, node in graph.nodes.items():
        # 假设根据节点的类型添加不同形状，这里仅为示例，可根据实际情况修改
        if "模块" in node.name:
            shape = "rectangle"
        else:
            shape = "circle"
        mermaid_code += f"    {node_id}[{node.name}] {shape};\n"
    for edge in graph.edges:
        if edge.conditional:
            mermaid_code += f"    {edge.source} --{edge.data}--> {edge.target};\n"
        else:
            mermaid_code += f"    {edge.source} --> {edge.target};\n"
    return mermaid_code


if __name__ == "__main__":
    # 假设你可以将 app.get_graph() 的结果存储到 graph 变量中，这里仅为示例，你需要根据实际情况修改
    graph = Graph(
        nodes={
            '__start__': Node(id='__start__', name='__start__', data=None, metadata=None),
            'Planning模块': Node(id='Planning模块', name='Planning模块', data=None, metadata=None),
            '参考代码查询模块': Node(id='参考代码查询模块', name='参考代码查询模块', data=None, metadata=None),
            '代码生成模块': Node(id='代码生成模块', name='代码生成模块', data=None, metadata=None),
            '代码测试模块': Node(id='代码测试模块', name='代码测试模块', data=None, metadata=None),
            '代码验收模块': Node(id='代码验收模块', name='代码验收模块', data=None, metadata=None),
            '代码生成审查模块': Node(id='代码生成审查模块', name='代码生成审查模块', data=None, metadata=None),
            '记忆加载模块': Node(id='记忆加载模块', name='记忆加载模块', data=None, metadata=None),
            '记忆保存模块': Node(id='记忆保存模块', name='记忆保存模块', data=None, metadata=None),
            '记忆检索模块': Node(id='记忆检索模块', name='记忆检索模块', data=None, metadata=None),
            '决定是否完成': Node(id='决定是否完成', name='决定是否完成', data=None, metadata=None),
            '__end__': Node(id='__end__', name='__end__', data=None, metadata=None)
        },
        edges=[
            Edge(source='Planning模块', target='参考代码查询模块', data=None, conditional=False),
            Edge(source='__start__', target='Planning模块', data=None, conditional=False),
            Edge(source='代码生成模块', target='代码测试模块', data=None, conditional=False),
            Edge(source='参考代码查询模块', target='代码生成模块', data=None, conditional=False),
            Edge(source='代码测试模块', target='__end__', data='end', conditional=True),
            Edge(source='代码测试模块', target='代码生成审查模块', data='reflect', conditional=True),
            Edge(source='代码测试模块', target='代码生成模块', data='generate', conditional=True)
        ]
    )
    mermaid_code = graph_to_mermaid(graph)
    print(mermaid_code)


# 代码解释：
# 1. 改进的 graph_to_mermaid 函数根据节点名称中是否包含 "模块" 来为节点设置不同的形状，你可以根据节点的实际情况进行更细致的区分。
# 2. 在 main 部分，创建了一个示例的 Graph 对象作为 graph 变量，你需要将其替换为实际的 app.get_graph() 的结果。
# 3. 调用 graph_to_mermaid 函数将 Graph 对象转换为 Mermaid 代码。

# 输出结果：失败了  https://mermaid.live/
    """
graph TD;
    __start__[__start__] circle;
    Planning模块[Planning模块] rectangle;
    参考代码查询模块[参考代码查询模块] rectangle;
    代码生成模块[代码生成模块] rectangle;
    代码测试模块[代码测试模块] rectangle;
    代码验收模块[代码验收模块] rectangle;
    代码生成审查模块[代码生成审查模块] rectangle;
    记忆加载模块[记忆加载模块] rectangle;
    记忆保存模块[记忆保存模块] rectangle;
    记忆检索模块[记忆检索模块] rectangle;
    决定是否完成[决定是否完成] circle;
    __end__[__end__] circle;
    Planning模块 --> 参考代码查询模块;
    __start__ --> Planning模块;
    代码生成模块 --> 代码测试模块;
    参考代码查询模块 --> 代码生成模块;
    代码测试模块 --end--> __end__;
    代码测试模块 --reflect--> 代码生成审查模块;
    代码测试模块 --generate--> 代码生成模块;
    """

# 实际绘制截取：
#     Planning模块 --> 参考代码查询模块;
#     __start__ --> Planning模块;
#     代码生成模块 --> 代码测试模块;
#     参考代码查询模块 --> 代码生成模块;
#     代码测试模块 --end--> __end__;
#     代码测试模块 --reflect--> 代码生成审查模块;
#     代码测试模块 --generate--> 代码生成模块;