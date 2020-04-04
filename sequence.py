import json
from collections import ChainMap
from componentbase import ComponentBase
from componentbasic import *

class Sequence(ComponentBase):
    """
    序列容器，也可以作为组件
    """
    def __init__(self, sequence_info, container):
        """
        sequence_info: 保存序列信息的字典
        """
        self.sequence_info = sequence_info
        # 序列比组件多两个参数：components和variables，少了funcname
        super().__init__(self.sequence_info, container)
        # 容器会将变量信息传递给内部所有组件
        if not self.container:
            self.variables = self.sequence_info.get("variables")
        else:
            # 如果该容器在另一个容器中，则同名变量以另一容器为准
            # 但是非同名变量就在该容器的variables中查找
            # 我们利用ChainMap来传递我们需要的作用域
            self.variables = ChainMap(
                self.container.variables, self.sequence_info.get("variables")) 
        # 将所有组件实例化并保存在列表中
        # self.components = []
        # for component_info in self.sequence_info.get("components"):
        #     self.components.append(eval("{}({}, self)".format(
        #         component_info.get("classname"), component_info)))
        
        # 生成器模式下每次调用都生成了新的局部作用域，locals()不再保存self实例信息，所以self实例提前用字典保存下来
        # 求值过程较为耗费资源，后续可以考虑先把各种情况都用compile预编译为字节码再调用eval执行
        self_dict = {"self": locals()["self"]}
        self.components = (eval("{}({}, self)".format(component_info.get(
            "classname"), component_info), globals(), self_dict) 
            for component_info in self.sequence_info.get("components"))

    def run_code(self):
        """
        容器类的运行逻辑和组件不同，需要重写方法
        """
        for component in self.components:
            if not component.is_ignored:
                component.run_code()


if __name__ == "__main__":
    json_path = r'C:\Users\yuryq\Desktop\test.json'
    with open(json_path,'r',encoding='utf-8') as f:
        sequence_info = json.load(f)
        s = Sequence(sequence_info, False)
    s.run_code()