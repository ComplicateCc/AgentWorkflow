# %pip install --upgrade --quiet  playwright > /dev/null
# !playwright install

from typing import List, Optional
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from playwright.async_api import Page

from langchain_core.messages import HumanMessage, SystemMessage  # 导入消息类型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate # 导入模板
from langchain_core.prompts.image import ImagePromptTemplate

import os
from dotenv import load_dotenv
# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')
lanchain_api = os.getenv('LANGCHAIN_API_KEY')

##临时设置环境变量
###LANGCHAIN_TRACING_V2是设置LangChain是否开启日志跟踪模式。
os.environ['LANGCHAIN_TRACING_V2'] = "true"
###LANGCHAIN_API_KEY就是上面生成的LangSmith的key。
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
###LANGCHAIN_PROJECT 跟踪项目名称
os.environ['LANGCHAIN_PROJECT'] = "Test_Graph_Web_Search"


class BBox(TypedDict):
    x: float
    y: float
    text: str
    type: str
    ariaLabel: str


class Prediction(TypedDict):
    action: str
    args: Optional[List[str]]


# This represents the state of the agent
# as it proceeds through execution
class AgentState(TypedDict):
    page: Page  # The Playwright web page lets us interact with the web environment
    input: str  # User request
    img: str  # b64 encoded screenshot
    bboxes: List[BBox]  # The bounding boxes from the browser annotation function
    prediction: Prediction  # The Agent's output
    # A system message (or messages) containing the intermediate steps
    scratchpad: List[BaseMessage]
    observation: str  # The most recent response from a tool





#Define tools
import asyncio
import platform


async def click(state: AgentState):
    # - Click [Numerical_Label]
    page = state["page"]
    click_args = state["prediction"]["args"]
    if click_args is None or len(click_args) != 1:
        return f"Failed to click bounding box labeled as number {click_args}"
    bbox_id = click_args[0]
    bbox_id = int(bbox_id)
    try:
        bbox = state["bboxes"][bbox_id]
    except Exception:
        return f"Error: no bbox for : {bbox_id}"
    x, y = bbox["x"], bbox["y"]
    await page.mouse.click(x, y)
    # TODO: In the paper, they automatically parse any downloaded PDFs
    # We could add something similar here as well and generally
    # improve response format.
    return f"Clicked {bbox_id}"


async def type_text(state: AgentState):
    page = state["page"]
    type_args = state["prediction"]["args"]
    if type_args is None or len(type_args) != 2:
        return (
            f"Failed to type in element from bounding box labeled as number {type_args}"
        )
    bbox_id = type_args[0]
    bbox_id = int(bbox_id)
    bbox = state["bboxes"][bbox_id]
    x, y = bbox["x"], bbox["y"]
    text_content = type_args[1]
    await page.mouse.click(x, y)
    # Check if MacOS
    select_all = "Meta+A" if platform.system() == "Darwin" else "Control+A"
    await page.keyboard.press(select_all)
    await page.keyboard.press("Backspace")
    await page.keyboard.type(text_content)
    await page.keyboard.press("Enter")
    return f"Typed {text_content} and submitted"


async def scroll(state: AgentState):
    page = state["page"]
    scroll_args = state["prediction"]["args"]
    if scroll_args is None or len(scroll_args) != 2:
        return "Failed to scroll due to incorrect arguments."

    target, direction = scroll_args

    if target.upper() == "WINDOW":
        # Not sure the best value for this:
        scroll_amount = 500
        scroll_direction = (
            -scroll_amount if direction.lower() == "up" else scroll_amount
        )
        await page.evaluate(f"window.scrollBy(0, {scroll_direction})")
    else:
        # Scrolling within a specific element
        scroll_amount = 200
        target_id = int(target)
        bbox = state["bboxes"][target_id]
        x, y = bbox["x"], bbox["y"]
        scroll_direction = (
            -scroll_amount if direction.lower() == "up" else scroll_amount
        )
        await page.mouse.move(x, y)
        await page.mouse.wheel(0, scroll_direction)

    return f"Scrolled {direction} in {'window' if target.upper() == 'WINDOW' else 'element'}"


async def wait(state: AgentState):
    sleep_time = 5
    await asyncio.sleep(sleep_time)
    return f"Waited for {sleep_time}s."


async def go_back(state: AgentState):
    page = state["page"]
    await page.go_back()
    return f"Navigated back a page to {page.url}."


async def to_google(state: AgentState):
    page = state["page"]
    await page.goto("https://www.google.com/")
    return "Navigated to google.com."







### Define Agent
import base64

from langchain_core.runnables import chain as chain_decorator

