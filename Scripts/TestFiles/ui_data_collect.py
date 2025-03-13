# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties

# 设置字体
font = FontProperties(fname='C:/Windows/Fonts/simhei.ttf')  # 确保路径正确

# 假设数据存储在这个字符串中，你也可以从文件读取
data_str = """
Name=txt_冒险笔记  
CtrlType=CMyText  
x=0.4585  
y=0.0557  
Width=0.0917  
Height=0.0267  
Text='冒险笔记'

Name=txt_总览  
CtrlType=CMyText  
x=0.1146  
y=0.1497  
Width=0.0494  
Height=0.0325  
Text='总览'

Name=txt_神兽  
CtrlType=CMyText  
x=0.1146  
y=0.2030  
Width=0.0494  
Height=0.0325  
Text='神兽'

Name=txt_故事  
CtrlType=CMyText  
x=0.1146  
y=0.2564  
Width=0.0494  
Height=0.0325  
Text='故事'

Name=txt_玩法副本  
CtrlType=CMyText  
x=0.1146  
y=0.3097  
Width=0.0741  
Height=0.0325  
Text='玩法副本'

Name=txt_观景台  
CtrlType=CMyText  
x=0.1146  
y=0.3631  
Width=0.0564  
Height=0.0325  
Text='观景台'

Name=txt_升级风物  
CtrlType=CMyText  
x=0.1146  
y=0.4167  
Width=0.0741  
Height=0.0325  
Text='升级风物'

Name=txt_主线故事  
CtrlType=CMyText  
x=0.2822  
y=0.1497  
Width=0.1235  
Height=0.0290  
Text='主线故事'

Name=txt_最后一个主线名称  
CtrlType=CMyText  
x=0.2822  
y=0.2030  
Width=0.1579  
Height=0.0290  
Text='最后一个主线名称'

Name=img_主线图片  
CtrlType=CMyText  
x=0.2822  
y=0.2459  
Width=0.6781  
Height=0.2413  
Text=''

Name=txt_支线故事  
CtrlType=CMyText  
x=0.2822  
y=0.5140  
Width=0.1235  
Height=0.0290  
Text='支线故事'

Name=txt_解锁的故事名称1  
CtrlType=CMyText  
x=0.2822  
y=0.5790  
Width=0.1579  
Height=0.0290  
Text='解锁的故事名称'

Name=input_支线icon1  
CtrlType=CMyText  
x=0.2822  
y=0.6220  
Width=0.2011  
Height=0.1160  
Text='支线\nicon'

Name=txt_未解锁故事名称1  
CtrlType=CMyText  
x=0.5123  
y=0.5790  
Width=0.1579  
Height=0.0290  
Text='未解锁故事名称'

Name=input_支线icon2  
CtrlType=CMyText  
x=0.5123  
y=0.6220  
Width=0.2011  
Height=0.1160  
Text='支线\nicon'

Name=txt_解锁的故事名称2  
CtrlType=CMyText  
x=0.7425  
y=0.5790  
Width=0.1579  
Height=0.0290  
Text='解锁的故事名称'

Name=input_支线icon3  
CtrlType=CMyText  
x=0.7425  
y=0.6220  
Width=0.2011  
Height=0.1160  
Text='支线\nicon'

Name=txt_解锁的故事名称3  
CtrlType=CMyText  
x=0.2822  
y=0.7564  
Width=0.1579  
Height=0.0290  
Text='解锁的故事名称'

Name=input_支线icon4  
CtrlType=CMyText  
x=0.2822  
y=0.8000  
Width=0.2011  
Height=0.1160  
Text='支线'

Name=txt_解锁的故事名称4  
CtrlType=CMyText  
x=0.5123  
y=0.7564  
Width=0.1579  
Height=0.0290  
Text='解锁的故事名称'

Name=input_支线icon5  
CtrlType=CMyText  
x=0.5123  
y=0.8000  
Width=0.2011  
Height=0.1160  
Text='支线'

Name=txt_解锁的故事名称5  
CtrlType=CMyText  
x=0.7425  
y=0.7564  
Width=0.1579  
Height=0.0290  
Text='解锁的故事名称'

Name=input_支线icon6  
CtrlType=CMyText  
x=0.7425  
y=0.8000  
Width=0.2011  
Height=0.1160  
Text='支线'

Name=btn_一键领取  
CtrlType=CMyButton  
x=0.4639  
y=0.9188  
Width=0.1411  
Height=0.0429  
Text='一键领取'
"""

# 假设屏幕分辨率
screen_width = 1134
screen_height = 862

# 解析数据
controls = []
for block in data_str.strip().split('\n\n'):
    control = {}
    for line in block.split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            control[key.strip()] = value.strip().strip("'")
    controls.append(control)

# 创建绘图对象
fig, ax = plt.subplots()

# 绘制矩形和文本
for control in controls:
    x = float(control['x']) * screen_width
    y = float(control['y']) * screen_height
    width = float(control['Width']) * screen_width
    height = float(control['Height']) * screen_height
    text = control.get('Text', '')
    if control['CtrlType'] == 'CMyText':
        color = 'red'
    elif control['CtrlType'] == 'CMyButton':
        color = 'green'
    rect = Rectangle((x, y), width, height, edgecolor=color, facecolor='none')
    ax.add_patch(rect)
    # 在矩形范围内绘制文本
    ax.text(x + width / 2, y + height / 2, text, ha='center', va='center', fontsize=10, fontproperties=font)

# 设置坐标轴范围和显示图形
ax.set_xlim(0, screen_width)
ax.set_ylim(0, screen_height)
ax.set_aspect('equal')
#反转 （有的大模型embedding的y轴是反的）
plt.gca().invert_yaxis()
plt.show()