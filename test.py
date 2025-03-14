"""
用于测试各种函数的先行版本.
测试好后会放到 Parts 或者 Projects 中.
个别早期版本和垃圾版本放到 Others 文件夹的 Old_Functions 和 Trash 中.
"""
import os
import re
import shutil

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pygame.examples.testsprite import use_rle
from sklearn.ensemble import IsolationForest # 去除离群值函数需要

from tkinter import Tk, filedialog
from tkinter.filedialog import askdirectory

import Parts as pt
import Projects as pjc


# 设置中文字体，解决字体显示问题
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 例如使用微软雅黑（SimHei）
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""-------------------全函数统一测试 (注意画图的函数 batch_analyze_data 需要到文件夹中自行查看画图结果)-------------------------"""
'''
修改任意函数后在此处可以快速解除注释并运行查看情况
'''
# #
# folder_path = './datas_learn/compare/d_B_compare2'
# file_path = './datas_learn/B00.xlsx'
# batch_path = './datas_learn/csv/csv2/xlsx'
#
# pjc.analyze_data(file_path)
# pjc.analyze_data_windowed()
#
# pjc.plot_multiple_files(folder_path)
# pjc.plot_multiple_files_windowed()
#
# pjc.analyze_data_OutlierRemoval(file_path)
# pjc.analyze_data_OutlierRemoval_windowed()
#
# pjc.iterate_fitting_OutlierRemoval(file_path)
# pjc.iterate_fitting_OutlierRemoval_windowed()

# pjc.batch_analyze_data(batch_path)
# pjc.batch_analyze_data_windowed()

"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""
'''
查看对数处理后的函数运行情况
'''
# #
# folder_path = './datas_learn/compare/d_B_compare2'
# file_path = './datas_learn/B00.xlsx'
# batch_path = './datas_learn/csv/csv2/xlsx'

# pjc.analyze_data(file_path, use_log=True)
# pjc.analyze_data_windowed(use_log=True)
#
# pjc.plot_multiple_files(folder_path, use_log=True)
# pjc.plot_multiple_files_windowed(use_log=True)
#
# pjc.analyze_data_OutlierRemoval(file_path, use_log=True)
# pjc.analyze_data_OutlierRemoval_windowed(use_log=True)
#
# pjc.iterate_fitting_OutlierRemoval(file_path, use_log=True)
# pjc.iterate_fitting_OutlierRemoval_windowed(use_log=True)
#
# # pjc.batch_analyze_data(batch_path, use_log=True)
# # pjc.batch_analyze_data_windowed(use_log=True)


"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""

# import os
# import shutil
# import re
#
# def sort_variable(root_dir, sort_standard=None, sort_all=False):
#     if not sort_standard and not sort_all:
#         print("No sort standard provided. Function will not execute.")
#         return
#
#     # 定义占位符规则
#     placeholder_map = {
#         'P': 'P',  # 走线类型
#         'd': 'd',  # 导线间距
#         'n': 'n',  # 序号
#         't': 't',  # 实验次数
#         'g': 'g',  # 实验组别
#         'e': 'e',  # 辐照注量
#         'v': 'v'   # 偏压
#     }
#
#     # 创建 compare_dir 目录
#     compare_dir = os.path.join(os.path.dirname(root_dir), f"compare_{sort_standard}")
#     os.makedirs(compare_dir, exist_ok=True)
#
#     # 遍历二级文件夹
#     for subdir, _, files in os.walk(root_dir):
#         for file in files:
#             if file.endswith('.xlsx'):
#                 file_path = os.path.join(subdir, file)
#                 file_name = os.path.basename(file_path)
#                 # 解析文件名
#                 pattern = re.compile(r'([TB]\d(?:\.\d)?)-(\d+)-(\d+)(\d+)-(\d+)(\d+)(?:\(.*\))?')
#                 match = pattern.match(file_name)
#                 if not match:
#                     continue
#
#                 # 提取文件名各部分
#                 layer_spacing = match.group(1)  # 走线类型和导线间距
#                 number = match.group(2)         # 序号
#                 experiment_num = match.group(3)  # 实验次数
#                 experiment_group = match.group(4)  # 实验组别
#                 fluence = match.group(5)        # 辐照注量
#                 bias = match.group(6)           # 偏压
#
#                 # 根据分类标准生成占位符
#                 if sort_standard:
#                     if sort_standard == 'P':  # 按走线类型分类
#                         group_key = f"{placeholder_map['P']}-{number}-{experiment_num}{experiment_group}-{fluence}{bias}"
#                     elif sort_standard == 'd':  # 按导线间距分类
#                         group_key = f"{layer_spacing[0]}{placeholder_map['d']}-{number}-{experiment_num}{experiment_group}-{fluence}{bias}"
#                     elif sort_standard == 'n':  # 按序号分类
#                         group_key = f"{layer_spacing}-{placeholder_map['n']}-{experiment_num}{experiment_group}-{fluence}{bias}"
#                     elif sort_standard == 't':  # 按实验次数分类
#                         group_key = f"{layer_spacing}-{number}-{placeholder_map['t']}{experiment_group}-{fluence}{bias}"
#                     elif sort_standard == 'g':  # 按实验组别分类
#                         group_key = f"{layer_spacing}-{number}-{experiment_num}{placeholder_map['g']}-{fluence}{bias}"
#                     elif sort_standard == 'e':  # 按辐照注量分类
#                         group_key = f"{layer_spacing}-{number}-{experiment_num}{experiment_group}-{placeholder_map['e']}{bias}"
#                     elif sort_standard == 'v':  # 按偏压分类
#                         group_key = f"{layer_spacing}-{number}-{experiment_num}{experiment_group}-{fluence}{placeholder_map['v']}"
#                     else:
#                         print(f"Invalid sort_standard: {sort_standard}")
#                         return
#                 else:
#                     # 如果 sort_standard 为 None，且 sort_all 为 True，则全分类
#                     group_key = f"{layer_spacing}-{number}-{experiment_num}{experiment_group}-{fluence}{bias}"
#
#                 # 创建分类文件夹并移动文件
#                 group_dir = os.path.join(compare_dir, group_key)
#                 os.makedirs(group_dir, exist_ok=True)
#                 shutil.move(file_path, os.path.join(group_dir, file_name))
#
#     # 清理空文件夹
#     for subdir, _, _ in os.walk(compare_dir):
#         if not os.listdir(subdir):
#             os.rmdir(subdir)
#
# # 分类文件
# root_dir = './datas_learn/sort_test/temp'
# sort_variable(root_dir, sort_standard='d')

"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""


# 分类文件
root_dir = './datas_learn/sort_test/test_2/all_data'

# pjc.sort_variable(root_dir, sort_standard='P')
# pjc.sort_variable(root_dir, sort_standard='d')
# pjc.sort_variable(root_dir, sort_standard='n')

# pjc.sort_variable(root_dir, sort_standard='t')
# pjc.sort_variable(root_dir, sort_standard='g')
# pjc.sort_variable(root_dir, sort_standard='e')
# pjc.sort_variable(root_dir, sort_standard='v')

pjc.sort_variable(root_dir, sort_standard=None, sort_all=True, ignore_list=['n', 'g'], move_single=True, draw_plot=True, use_log=True)

"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""

# import pandas as pd
#
# def analyze_data(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
#                  line_width=1.5, connect_points=False):
#     """
#     读取数据，进行多项式拟合并绘制结果，同时可以控制图表的细节和拟合的显示内容。
#
#     参数：
#     - file_path: Excel 文件的路径。
#     - degree: 多项式拟合的次数，默认3。
#     - show_equation: 是否在图中显示拟合函数表达式，默认显示。
#     - show_r_squared: 是否显示决定系数R²，默认显示。
#     - line_style: 曲线的线型，默认为 '--'（虚线）。
#     - line_color: 曲线的颜色，默认为 'r'（红色）。
#     - line_width: 曲线的线宽，默认为 1.5。
#     - connect_points: 是否连接原始数据点，默认不连接。(因为数据点较多, 不连接可以看出走势, 连接后观感不好)
#          - 但在数据点上下频繁跳动时, 连接数据点看得更加清楚 (特指辐照注量小的情况)
#     """
#
#     # 读取 Excel 文件, 提取电压电流数据
#     x, y = pt.read_xlsx(file_path)
#
#     # 多项式拟合
#     p, y_fit = pt.polynomial_fit(x, y, degree)
#
#     # 打印拟合的多项式系数
#     print(f"拟合多项式的系数（从高次到低次）: {p}")
#
#     # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
#     equation_str = pt.format_equation(p, degree)
#
#     # 计算 R²（决定系数）
#     r_squared = pt.calculate_r_squared(y,y_fit)
#
#     # 打印 R² 值
#     print(f"决定系数: R^2 = {r_squared:.12f}")  # 12位保证在拟合效果较好时能看出差距
#
#     # 作图, 原数据及拟合曲线
#     pt.plot_single(np.log10(x), y, y_fit, p, degree, show_equation, show_r_squared, line_style, line_color, line_width,
#                     connect_points)
#
# # pjc.analyze_data(file_path='./datas_learn/B00.xlsx',use_log=True)
#
# pjc.analyze_data_OutlierRemoval(file_path='./datas_learn/B00.xlsx', use_log=True)
#
# pjc.iterate_fitting_OutlierRemoval(file_path='./datas_learn/B00.xlsx', use_log=True)