import os

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建文件路径
file_path = os.path.join(current_dir, "mark_page.js")
# Some javascript we will run on each step
# to take a screenshot of the page, select the
# elements to annotate, and add bounding boxes
with open(file_path, 'r', encoding='utf-8') as f:
    mark_page_script = f.read()


@chain_decorator
async def mark_page(page):
    await page.evaluate(mark_page_script)
    for _ in range(10):
        try:
            bboxes = await page.evaluate("markPage()")
            break
        except Exception:
            # May be loading...
            asyncio.sleep(3)
    screenshot = await page.screenshot()
    # Ensure the bboxes don't follow us around
    await page.evaluate("unmarkPage()")
    return {
        "img": base64.b64encode(screenshot).decode(),
        "bboxes": bboxes,
    }

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


async def annotate(state):
    marked_page = await mark_page.with_retry().ainvoke(state["page"])
    # print(f"Marked page: {marked_page}")
    return {**state, **marked_page}


def format_descriptions(state):
    labels = []
    for i, bbox in enumerate(state["bboxes"]):
        text = bbox.get("ariaLabel") or ""
        if not text.strip():
            text = bbox["text"]
        el_type = bbox.get("type")
        labels.append(f'{i} (<{el_type}/>): "{text}"')
    bbox_descriptions = "\nValid Bounding Boxes:\n" + "\n".join(labels)
    return {**state, "bbox_descriptions": bbox_descriptions}


def parse(text: str) -> dict:
    action_prefix = "Action: "
    if not text.strip().split("\n")[-1].startswith(action_prefix):
        return {"action": "retry", "args": f"Could not parse LLM Output: {text}"}
    action_block = text.strip().split("\n")[-1]

    action_str = action_block[len(action_prefix) :]
    split_output = action_str.split(" ", 1)
    if len(split_output) == 1:
        action, action_input = split_output[0], None
    else:
        action, action_input = split_output
    action = action.strip()
    if action_input is not None:
        action_input = [
            inp.strip().strip("[]") for inp in action_input.strip().split(";")
        ]
    return {"action": action, "args": action_input}


# Will need a later version of langchain to pull
# this image prompt template
# prompt = hub.pull("wfh/web-voyager")

prompt = ChatPromptTemplate.from_messages(
    [
        # 系统消息模板
        SystemMessagePromptTemplate(
            prompt=[PromptTemplate(
                input_variables=[],
                input_types={},
                partial_variables={},
                template="Imagine you are a robot browsing the web, just like humans. Now you need to complete a task. In each iteration, you will receive an Observation that includes a screenshot of a webpage and some texts. This screenshot will\nfeature Numerical Labels placed in the TOP LEFT corner of each Web Element. Carefully analyze the visual\ninformation to identify the Numerical Label corresponding to the Web Element that requires interaction, then follow\nthe guidelines and choose one of the following actions:\n\n1. Click a Web Element.\n2. Delete existing content in a textbox and then type content.\n3. Scroll up or down.\n4. Wait \n5. Go back\n7. Return to google to start over.\n8. Respond with the final answer\n\nCorrespondingly, Action should STRICTLY follow the format:\n\n- Click [Numerical_Label] \n- Type [Numerical_Label]; [Content] \n- Scroll [Numerical_Label or WINDOW]; [up or down] \n- Wait \n- GoBack\n- Google\n- ANSWER; [content]\n\nKey Guidelines You MUST follow:\n\n* Action guidelines \n1) Execute only one action per iteration.\n2) When clicking or typing, ensure to select the correct bounding box.\n3) Numeric labels lie in the top-left corner of their corresponding bounding boxes and are colored the same.\n\n Web Browsing Guidelines *\n1) Don't interact with useless web elements like Login, Sign - in, donation that appear in Webpages\n2) Select strategically to minimize time wasted.\n\nYour reply should strictly follow the format:\n\nThought: {{Your brief thoughts (briefly summarize the info that will help ANSWER)}}\nAction: {{One Action format you choose}}\nThen the User will provide:\nObservation: {{A labeled screenshot Given by User}}\n"
            )],
            additional_kwargs={}
        ),
        
        MessagesPlaceholder(variable_name='scratchpad', optional=True),
        
        HumanMessagePromptTemplate(
            prompt=[
                ImagePromptTemplate(
                    input_variables=['img'],
                    input_types={},
                    partial_variables={},
                    template={'url': 'data:image/png;base64,{img}'}
                ),
                PromptTemplate(
                    input_variables=['bbox_descriptions'],
                    input_types={},
                    partial_variables={},
                    template='{bbox_descriptions}'
                ),
                PromptTemplate(
                    input_variables=['input'],
                    input_types={},
                    partial_variables={},
                    template='{input}'
                )
            ],
            additional_kwargs={}
        ),
    ]
)

from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
from langsmith import traceable

# 加载.env文件中的环境变量
load_dotenv()

