# 基于python flet库的函数图像计算器

**注意：该项目是作者的参赛项目，在正式参赛前不会接受任何贡献，该项目采用GPL2.0协议开源，请不要用此项目作为你个人的参赛项目**

## 项目介绍
- 背景：在我们的日常学习生活中，需要函数图像辅助我们理解函数
- 功能：
    1. 绘制函数图像（已实现）
    2. 获取函数详细信息（奇偶性，对称性，极值等）（未实现）
    3. 解方程（已实现）
- 具体实现方法：
    1. 利用Matplotlib实现函数绘制，并利用Matplotlib的mathtext功能实现Latex（部分）渲染
    2. 利用flet构建应用UI与多平台支持
    3. 使用latexify作为函数表达式转为Latex
    4. 使用sympy实现解方程


* 注：该应用的latexify库与mathtext函数都是经过作者修改过的，其中mathtext函数已经内嵌进了本项目（位于matplot/mathtext.py），而latexify由于增加功能较多，需要克隆作者的fork并在利用pip在本地安装

## 调试说明
请确保你已经安装了python3.9与pip

### macOS与Linux
``` bash
git clone https://github.com/qjasn/flet-tools.git # 克隆本项目
cd flet-tools # 进入本项目根目录
python3 -m venv .venv # 建立虚拟python环境
source .venv/bin/activate # 进入虚拟python环境
pip install -r requirements.txt # 安装依赖（部分一）
git clone https://github.com/qjasn/latexify_get_from_code.git # 克隆作者的fork
pip install ./latexify_get_from_code # 安装作者修改后的latexify
flet run # 运行该应用
```

### Windows
暂未实现