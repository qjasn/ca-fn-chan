<p align="center">
  <a href="https://github.com/qjasn/ca-fn-chan/">
    <img width="200" height="200" src="https://github.com/qjasn/ca-fn-chan/blob/main/assets/icon.jpg" alt="ca-fn-chan">
  </a>
</p>

<h1 align="center">算方阐</h1>
<h3 align="center">CaFnChan</h3>
<p align="center">基于python的函数图像计算器</p>

**简明扼要的，GPL2.0协议意味着：你可以修改本代码，但你不能用作商用，且在修改完源代码后，以本协议开源你修改的源代码**

## 项目介绍
- 背景：在我们的日常学习生活中，需要函数图像辅助我们理解函数
- 功能：
    1. 绘制函数图像（已实现），导出函数图像（已实现）
    2. 获取函数详细信息（极值）（已实现）
    3. 解方程（已实现）
    4. 内嵌python运行 （未实现）
    5. 拟合曲线 （已实现）
    6. 其它函数与代数功能
- 具体实现方法：
    1. 利用Matplotlib实现函数绘制，并利用Matplotlib的mathtext功能实现Latex（部分）渲染
    2. 利用flet构建应用UI与多平台支持
    3. 使用latexify/sympy作为函数表达式转为Latex
    4. 使用sympy实现解方程
    5. 使用scipy与numpy实现函数相关操作
    6. 使用numpy生成列表
- 名字由来
    1. ”算“取自《则古昔斋算学》（清 李善兰），其中“方阐”取自其中的《方圆阐幽》一章，李善兰先生作为中国首名翻译函数的人，其著作可以说很具有划时代的影响，虽然此项目并不会有划时代的影响，但我还是希望能以此为契机，鼓励我能将计算机爱好坚持下去
    2. 英文名Ca为Calc，Fn为function，Chan即为中文”阐“的音译
    3. 实际上在现代数学的理解中，”算“可以理解为“计算”，“方“可以理解为“方程”，“阐”理解为“阐述”，方程与函数关系密切，考虑的种种因素，这种理解也算合理

* 注：该应用的latexify库与mathtext函数都是经过作者修改过的，latexify与mathtext函数已经内嵌进了本项目（位于./matplot/latex/），其中latexify-py库的fork在qjasn/latexify_get_from_code中

## 调试说明
请确保你已经安装了python3.11,pip与git

**注意：Linux与 Web以及未安装字体包的Windows很大可能会出现中文字体显示问题**

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
# 请在powershell下运行
git clone https://github.com/qjasn/flet-tools.git # 克隆本项目
cd flet-tools # 进入本项目根目录
python3 -m venv .venv # 建立虚拟python环境
.\.venv\Scripts\Activate.ps1 # 进入虚拟python环境
pip install -r requirements.txt # 安装依赖
flet run # 运行该应用
```

iOS、Android与Web调试
（iOS与Android请安装Flet应用）
``` bash
flet run --ios # iOS
flet run --android # Android
flet run --web # Web
```
运行完后，Web会自动打开网页，移动端设备请遵循 https://flet.dev/docs/guides/python/testing-on-ios 或 https://flet.dev/docs/guides/python/testing-on-android 继续下面的步骤

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
brew install cocoapods
pip install git+https://github.com/flet-dev/python-for-ios.git
toolchain build matplotlib numpy scipy
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

* 注意：编译后的macOS app在Apple Silicon上运行后如果numpy/scipy报错，请勾选使用Rosetta2运行