# api_key = os.getenv('Deepseek_API_Key')
# api_url = os.getenv('Deepseek_API_URL')

api_key = os.getenv('Doubao_API_Key')
api_url = os.getenv('Doubao_API_URL')

model_name = 'ep-20250124142348-md7td'

##临时设置环境变量
###LANGCHAIN_TRACING_V2是设置LangChain是否开启日志跟踪模式。
os.environ['LANGCHAIN_TRACING_V2'] = "true"
###LANGCHAIN_API_KEY就是上面生成的LangSmith的key。
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
###LANGCHAIN_PROJECT 跟踪项目名称
os.environ['LANGCHAIN_PROJECT'] = "test_web_search"

import json
import openai

llm = ChatOpenAI(model=model_name, 
                 api_key=api_key, 
                 base_url=api_url,
                 max_tokens = 4096)

# agent = annotate | RunnablePassthrough.assign(
#     prediction=format_descriptions | prompt | llm | StrOutputParser() | parse
# )

try:
    # Assuming `format_descriptions`, `prompt`, `llm`, `StrOutputParser`, and `parse` are defined elsewhere
    agent = annotate | RunnablePassthrough.assign(
        prediction=format_descriptions | prompt | llm | StrOutputParser() | parse
    )
    
    # Debugging: Print the JSON body
    json_body = {
        "format_descriptions": format_descriptions,
        "prompt": prompt,
        "llm": llm,
        "StrOutputParser": StrOutputParser(),
        "parse": parse
    }
    print("JSON Body:", json.dumps(json_body, indent=2))

except openai.UnprocessableEntityError as e:
    print("UnprocessableEntityError:", e)
    print("Error details:", e.json_body)
except Exception as e:
    print("An unexpected error occurred:", e)


import re

def update_scratchpad(state: AgentState):
    """After a tool is invoked, we want to update
    the scratchpad so the agent is aware of its previous steps"""
    old = state.get("scratchpad")
    if old:
        txt = old[0].content
        last_line = txt.rsplit("\n", 1)[-1]
        step = int(re.match(r"\d+", last_line).group()) + 1
    else:
        txt = "Previous action observations:\n"
        step = 1
    txt += f"\n{step}. {state['observation']}"

    return {**state, "scratchpad": [SystemMessage(content=txt)]}

from langchain_core.runnables import RunnableLambda

from langgraph.graph import END, START, StateGraph

graph_builder = StateGraph(AgentState)


graph_builder.add_node("agent", agent)
graph_builder.add_edge(START, "agent")

graph_builder.add_node("update_scratchpad", update_scratchpad)
graph_builder.add_edge("update_scratchpad", "agent")

tools = {
    "Click": click,
    "Type": type_text,
    "Scroll": scroll,
    "Wait": wait,
    "GoBack": go_back,
    "Google": to_google,
}


for node_name, tool in tools.items():
    graph_builder.add_node(
        node_name,
        # The lambda ensures the function's string output is mapped to the "observation"
        # key in the AgentState
        RunnableLambda(tool) | (lambda observation: {"observation": observation}),
    )
    # Always return to the agent (by means of the update-scratchpad node)
    graph_builder.add_edge(node_name, "update_scratchpad")


def select_tool(state: AgentState):
    # Any time the agent completes, this function
    # is called to route the output to a tool or
    # to the end user.
    action = state["prediction"]["action"]
    if action == "ANSWER":
        return END
    if action == "retry":
        return "agent"
    return action


graph_builder.add_conditional_edges("agent", select_tool)

graph = graph_builder.compile()

from IPython import display
from playwright.async_api import async_playwright

async def call_agent(question: str, page, max_steps: int = 150):
    event_stream = graph.astream(
        {
            "page": page,
            "input": question,
            "scratchpad": [],
        },
        {
            "recursion_limit": max_steps,
        },
    )
    final_answer = None
    steps = []
    async for event in event_stream:
        # We'll display an event stream here
        if "agent" not in event:
            continue
        pred = event["agent"].get("prediction") or {}
        action = pred.get("action")
        action_input = pred.get("args")
        display.clear_output(wait=False)
        steps.append(f"{len(steps) + 1}. {action}: {action_input}")
        print("\n".join(steps))
        display.display(display.Image(base64.b64decode(event["agent"]["img"])))
        if "ANSWER" in action:
            final_answer = action_input[0]
            break
    return final_answer

async def main():
    browser = await async_playwright().start()
    # We will set headless=False so we can watch the agent navigate the web.
    browser = await browser.chromium.launch(headless=False, args=None)
    page = await browser.new_page()
    _ = await page.goto("https://www.google.com")

    res = await call_agent("你可以告诉我去华宝花园怎么走吗？公交方案", page)
    print(f"Final response: {res}")

asyncio.run(main())