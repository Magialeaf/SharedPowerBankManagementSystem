import math
from collections import defaultdict
"""
100282. 数组最后一个元素的最小值 显示英文描述 
给你两个整数 n 和 x 。你需要构造一个长度为 n 的 正整数 数组 nums ，
对于所有 0 <= i < n - 1 ，满足 nums[i + 1] 大于 nums[i] ，
并且数组 nums 中所有元素的按位 AND 运算结果为 x 。
返回 nums[n - 1] 可能的 最小 值。


示例 1：
输入：n = 3, x = 4
输出：6
解释：
数组 nums 可以是 [4,5,6] ，最后一个元素为 6 。

示例 2：
输入：n = 2, x = 7
输出：15
解释：
数组 nums 可以是 [7,15] ，最后一个元素为 15 。

"""


class Solution:
    def diagonalSort(self, mat):
        rows = len(mat)
        cols = len(mat[0])
        for row in range(rows - 1, -1, -1):
            col = 0
            lst = []
            while row < rows and col < cols:
                lst.append(mat[row][col])
                row += 1
                col += 1
            lst.sort()
            p = 0
            while row < rows and col < cols:
                mat[row][col] = lst[p]
                row += 1
                col += 1
                p += 1

        for col in range(1, cols):
            row = 0
            lst = []
            while row < rows and col < cols:
                lst.append(mat[row][col])
                row += 1
                col += 1
            lst.sort()
            p = 0
            while row < rows and col < cols:
                mat[row][col] = lst[p]
                row += 1
                col += 1
                p += 1

        return mat




s = Solution()
print(s.diagonalSort([[3, 3, 1, 1], [2, 2, 1, 2], [1, 1, 1, 2]]))
"""
1
11
101
111

101
111

4 = 100
5 = 101
6 = 110

1 = 1
2 = 10
3 = 101
4 = 1010
5 = 10101
6 = 101010
"""
