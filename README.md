# RPA-JSON-flowfile-Interpreter-based-on-python

RPA软件在前端（设计器）通过组件拖拽的方式生成流程的标记语言：
* Uipath生成类似xml格式的称为xmal的标记语言
* 艺赛旗IS-RPA生成json格式的后缀为.seq和.ren的标记语言

之后后台服务会将标记语言编译为某种特定的代码文件，比如艺赛旗IS-RPA会利用python解释器将其编译为python脚本文件，再调用python解释器运行生成的python脚本文件。

本人的目标是设计一种新的架构，能够免去将标记语言编译为代码文件这一过程，直接由解释器解析标记语言并运行。
