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


# if __name__ == "__main__":
#     # 假设你可以将 app.get_graph() 的结果存储到 graph 变量中，这里仅为示例，你需要根据实际情况修改
#     graph = Graph(
#         nodes={
#             '__start__': Node(id='__start__', name='__start__', data=None, metadata=None),
#             'Planning模块': Node(id='Planning模块', name='Planning模块', data=None, metadata=None),
#             '参考代码查询模块': Node(id='参考代码查询模块', name='参考代码查询模块', data=None, metadata=None),
#             '代码生成模块': Node(id='代码生成模块', name='代码生成模块', data=None, metadata=None),
#             '代码测试模块': Node(id='代码测试模块', name='代码测试模块', data=None, metadata=None),
#             '代码验收模块': Node(id='代码验收模块', name='代码验收模块', data=None, metadata=None),
#             '代码生成审查模块': Node(id='代码生成审查模块', name='代码生成审查模块', data=None, metadata=None),
#             '记忆加载模块': Node(id='记忆加载模块', name='记忆加载模块', data=None, metadata=None),
#             '记忆保存模块': Node(id='记忆保存模块', name='记忆保存模块', data=None, metadata=None),
#             '记忆检索模块': Node(id='记忆检索模块', name='记忆检索模块', data=None, metadata=None),
#             '决定是否完成': Node(id='决定是否完成', name='决定是否完成', data=None, metadata=None),
#             '__end__': Node(id='__end__', name='__end__', data=None, metadata=None)
#         },
#         edges=[
#             Edge(source='Planning模块', target='参考代码查询模块', data=None, conditional=False),
#             Edge(source='__start__', target='Planning模块', data=None, conditional=False),
#             Edge(source='代码生成模块', target='代码测试模块', data=None, conditional=False),
#             Edge(source='参考代码查询模块', target='代码生成模块', data=None, conditional=False),
#             Edge(source='代码测试模块', target='__end__', data='end', conditional=True),
#             Edge(source='代码测试模块', target='代码生成审查模块', data='reflect', conditional=True),
#             Edge(source='代码测试模块', target='代码生成模块', data='generate', conditional=True)
#         ]
#     )
#     mermaid_code = graph_to_mermaid(graph)
#     print(mermaid_code)


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


class Node:
    def __init__(self, id, name, data, metadata):
        self.id = id
        self.name = name
        self.data = data
        self.metadata = metadata


class Edge:
    def __init__(self, source, target, data, conditional):
        self.source = source
        self.target = target
        self.data = data
        self.conditional = conditional


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges


def graph_to_mermaid(graph):
    mermaid_str = "flowchart TD\n"
    # 处理节点
    for node_id, node in graph.nodes.items():
        # 提取节点名称
        node_name = node.name
        # 为节点添加唯一标识符，防止名称冲突
        mermaid_str += f"    {node_id}[{node_name}]\n"
    # 处理边
    for edge in graph.edges:
        # 根据边的条件添加不同的箭头表示
        if edge.conditional:
            mermaid_str += f"    {edge.source} -->|{edge.data}| {edge.target}\n"
        else:
            mermaid_str += f"    {edge.source} --> {edge.target}\n"
    return mermaid_str


# 以下是根据你提供的数据构造图对象
nodes = {
    '__start__': Node('__start__', '__start__', None, None),
    'Planning模块': Node('Planning模块', 'Planning模块', None, None),
    '参考代码查询模块': Node('参考代码查询模块', '参考代码查询模块', None, None),
    '代码生成模块': Node('代码生成模块', '代码生成模块', None, None),
    '代码测试模块': Node('代码测试模块', '代码测试模块', None, None),
    '代码验收模块': Node('代码验收模块', '代码验收模块', None, None),
    '代码生成审查模块': Node('代码生成审查模块', '代码生成审查模块', None, None),
    '记忆加载模块': Node('记忆加载模块', '记忆加载模块', None, None),
    '记忆保存模块': Node('记忆保存模块', '记忆保存模块', None, None),
    '记忆检索模块': Node('记忆检索模块', '记忆检索模块', None, None),
    '决定是否完成': Node('决定是否完成', '决定是否完成', None, None),
    '结束前模块': Node('结束前模块', '结束前模块', None, None),
    '__end__': Node('__end__', '__end__', None, None)
}

edges = [
    Edge('Planning模块', '参考代码查询模块', None, False),
    Edge('__start__', 'Planning模块', None, False),
    Edge('代码生成审查模块', '代码生成模块', None, False),
    Edge('代码生成模块', '代码测试模块', None, False),
    Edge('参考代码查询模块', '代码生成模块', None, False),
    Edge('结束前模块', '__end__', None, False),
    Edge('代码测试模块', '结束前模块', 'end', True),
    Edge('代码测试模块', '代码生成审查模块', 'reflect', True),
    Edge('代码测试模块', '代码生成模块', 'generate', True)
]

graph = Graph(nodes, edges)
mermaid_code = graph_to_mermaid(graph)
print(mermaid_code)