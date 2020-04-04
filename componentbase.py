class ComponentBase:
    """
    组件基类
    """
    def __init__(self, component_info, container):
        """
        component_info: 字典格式，保存组件信息
        container: 对应组件所在容器的类实例
        """
        # 组件信息字典
        self.component_info = component_info
        # 是否不运行此组件
        self.is_ignored = self.component_info.get("is_ignored")
        # 组件对应类名
        self.classname = self.component_info.get("classname")
        # 类对应的函数名
        self.funcname = self.component_info.get("funcname")
        # 获取组件入参，用于操作容器中的变量
        # 判断入参和容器变量的关系，交给前端去做
        self.arguments = self.component_info.get("arguments")
        # 判断组件是否处于容器内
        self.container = container

    def run_code(self):
        # 希望子类能直接用自己的实例来调用它对应的funcname
        func = eval("self.{}".format(self.funcname))
        func()