#coding=UTF-8
########################################################################################
#   Author:     杨怡婧 
#
#   Algorithms: 宽度优先搜索算法 (估价函数：h(n)＝0)
#				A* 算法（估价函数：不在位数目 Misplaced Tile)
#				A* 算法（估价函数：曼哈顿距离 Manhattan distance）
#########################################################################################

import copy
import time
from pip._vendor.distlib.compat import raw_input

GOALSEQ = [1, 2, 3, 4, 5, 6, 7, 8, 0]
GOALIND = [(0, (2, 2)), (1, (0, 0)), (2, (0, 1)), (3, (0, 2)), (4, (1, 0)), (5, (1, 1)), (6, (1, 2)), (7, (2, 0)), (8, (2, 1))]

###########################################################################################################################
###########################################################################################################################

class Node:

	#初始化结点
	def __init__(self, data):
		self.data = data  
		self.child = [None, None, None, None]
		self.g_n = 0
		self.h_n = 0
		self.state = "notgoal"

	#计算估价函数（ misplaced tile ）
	def h_n_misplaced(self):
		h_n = 0
		k = 0
		
		#确定不在目标位置的数字 
		for i in range(len(self.data)):
			for j in range(len(self.data)):
				if self.data[i][j] != GOALSEQ[k] and self.data[i][j] != 0:
					h_n += 1
				k +=1

		if h_n == 0:
			self.state = "goal"
			
		self.h_n = h_n
		
		
	# 计算估价函数（ manhattan ）
	def h_n_manhattan(self):

		h_n = 0
		k = 0

		# 检查每一个数字是否和 GOALSEQ 一致，如果不一致， h(n) += | [x][y] - [i][i] |
		# [x][y]为数字应该在的位置 
		#[i][j]为目前位置
		
		for i in range(len(self.data)):
			for j in range(len(self.data)):
				if self.data[i][j] == 0:
					k = k + 1
					continue
				if self.data[i][j] != GOALSEQ[k]:
					num = self.data[i][j]
					x = GOALIND[num][1][0]
					y = GOALIND[num][1][1]
						  
					distance = abs(x - i) + abs(y - j)
					h_n = h_n + distance
				#endif
				k = k + 1
			#endfor
		#endfor

		if h_n == 0:
			self.state = "goal"
						  
		self.h_n = h_n
						  
		#enddef
		
						  
	def create_children(self, choice):

		#确定可能的移动，为每一次移动创建结点（Node），将其加入队列（queue）
		blank_index = (0, 0)

		# ------ 确定空白位置------#
		for i in range(len(self.data)):
			for j in range(len(self.data)):
				if self.data[i][j] == 0:
					blank_index = (i, j)

		i = blank_index[0]
		j = blank_index[1]


		#------- 向右移动空白格，如果可以-----------------------------------------------
		if j < (len(self.data) - 1):
			#可以右移
			self.child[3] = Node(self.data)
			self.child[3] = copy.deepcopy(self)

			#交换空格
			temp = self.child[3].data[i][j+1]
			self.child[3].data[i][j+1] = 0
			self.child[3].data[i][j] = temp

			#设置 g(n)
			self.child[3].g_n = self.g_n + 1
			
			#设置 h(n)
			if choice == 1:
				self.child[3].h_n = 0
			if choice == 2:
				self.child[3].h_n_misplaced()
			if choice == 3:
				self.child[3].h_n_manhattan()
		else:
			
			self.child[3] = None



		#------- 向左移动空白格，如果可以 ------------------------------------------------
		if j != 0:
			#可以左移
			self.child[2] = Node(self.data)
			self.child[2] = copy.deepcopy(self)

			#交换空格
			temp = self.child[2].data[i][j-1]
			self.child[2].data[i][j-1] = 0
			self.child[2].data[i][j] = temp
			
			#设置 g(n)
			self.child[2].g_n = self.g_n + 1
			#设置 h(n)
			if choice == 1:
				self.child[2].h_n = 0
			if choice == 2:
				self.child[2].h_n_misplaced()
			if choice == 3:
				self.child[2].h_n_manhattan()
		else:
			self.child[2] = None



		#------- 向下移动空白格，如果可以 ------------------------------------------------
		if i < (len(self.data) - 1):
			#可以下移
			self.child[1] = Node(self.data)
			self.child[1] = copy.deepcopy(self)

			#交换空格
			temp = self.child[1].data[i+1][j]
			self.child[1].data[i+1][j] = 0
			self.child[1].data[i][j] = temp

			#设置 g(n)
			self.child[1].g_n = self.g_n + 1
			
			#设置 h(n)
			if choice == 1:
				self.child[1].h_n = 0
			if choice == 2:
				self.child[1].h_n_misplaced()
			if choice == 3:
				self.child[1].h_n_manhattan()
		else:
			self.child[1] = None
		

		#------- 向上移动空白格，如果可以 -------------------------------------------------
		if i != 0:
			#可以上移
			self.child[0] = Node(self.data)
			self.child[0] = copy.deepcopy(self)

			#交换空格
			temp = self.child[0].data[i-1][j]
			self.child[0].data[i-1][j] = 0
			self.child[0].data[i][j] = temp

			#设置 g(n)
			self.child[0].g_n = self.g_n + 1
			
			#设置 h(n)
			if choice == 1:
				self.child[0].h_n = 0
			if choice == 2:
				self.child[0].h_n_misplaced()
			if choice == 3:
				self.child[0].h_n_manhattan()
		else:
			self.child[0] = None


	#计算估价函数 f(n) = g(n) + h(n)
	def f_n(self):
		fx = self.g_n + self.h_n
		return fx



