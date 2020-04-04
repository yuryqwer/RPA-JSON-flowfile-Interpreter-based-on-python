from componentbase import ComponentBase

class OutPut(ComponentBase):
    """
    用于输出的组件
    """
    def __init__(self, component_info, container):
        super().__init__(component_info, container)

    def output(self):
        # print(self.arguments, '->', self.container.variables.get(self.arguments))
        # 还有一种方法是如果打印变量的值，就在json的arguments中用特殊记号
        # 比如Uipath中用中括号标记变量
        print(eval(self.arguments, {}, self.container.variables))


class Assign(ComponentBase):
    """
    用于赋值的组件，支持多重赋值
    """
    def __init__(self, component_info, container):
        super().__init__(component_info, container)

    def assign(self):
        # 对dict和ChainMap对象要分情况
        # 如果组件所在容器不含嵌套则直接赋值
        if isinstance(self.container.variables, dict):
            self.container.variables.update(self.arguments)
        # 否则按一定规则赋值
        # 规则：对于需要赋值的每一组键值对，在ChainMaps.maps中先找到就先赋值
        else:
            maps = self.container.variables.maps
            for dic in maps:
                for k in self.arguments:
                    if k in dic:
                        dic.update([(k, self.arguments[k])])
                    else:
                        pass


class IfStatement(ComponentBase):
    """
    判断分支
    """
    def __init__(self, component_info, container):
        # 判断比组件基类少了funcname，但是直接初始化也不要紧
        super().__init__(component_info, container)
        # 这边需要思考一下要不要variables变量
        # 本着能不要就尽量不要的原则，这边先不设置

        # 获取真假分支对应的组件
        branch_true = self.component_info.get("branch_true")
        branch_false = self.component_info.get("branch_false")
        # 把自己所在的容器作为容器传递给真假分支，全局和局部作用域字典需要思考一下
        # 根据计算这边对两个分支（都只含一个组件）进行求值花费0.001秒左右
        self.branch_true = eval("{}({}, container)".format(branch_true.get(
            "classname"), branch_true), globals(), {"container": self.container})
        self.branch_false = eval("{}({}, container)".format(branch_false.get(
            "classname"), branch_false), globals(), {"container": self.container})

    def run_code(self):
        # 对判断组件进行求值时，作用域需要思考一下
        if eval(self.arguments, {}, self.container.variables):
            self.branch_true.run_code()
        else:
            self.branch_false.run_code()