#!/usr/bin/python
#coding=utf-8


'''
Factory Pattern (工厂模式）

如果子类的某个方法要根据情况来决定用什么类去实例化相关对象，可以使用工厂模式。

此模式可以单独使用，也可以在无法预知对象类型的时候使用。（比如：待初始化的对象，
类型要从文件中读取， 或是由用户来输入）

实例：

编写一段棋盘生成程序， 用于生成国际跳棋和国际象棋的棋盘。

棋盘对象包含一份儿二维列表，其中每一个一维列表都表示棋盘中都一行，
而一维列表中都元素则表示行中对应单元格上都棋子， 如果某个格子上没有棋子，
那么对应都元素就是 None 。
'''

import io
import os
import sys
import tempfile

# 用于表示棋盘格子的背景色。 这行代码本来按照惯例写成 BLACK，WHITE = range（2），但是用字符串来定义常量在调试时更容易联储错误信息的含义
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
		'''
		 返回都字符串用于表示棋子及背景颜色， 函数所返回都字符串里会包含转译符，
		 用于修改字符都背景色。
		:param char:
		:param background:
		:return:
		'''
		return char or " "


	sys.stdout = io.StringIO()
else:
	def console(char, background):
		''' 同上 '''
		return "\x1B[{}m{}\x1B[0m".format(
			43 if background == BLACK else 47, char or " ")


class AbstractBoard:

	def __init__(self, rows, columns):
		self.board = [[None for _ in range(columns)] for _ in range(rows)]
		self.populate_board()

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
			for row in range(4):
				column = x + ((row + 1) % 2)
				self.board[row][column] = BlackDraught()
				self.board[row + 6][column] = WhiteDraught()


class ChessBoard(AbstractBoard):

	def __init__(self):
		super().__init__(8, 8)

	def populate_board(self):
		self.board[0][0] = BlackChessRook()
		self.board[0][1] = BlackChessKnight()
		self.board[0][2] = BlackChessBishop()
		self.board[0][3] = BlackChessQueen()
		self.board[0][4] = BlackChessKing()
		self.board[0][5] = BlackChessBishop()
		self.board[0][6] = BlackChessKnight()
		self.board[0][7] = BlackChessRook()
		self.board[7][0] = WhiteChessRook()
		self.board[7][1] = WhiteChessKnight()
		self.board[7][2] = WhiteChessBishop()
		self.board[7][3] = WhiteChessQueen()
		self.board[7][4] = WhiteChessKing()
		self.board[7][5] = WhiteChessBishop()
		self.board[7][6] = WhiteChessKnight()
		self.board[7][7] = WhiteChessRook()
		for column in range(8):
			self.board[1][column] = BlackChessPawn()
			self.board[6][column] = WhiteChessPawn()


class Piece(str):
	# __slots__ 用来限制 给本class绑定成员变量与成员方法,赋值为空元组将不可后续绑定任何成员变量与方法
	__slots__ = ()


class BlackDraught(Piece):
	# sub class 无法继承 upper的 __slots__ . 需要重新定义 __slots__
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{black draughts man}")


class WhiteDraught(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{white draughts man}")


class BlackChessKing(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{black chess king}")


class WhiteChessKing(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{white chess king}")


class BlackChessQueen(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{black chess queen}")


class WhiteChessQueen(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{white chess queen}")


class BlackChessRook(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{black chess rook}")


class WhiteChessRook(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{white chess rook}")


class BlackChessBishop(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{black chess bishop}")


class WhiteChessBishop(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{white chess bishop}")


class BlackChessKnight(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{black chess knight}")


class WhiteChessKnight(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{white chess knight}")


class BlackChessPawn(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{black chess pawn}")


class WhiteChessPawn(Piece):
	__slots__ = ()

	def __new__(Class):
		return super().__new__(Class, "\N{white chess pawn}")


if __name__ == "__main__":
	main()