###########################################################################################################################

def f(node):
	fx = node.g_n + node.h_n
	return fx

###########################################################################################################################

def goal_found(max_nodes, node_depth, count):
	print("完成!!!!!!!")
	print()						  
	print('扩展结点数为 ', count)
	print('生成结点数为 ', max_nodes)
	print('目标结点的深度为 ', node_depth,'\n\n')
	
	return

###########################################################################################################################

def print_node(node):
		#打印当前结点状态
	
	if node is None:
		return
	else:
		for x in range(len(node.data)):
			s = ''
			for y in range(len(node.data)):
				s = s + str(node.data[x][y])
				s = s + ' '
			s = s + '\n'
			print(s)

###########################################################################################################################

# 搜索算法

def solve_puzzle(puzzle, choice):
	#goal = None
	
	closed_list = []
	open_list = []
	
	open_list.append(Node(puzzle))
	
	max_nodes = 0
	count = 0

###########################################################

	while len(open_list) != 0:
		#推出open表的第一个结点
		node = open_list.pop(0)


		#检查它是否重复
		for m in range(len(closed_list)):
			if node.data == closed_list[m].data:
				node = open_list.pop(0)
		
		#检查是否是目标结点
		if node.state == "goal":
			goal_found(max_nodes, node.g_n, count)
			return


		#扩展结点，得到后继结点
		node.create_children(choice)
		count += 1

		#将非空后继结点加入open表
		for x in range(4):
			if node.child[x] is not None:
					open_list.insert(0, node.child[x])
					
		#利用 f(n) = g(n) + h(n) 对open表重新排序
		new = sorted(open_list, key=f)
		open_list = new
		
		if max_nodes < len(open_list):
			max_nodes = len(open_list)

		#将父结点加入close表
		
		print('扩展结点------ g(n) = ', node.g_n, '   h(n) = ', node.h_n, '...\n')
		print_node(node)
		print('\n')

		closed_list.append(node)
	#endwhile

	print('失败!')



###########################################################################################################################

def get_input():
	
	ret = list()
	input_type = int(input(" 1.使用默认的八数码\n 2.使用输入的八数码 \n "))

	num = ['1', '2', '3']
	i = 0

	#使用默认的八数码-------------------------------------------------------------------------------------------------------
	if input_type == 1:
		ret = [[1, 2, 3], [4, 8, 0], [7, 6, 5]]
		print('\n')
				
		print('请选择算法: \n', '1. 宽度优先搜索算法 (估计代价：h(n)＝0) [速度过慢，不建议使用]\n', '2. A* 算法（估计代价：不在位数目 Misplaced Tile)')
		print(' 3. A* 算法（估计代价：曼哈顿距离 Manhattan distance）\n\n')
						
		choice = raw_input()
		choice = int(choice)
								
		print('\n')
		return ret, choice
	#输入八数码-------------------------------------------------------------------------------------------------
	elif input_type == 2:
		
		#获取输入，存到ret中
		while i < 3:
			
			print('请输入第', num[i], '行, 用空格分开: ')
			
			#检索行，形成数字数组
			arr = raw_input().split()
			
			#转换成int
			arr = [int(x) for x in arr]
			
			#检查用户是否是输入了三个数字，否则报错
			if len(arr) > 3:
				print("Error: 参数过多")
				quit(1)
			if len(arr) < 3:
				print("Error: 参数太少")
				quit(1)
			
			#将输入的数字添加到最终数组中
			ret.append(arr)
			
			#循环直到执行3次
			i = i + 1
		#endwhile
		
		#检查矩阵是否有重复元素
		sum = 0
		for x in range(3):
			sum += ret[0][x]
			sum += ret[1][x]
			sum += ret[2][x]
		
		if sum != 36:
			print("\nError: 检查到有重复数字... 请重新输入\n")
			get_input()
		
		print('\n')

		print('请选择算法: \n', '1. 宽度优先搜索算法 (估计代价：h(n)＝0)[速度过慢，不建议使用]\n', '2. A* 算法（估计代价：不在位数目 Misplaced Tile)')
		print(' 3. A* 算法（估计代价：曼哈顿距离 Manhattan distance）\n\n')

		choice = raw_input()
		choice = int(choice)
			
		print('\n')

		return ret, choice
	else:
		print("error: 无效输入")
		quit(1)




###########################################################################################################################

def main():

	print("\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~ 八数码 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	puzzle, choice = get_input()
	
	
	#在搜索过程中运行
	start = time.time()
	solve_puzzle(puzzle, choice)
	end = time.time()
	
	algtime = end - start
	
	print ('完成时间 ： ', str(algtime), ' 秒.')

	print("\n")

if __name__ == '__main__':
	main()

