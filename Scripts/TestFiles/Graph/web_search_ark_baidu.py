from typing import List, Optional
from typing_extensions import TypedDict
from playwright.async_api import Page, async_playwright
import asyncio
import platform
import base64
import os
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

class BBox(TypedDict):
    x: float
    y: float
    text: str
    type: str
    ariaLabel: str

class AgentState:
    def __init__(self, page: Page, input: str):
        self.page = page
        self.input = input
        self.img = ""
        self.bboxes: List[BBox] = []
        self.scratchpad: List[str] = []
        self.observation = ""

class WebSearchTool:
    def __init__(self, api_key: str = None, api_url: str = None, model_name: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv('Doubao_API_Key')
        self.api_url = api_url or os.getenv('Doubao_API_URL')
        self.model_name = model_name or 'ep-20250124142348-md7td'
        self.client = Ark(api_key=self.api_key)
        
        # 获取当前脚本的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建文件路径
        file_path = os.path.join(current_dir, "mark_page.js")
        # 读取JavaScript文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            self.mark_page_script = f.read()

    async def _mark_page(self, page: Page, debug_mark : bool = False):
        
        # while debug_mark:
        #     await asyncio.sleep(3)
        
        await page.evaluate(self.mark_page_script)
        bboxes = []
        for _ in range(5):
            try:
                bboxes = await page.evaluate("markPage()")
                break
            except Exception:
                await asyncio.sleep(3)
        
        screenshot = await page.screenshot()
        await page.evaluate("unmarkPage()")
        
        return {
            "img": base64.b64encode(screenshot).decode(),
            "bboxes": bboxes
        }

    async def _click(self, state: AgentState, bbox_id: int) -> str:
        try:
            bbox = state.bboxes[bbox_id]
            x, y = bbox["x"], bbox["y"]
            await state.page.mouse.click(x, y)
            return f"Clicked {bbox_id}"
        except Exception as e:
            return f"Error clicking {bbox_id}: {str(e)}"

    async def _type_text(self, state: AgentState, bbox_id: int, text: str) -> str:
        try:
            bbox = state.bboxes[bbox_id]
            x, y = bbox["x"], bbox["y"]
            await state.page.mouse.click(x, y)
            select_all = "Meta+A" if platform.system() == "Darwin" else "Control+A"
            await state.page.keyboard.press(select_all)
            await state.page.keyboard.press("Backspace")
            await state.page.keyboard.type(text)
            await state.page.keyboard.press("Enter")
            return f"Typed {text} and submitted"
        except Exception as e:
            return f"Error typing text: {str(e)}"

    async def _scroll(self, state: AgentState, target: str, direction: str) -> str:
        try:
            if target.upper() == "WINDOW":
                scroll_amount = 500
                scroll_direction = -scroll_amount if direction.lower() == "up" else scroll_amount
                await state.page.evaluate(f"window.scrollBy(0, {scroll_direction})")
            else:
                scroll_amount = 200
                target_id = int(target)
                bbox = state.bboxes[target_id]
                x, y = bbox["x"], bbox["y"]
                scroll_direction = -scroll_amount if direction.lower() == "up" else scroll_amount
                await state.page.mouse.move(x, y)
                await state.page.mouse.wheel(0, scroll_direction)
            return f"Scrolled {direction} in {'window' if target.upper() == 'WINDOW' else 'element'}"
        except Exception as e:
            return f"Error scrolling: {str(e)}"

    async def _execute_action(self, state: AgentState, action: str, args: List[str]) -> str:
        if action == "Click" and len(args) == 1:
            return await self._click(state, int(args[0]))
        elif action == "Type" and len(args) == 2:
            return await self._type_text(state, int(args[0]), args[1])
        elif action == "Scroll" and len(args) == 2:
            return await self._scroll(state, args[0], args[1])
        elif action == "Wait":
            await asyncio.sleep(5)
            return "Waited for 5s."
        elif action == "GoBack":
            await state.page.go_back()
            return f"Navigated back to {state.page.url}."
        elif action == "Search":
            await state.page.goto("https://www.baidu.com/")
            return "Navigated to baidu.com."
        return f"Unknown or invalid action: {action}"

    async def search(self, query: str, max_steps: int = 10) -> str:
        state = None
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            # 设置浏览器窗口大小
            await page.set_viewport_size({"width": 960, "height": 500})
            await page.goto("https://www.baidu.com")
            
            state = AgentState(page, query)
            step = 0
            
            while step < max_steps:
                # 标注页面并获取截图
                marked_page = await self._mark_page(page, step > 0)
                state.img = marked_page["img"]
                state.bboxes = marked_page["bboxes"]
                
                # 构建提示词
                bbox_descriptions = "\nValid Bounding Boxes:\n" + "\n".join(
                    f'{i} (<{bbox["type"]}/): "{bbox["text"]}"'
                    for i, bbox in enumerate(state.bboxes)
                )
                
                # 调用模型获取下一步动作
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    temperature = 0.0,
                    messages=[
                        {
                            "role": "system",
                            "content": "你是一个像人类一样浏览网页的机器人。分析截图中的数字标签，选择合适的动作。\n\n每次只能输出一个Action。你必须找到用户提出所有问题的准确答案才可以输出ANSWER。你必须严格按照以下格式输出：\n想法：[简要描述你的分析和决策]\nAction: [动作] [参数1]; [参数2]\n\n可用的动作格式：\n- Click [数字标签]\n- Type [数字标签]; [内容]\n- Scroll [数字标签或WINDOW]; [up或down]\n- Wait\n- GoBack\n- Search\n- ANSWER [内容]\n\n示例输出：\n想法：我看到搜索框，需要输入查询内容\nAction: Type 4; 搜索内容"
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"任务：{query}\n历史操作：{'\n'.join(state.scratchpad)}\n{bbox_descriptions}"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{state.img}"
                                    }
                                }
                            ]
                        }
                    ]
                )
                
                # 解析模型响应
                model_response = response.choices[0].message.content
                print("=======bbox_descriptions:=======\n" + bbox_descriptions)
                print("\n=======Model Response:=======\n" + model_response)
                
                # 使用TypedDict规范解析结果
                prediction: Prediction = {"action": "", "args": None}
                
                # 解析action和args
                action_line = [line for line in model_response.split('\n') if line.startswith('Action:')]
                if not action_line:
                    prediction["action"] = "retry"
                    prediction["args"] = ["Could not parse model response: no Action found"]
                else:
                    action_parts = action_line[0].replace('Action:', '').strip().split(' ', 1)
                    prediction["action"] = action_parts[0].strip()
                    
                    if len(action_parts) > 1:
                        prediction["args"] = [arg.strip().strip('[]') for arg in action_parts[1].strip().split(';')]
                
                if prediction["action"] == "ANSWER":
                    await browser.close()
                    return prediction["args"][0] if prediction["args"] else "No answer provided."
                
                print("observation :" + prediction["action"] + " " + str(prediction["args"]))

                # 执行动作
                observation = await self._execute_action(state, prediction["action"], prediction["args"] or [])
                state.scratchpad.append(f"{step + 1}. {prediction['action']}: {prediction['args']} -> {observation}")
                step += 1
            
            await browser.close()
            return "Reached maximum steps without finding an answer."

async def main():
    tool = WebSearchTool()
    result = await tool.search("哪吒二2月21日最新的票房是多少？距离世界影史第一还差多少？")
    print(f"Final response: {result}")

if __name__ == "__main__":
    asyncio.run(main())