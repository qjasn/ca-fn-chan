from flet_core import Page, ThemeMode


# 此Class用来存放全局变量，以保证不同功能的Class可以访问相同的变量
class UString:
    y_offset = 0
    x_offset = 0
    display_step = 2
    lists = []  # 所有的结构化函数/方程，内部item形如：
    # {"mode":"fx"."name":"f","args":"x",text:"x",color:"white"}
    # {"mode":"equ","equ":"x = 1","args":"x"}
    # {"mode":"point","name":"A","x":1,"y":2}
    # mode为fx时，其中name是函数名称，args为函数参数，即f（x）中的x，text为函数返回的表达式，即f(x)=x中等号右侧的部分
    t = 0  # 为默认函数下表，即每次新建函数时函数名称的下标，0为空
    f_n = ["f", "g", "h", "p", "q", "r", "s", "t"]  # 默认函数，这些关键字是在新建函数时name字段的默认值,f_n即function name
    a_e = []  # 已经存在的函数名称，防止重复命名函数，a_e即already exist
    p_e = []
    p_n = ["A", "B", "C", "D", "E", "F", "G"]  # 默认Point，这些关键字是在新建函数时name字段的默认值,point name
    p_t = 0
    width = 500  # 页面宽度，默认为500
    height = 600  # 页面高度，默认为600
    step = 25  # 步长，用于给出页面宽度像素与函数图像x轴的值的关系
    darkMode = {
        "SYSTEM": ThemeMode.SYSTEM,
        "LIGHT": ThemeMode.LIGHT,
        "DARK": ThemeMode.DARK
    }  # flet 暗黑模式的映射
    resize = False  # 帮助更新UI的函数确定为什么更新，如果该选项为True，则为页面大小更改时的更新
    matplot_chart = None  # 全局的函数图像控件，在main_page.py中被赋予值
    nav_change = False  # 在路由更改时为True
    main_page_control = None  # MainPage的总控
    math_list = None  # 数学公式的添加与UI构建控制
    change_dark = False  # 在页面显示模式更改时为True
    draw_class = {}  # 所有的实例化函数
    python_repl = None

    def __init__(self, page: Page):
        UString.width = page.width
        UString.height = page.height
