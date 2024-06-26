from basic.app_str import UString
from sympy import *


def exec_plain(args, plain):
    exec("""
def result({}):
    y = {}
    return y
""".format(args, plain))
    return locals()["result"]


class DefineUserFunction:

    def __init__(self):
        self.function = UString.lists

    def exec(self, name: str, args):
        for i in self.function:
            if i["mode"] == "fx":
                if i["name"] == name:
                    fn = {
                        "name": i["name"],
                        "args": i["args"],
                        "code": "def user_function_{}({}):return {}".format(i["name"], i["args"], i["text"])
                    }
                    exec(fn["code"])
                    _args = [x.replace(" ", "") for x in i["args"].split(",")]
                    exec_args = ""
                    for a in _args:
                        exec_args = exec_args + "{}={}".format(a, args[a])
                    exec("result = user_function_{}({})".format(i["name"], exec_args))
                    return_r = locals()["result"]
                    return return_r
