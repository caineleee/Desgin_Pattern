#!/usr/bin/python
#coding=utf-8

'''

Creational Design Pattern(创建型设计模式）下的 Abstract Factory Pattern(抽象工厂模式） 使用实例。

abstract_factory_pattern.py 文件中的工厂模式存在几个缺点：

1 两个工厂都没有各自都状态，所以根本不需要创建工厂实例

2 SvgDiagramFactory 与 DiagramFactory都代码基本上一模一样 只不过前者使用make_diagrm方法调用都是SvgText实例，而后者返回Text实例
	这样产生许多重复代码。

3 DiagramFactory  Diagram  Rectangle  Text 类以及SVG 系列中与其对应都那些类都放在了"顶级命名空间"（top-level namespace）里
	但是我们根本不需要这样，因为我们只需要两个工厂。

4 给SVG Diagram 的组件类起名时，为了避免命名冲突，必须加上前缀才可以（例如： 表示SVG矩形的那个class叫SvgRectangle，而不能直接叫成Rectangle）

对之前的代码作出改进：

1 把Diagram/Rectangle/Text 等class都嵌入到DiagramFactory类中。 修改后需要用DiagramFactory.Diagram 来引用纯文本到Diagram class

2 SVG Diagram 那些 class 也嵌入到 SvgDiagramFactory中。 这样就不会产生命名冲突了，它们可以和纯文本系列的那些类同名。例如： 可以通过SvgDiagramFactory.Diagram
    来引用 SVG Diagram 。 而不必用 SvgDiagram这样的名字了。

3 给几个make_xxx 方法加 classmethod 装饰器。

'''


import os
import sys
import tempfile


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-P": # For regression testing
        create_diagram(DiagramFactory).save(sys.stdout)
        create_diagram(SvgDiagramFactory).save(sys.stdout)
        return
    textFilename = os.path.join(tempfile.gettempdir(), "diagram.txt")
    svgFilename = os.path.join(tempfile.gettempdir(), "diagram.svg")

    txtDiagram = create_diagram(DiagramFactory)
    txtDiagram.save(textFilename)
    print("wrote", textFilename)

    svgDiagram = create_diagram(SvgDiagramFactory)
    svgDiagram.save(svgFilename)
    print("wrote", svgFilename)


def create_diagram(factory):
    diagram = factory.make_diagram(30, 7)
    rectangle = factory.make_rectangle(4, 1, 22, 5, "yellow")
    text = factory.make_text(7, 3, "Abstract Factory")
    diagram.add(rectangle)
    diagram.add(text)
    return diagram


class DiagramFactory:

    @classmethod
    def make_diagram(Class, width, height):
        return Class.Diagram(width, height)


    @classmethod
    def make_rectangle(Class, x, y, width, height, fill="white",
            stroke="black"):
        return Class.Rectangle(x, y, width, height, fill, stroke)

    @classmethod
    def make_text(Class, x, y, text, fontsize=12):
        return Class.Text(x, y, text, fontsize)


    BLANK = " "
    CORNER = "+"
    HORIZONTAL = "-"
    VERTICAL = "|"


    class Diagram:

        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.diagram = DiagramFactory._create_rectangle(self.width,
                    self.height, DiagramFactory.BLANK)


        def add(self, component):
            for y, row in enumerate(component.rows):
                for x, char in enumerate(row):
                    self.diagram[y + component.y][x + component.x] = char


        def save(self, filenameOrFile):
            file = (None if isinstance(filenameOrFile, str) else
                    filenameOrFile)
            try:
                if file is None:
                    file = open(filenameOrFile, "w", encoding="utf-8")
                for row in self.diagram:
                    print("".join(row), file=file)
            finally:
                if isinstance(filenameOrFile, str) and file is not None:
                    file.close()


    class Rectangle:

        def __init__(self, x, y, width, height, fill, stroke):
            self.x = x
            self.y = y
            self.rows = DiagramFactory._create_rectangle(width, height,
                    DiagramFactory.BLANK if fill == "white" else "%")


    class Text:

        def __init__(self, x, y, text, fontsize):
            self.x = x
            self.y = y
            self.rows = [list(text)]


    def _create_rectangle(width, height, fill):
        rows = [[fill for _ in range(width)] for _ in range(height)]
        for x in range(1, width - 1):
            rows[0][x] = DiagramFactory.HORIZONTAL
            rows[height - 1][x] = DiagramFactory.HORIZONTAL
        for y in range(1, height - 1):
            rows[y][0] = DiagramFactory.VERTICAL
            rows[y][width - 1] = DiagramFactory.VERTICAL
        for y, x in ((0, 0), (0, width - 1), (height - 1, 0),
                (height - 1, width -1)):
            rows[y][x] = DiagramFactory.CORNER
        return rows


class SvgDiagramFactory(DiagramFactory):

    # The make_* class methods are inherited

    SVG_START = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"
    width="{pxwidth}px" height="{pxheight}px">"""

    SVG_END = "</svg>\n"

    SVG_RECTANGLE = """<rect x="{x}" y="{y}" width="{width}" \
height="{height}" fill="{fill}" stroke="{stroke}"/>"""

    SVG_TEXT = """<text x="{x}" y="{y}" text-anchor="left" \
font-family="sans-serif" font-size="{fontsize}">{text}</text>"""

    SVG_SCALE = 20


    class Diagram:

        def __init__(self, width, height):
            pxwidth = width * SvgDiagramFactory.SVG_SCALE
            pxheight = height * SvgDiagramFactory.SVG_SCALE
            self.diagram = [SvgDiagramFactory.SVG_START.format(**locals())]
            outline = SvgDiagramFactory.Rectangle(0, 0, width, height,
                    "lightgreen", "black")
            self.diagram.append(outline.svg)


        def add(self, component):
            self.diagram.append(component.svg)


        def save(self, filenameOrFile):
            file = (None if isinstance(filenameOrFile, str) else
                    filenameOrFile)
            try:
                if file is None:
                    file = open(filenameOrFile, "w", encoding="utf-8")
                file.write("\n".join(self.diagram))
                file.write("\n" + SvgDiagramFactory.SVG_END)
            finally:
                if isinstance(filenameOrFile, str) and file is not None:
                    file.close()


    class Rectangle:

        def __init__(self, x, y, width, height, fill, stroke):
            x *= SvgDiagramFactory.SVG_SCALE
            y *= SvgDiagramFactory.SVG_SCALE
            width *= SvgDiagramFactory.SVG_SCALE
            height *= SvgDiagramFactory.SVG_SCALE
            self.svg = SvgDiagramFactory.SVG_RECTANGLE.format(**locals())


    class Text:

        def __init__(self, x, y, text, fontsize):
            x *= SvgDiagramFactory.SVG_SCALE
            y *= SvgDiagramFactory.SVG_SCALE
            fontsize *= SvgDiagramFactory.SVG_SCALE // 10
            self.svg = SvgDiagramFactory.SVG_TEXT.format(**locals())


if __name__ == "__main__":
    main()
