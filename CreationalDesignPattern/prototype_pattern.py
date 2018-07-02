#!/usr/bin/python
#coding=utf-8

'''
如果根据现有对象复制出新的对象,并对其修改,可以使用"原型模式"(Prototype pattern)

只要在运行期间能够确定其类型或者是 class name 我们就能够创建出实例来.

point1 是按照传统方式(也就是静态方式)创建的.

point2/point3/point4 把类名当做参数传给函数,由于 point3 和 point4 是所用的方法都很简单,
所以我们没有必要再向 point2 时那样使用有安全隐患的 eval 函数.

point3和 point4原理完全相同.

point5 是通过 make_object() 函数创建出来的,在调用这个函数时,传入了类对象和相关参数.

point6 采用经典的原型方式创建,首先根据现有对象复制出新对象,然后在新对象上执行初始化或配置操作.

point7 是用 point1的类对象的创建出来的. 创建时传入了新的参数.
'''

import sys,copy

class Point:
	__slots__ = ('x','y')
	def __init__(self,x,y):
		self.x = x
		self.y = y



#可以通过7中方式都能创建出新的 Point 对象.
def make_object(Class,*args,**kwargs):
	return Class(*args,**kwargs)

point1 = Point(1,2)
point2 = eval('{}{},{}'.format('Point',2,4))
point3 = getattr(sys.modules[__name__],'Point')(3,6)
point4 = globals()['Point'](4,8)
point5 = make_object(Point,5,10)
point6 = copy.deepcopy(point5)
point6.x = 6
point6.y = 12
point7 = point1.__class__(7,12)