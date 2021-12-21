# 八数码问题

## 算法: 
	宽度优先搜索算法 (估计代价：h(n)＝0) //过慢，不建议使用
	A* 算法（估计代价：不在位数目 Misplaced Tile)
	A* 算法（估计代价：曼哈顿距离 Manhattan distance）

## 内容:   
	python语言
	用三种不同的估价函数计算八数码问题。
	可以处理默认的八数码或用户输入的八数码。
	可显示算法的生成结点数、扩展结点数、目标结点深度和计算时间。



## 测试用例:
	一些可以测试的八数码用例:
	
	1 3 2		1 2 3		0 1 2		8 7 1		
	4 8 0		4 8 0		4 5 3		6 0 2
	7 5 6		7 6 5		7 8 6		5 4 3
	
	以下是无法解决的用例，程序在报告失败前，会评估每个结点(~100,000)
	
	1 2 3
	4 5 6
	8 7 0

