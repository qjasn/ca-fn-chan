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


* 注：该应用的latexify库与mathtext函数都是经过作者修改过的，latexify与mathtext函数已经内嵌进了本项目（位于matplot/mathtext.py）

## 调试说明
请确保你已经安装了python3.11,pip与git

### macOS与Linux
``` bash
git clone https://github.com/qjasn/flet-tools.git # 克隆本项目
cd flet-tools # 进入本项目根目录
python3 -m venv .venv # 建立虚拟python环境
source .venv/bin/activate # 进入虚拟python环境
pip install -r requirements.txt # 安装依赖
flet run # 运行该应用
```

### Windows

请确保你已经安装了python3.11,pip与git

``` powershell
git clone https://github.com/qjasn/flet-tools.git # 克隆本项目
cd flet-tools # 进入本项目根目录
python3 -m venv .venv # 建立虚拟python环境
.\test_env\Scripts\Activate.ps1 # 进入虚拟python环境
pip install -r requirements.txt # 安装依赖
flet run # 运行该应用
```

## 编译说明：

### 本地编译说明：
（仅理论，作者未成功编译过任何一个二进制包）

**请提前安装好flutter的stable版本（3.2.6）**

#### macOS
仅可用于macOS
确保你已经安装了brew
``` bash
brew install cocoapods
flet build macos
```
编译后的二进制文件在`build/macos`

#### Windows
仅可用于Windows
``` powershell
flet build windows
```
编译后的二进制文件在`build/windows`

#### Linux
适用于Ubuntu
``` bash
apt install libgtk-3-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
flet build linux
```
编译后的二进制文件在`build/linux`

#### iOS
仅可用于macOS
``` bash
brew install autoconf automake libtool pkg-config
brew link libtool
brew cocoapods
pip install git+https://github.com/flet-dev/python-for-ios.git
toolchain build matplotlib numpy
export SERIOUS_PYTHON_IOS_DIST="`realpath dist`"
flet build ipa
```
编译后的二进制文件在`build/ipa`

#### Android
（可用于macOS与Linux）
请参考 https://flet.dev/docs/guides/python/packaging-app-for-distribution/#android

### 云端编译说明
(目前仅支持编译Windows，macOS与Linux平台）
- fork此项目
- 进入GitHub Acton
- 选择flet App Builder
- 点击标题下的build.yml
- 进入后编辑文件
- 更改`env`下的`platform`
  - 选项有`windows`,`macOS`,`Linux`（未进行测试），iOS与Android正在编写
