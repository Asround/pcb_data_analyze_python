"""
放置一些以后应该用不到的东西
一般是被淘汰或者替代的函数
"""
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest

from Parts import read_VA

# 设置中文字体，解决字体显示问题
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 例如使用微软雅黑（SimHei）
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 对应使用例 2
'''淘汰原因: 逐一指定文件路径太麻烦, 自定义选项不够多, 已有更好的替代'''
def plot_multiple_files(file_paths, colors=None, labels=None, line_styles=None, line_widths=None):
    """
    绘制多个文件的数据到同一张图中，方便对比。

    参数：
    - file_paths: 文件路径列表，例如 ["./file1.xlsx", "./file2.xlsx"]。
    - colors: 每个文件的曲线颜色列表，例如 ['b', 'r', 'g']。
    - labels: 每个文件的图例标签列表，例如 ["文件1", "文件2", "文件3"]。
    - line_styles: 每个文件的线型列表，例如 ['-', '--', ':']。
    - line_widths: 每个文件的线宽列表，例如 [1.5, 1.5, 1.5]。
    """
    # 设置默认值
    if colors is None:
        colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']  # 默认颜色列表
    if labels is None:
        labels = [f"文件 {i + 1}" for i in range(len(file_paths))]  # 默认标签
    if line_styles is None:
        line_styles = ['-'] * len(file_paths)  # 默认线型
    if line_widths is None:
        line_widths = [1.5] * len(file_paths)  # 默认线宽

    # 创建图表
    plt.figure(figsize=(10, 6))

    # 遍历文件路径列表
    for i, file_path in enumerate(file_paths):
        # 读取 Excel 文件
        xls = pd.ExcelFile(file_path)
        df = xls.parse(sheet_name=0)

        # if 判断实现不同文件均可读取
        x, y = read_VA(df)

        # 绘制数据
        plt.plot(x, y, linestyle=line_styles[i], color=colors[i], label=labels[i], linewidth=line_widths[i])

    # 图表设置
    plt.xlabel("电压 (V)")
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线对比")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()


# # 使用例 2：使用 plot_multiple_files 进行多文件对比
# file_paths = [
#     # "./datas_learn/compare1/B0.xlsx",
#     # "./datas_learn/compare1/B0.5.xlsx",
#     # "./datas_learn/compare1/B1.xlsx",
#
#     # "./datas_learn/B0.xlsx",
#     # "./datas_learn/B0.5.xlsx",
#     # "./datas_learn/B1.xlsx",
#
#     "./datas_learn/B0.xlsx",
#     "./datas_learn/B0.5.xlsx",
#     "./datas_learn/B1.xlsx",
#     "./datas_learn/B2.xlsx",
#     "./datas_learn/B4.xlsx",
#
# ]
#
# colors = ['b', 'r', 'g', 'k', 'm']  # 每个文件的曲线颜色
# labels = ["B0", "B0.5", "B1", "B2", "B4"]  # 每个文件的图例标签
# line_styles = ['-', '--', ':', '-', '--']  # 每个文件的线型
# line_widths = [1.5, 1.5, 1.5, 1.5, 1.5]  # 每个文件的线宽
#
# # colors = ['b', 'r']  # 每个文件的曲线颜色
# # labels = ["B0", "B0.5"]  # 每个文件的图例标签
# # line_styles = ['-', '--']  # 每个文件的线型
# # line_widths = [1.5, 1.5]  # 每个文件的线宽
#
# plot_multiple_files(file_paths, colors=colors, labels=labels, line_styles=line_styles, line_widths=line_widths)
