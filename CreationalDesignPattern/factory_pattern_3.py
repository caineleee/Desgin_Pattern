#!/usr/bin/python
#coding=utf-8

'''
factory pattern2 文件中 使用了 exec 内置函数, 但是这种方式风险很高,

所以必须要还一个更好的方式, 将其变为常量. 这个版本的棋子和颜色都是用常量.

并且使用了新的 create_piece() 方法来创建棋子.

这一版本中 create_piece() 工厂函数是 AbstractBorad class 的方法,

Checkerboard 与 ChessBoard 类都会继承它 .该方法接受两个常量做参数,根据棋子种类以及颜色

在静态的(也就是类级别的)字典中找到相对应的 class, 这个字典的key 是(piece,kind,color)二元组,

value 是类对象(class object). 找到值(也就是所需的 class)之后, 立即用()操作符将其实例化.

并返回创建好的棋子.

'''


import io
import itertools
import os
import sys
import tempfile
import unicodedata


DRAUGHT, PAWN, ROOK, KNIGHT, BISHOP, KING, QUEEN = ("DRAUGHT", "PAWN",
        "ROOK", "KNIGHT", "BISHOP", "KING", "QUEEN")
BLACK, WHITE = ("BLACK", "WHITE")


def main():
    checkers = CheckersBoard()
    print(checkers)

    chess = ChessBoard()
    print(chess)

    if sys.platform.startswith("win"):
        filename = os.path.join(tempfile.gettempdir(), "gameboard.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(sys.stdout.getvalue())
        print("wrote '{}'".format(filename), file=sys.__stdout__)


if sys.platform.startswith("win"):
    def console(char, background):
        return char or " "
    sys.stdout = io.StringIO()
else:
    def console(char, background):
        return "\x1B[{}m{}\x1B[0m".format(
                43 if background == BLACK else 47, char or " ")


class Piece(str):

    __slots__ = ()


# 知道了与棋子对应的字符及类名之后, 就可以用自定义的 make_new_method() 函数来创建 new() 函数(创建
# 好的函数将成为类的__new__() 方法) 在创建 new() 函数时不能调用 super() ,因为此处没有 supper()
# 函数所需要的类环境, 尽管 piece 类没有__new__()方法,但其基类 str 有,所以 make_new_method() 函数
# 所调用的 Piece.__new__() 实际上指的是 str.__new__().
def make_new_method(char): # Needed to create a fresh method each time
    def new(Class): # Can't use super() or super(Piece, Class)
        return Piece.__new__(Class, char)
    return new

# 不再用 factory_pattern1 & 2 中的 exce 和 eval 函数,但仍然是动态创建.
# Python 内置的 type() 函数创建新的类. 以这种方式创建类的时候,必须传入
# 类名称,含有基类名称的元组(piece) 以及含有类属性的字典. 在字典中,我们将__slots__ 属性设置为空元组.
# 并将__new__设置成刚才创建好的 new()函数
for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
    char = chr(code)
    name = unicodedata.name(char).title().replace(" ", "")
    if name.endswith("sMan"):
        name = name[:-4]
    new = make_new_method(char)
    Class = type(name, (Piece,), dict(__slots__=(), __new__=new))
    # 用内置函数 setattr() 把新创建的类(用 Class 变量表示,在创建白色的兵时, name 变量的 value
    # 就是'__classForPiece'中的 WhiteChessPawn) 添加到当前模块( sys.modules[__name__])中.
    setattr(sys.modules[__name__], name, Class) # Can be done better!


class AbstractBoard:

    __classForPiece = {(DRAUGHT, BLACK): BlackDraught,
            (PAWN, BLACK): BlackChessPawn,
            (ROOK, BLACK): BlackChessRook,
            (KNIGHT, BLACK): BlackChessKnight,
            (BISHOP, BLACK): BlackChessBishop,
            (KING, BLACK): BlackChessKing,
            (QUEEN, BLACK): BlackChessQueen,
            (DRAUGHT, WHITE): WhiteDraught,
            (PAWN, WHITE): WhiteChessPawn,
            (ROOK, WHITE): WhiteChessRook,
            (KNIGHT, WHITE): WhiteChessKnight,
            (BISHOP, WHITE): WhiteChessBishop,
            (KING, WHITE): WhiteChessKing,
            (QUEEN, WHITE): WhiteChessQueen}

    def __init__(self, rows, columns):
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.populate_board()


    def create_piece(self, kind, color):
        return AbstractBoard.__classForPiece[kind, color]()


    def populate_board(self):
        raise NotImplementedError()


    def __str__(self):
        squares = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                square = console(piece, BLACK if (y + x) % 2 else WHITE)
                squares.append(square)
            squares.append("\n")
        return "".join(squares)


class CheckersBoard(AbstractBoard):

    def __init__(self):
        super().__init__(10, 10)


    def populate_board(self):
        for x in range(0, 9, 2):
            for y in range(4):
                column = x + ((y + 1) % 2)
                for row, color in ((y, BLACK), (y + 6, WHITE)):
                    self.board[row][column] = self.create_piece(DRAUGHT,
                            color)


class ChessBoard(AbstractBoard):

    def __init__(self):
        super().__init__(8, 8)


    def populate_board(self):
        for row, color in ((0, BLACK), (7, WHITE)):
            for columns, kind in (((0, 7), ROOK), ((1, 6), KNIGHT),
                    ((2, 5), BISHOP), ((3,), QUEEN), ((4,), KING)):
                for column in columns:
                    self.board[row][column] = self.create_piece(kind,
                            color)
        for column in range(8):
            for row, color in ((1, BLACK), (6, WHITE)):
                self.board[row][column] = self.create_piece(PAWN, color)


if __name__ == "__main__":
    main()
