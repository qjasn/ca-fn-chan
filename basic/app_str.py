from flet_core import Page, ThemeMode

# 此Class用来存放全局变量，以保证不同功能的Class可以访问相同的变量
class UString:
    lists = [] # 所有的结构化函数，内部item形如：{"name":"f","args":"x",text:"return x"}，其中name是函数名称，args为函数参数，即f（x）中的x，text为函数返回的表达式，即f(x)=x中等号右侧的部分
    t = 0 # 为默认函数下表，即每次新建函数时函数名称的下标，0为空
    f_n = ["f", "g", "h", "p", "q", "r", "s", "t"] # 默认函数，这些关键字是在新建函数时name字段的默认值
    a_e = [] # 已经存在的函数名称，防止重复命名函数
    width = 500 # 页面宽度，默认为500
    height = 600 # 页面高度，默认为600
    step = 25 # 步长，用于给出页面宽度像素与函数图像x轴的值的关系
    darkMode = {
        "SYSTEM": ThemeMode.SYSTEM,
        "LIGHT": ThemeMode.LIGHT,
        "DARK": ThemeMode.DARK
    } # flet 暗黑模式的映射
    resize = False # 帮助更新UI的函数确定为什么更新，如果该选项为True，则为页面大小更改时的更新
    matplot_chart = None # 全局的函数图像控件，在main_page.py中被赋予值

    def __init__(self, page: Page):
        UString.width = page.width
        UString.height = page.height
