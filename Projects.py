"""
存放各类项目的单体
"""
import os
import shutil
import re

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest

from tkinter import Tk, filedialog
from tkinter.filedialog import askdirectory

import Projects as pjc
import Parts as pt

# 设置中文字体，解决字体显示问题
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 例如使用微软雅黑（SimHei）
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

''' --------------------------------------- 1(1). 单个表格画图分析函数 --------------------------------------------------'''


def analyze_data(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
                 line_width=1.5, connect_points=False, use_log=False):
    """
    读取数据，进行多项式拟合并绘制结果，同时可以控制图表的细节和拟合的显示内容。

    参数：
    - file_path: Excel 文件的路径。
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '--'（虚线）。
    - line_color: 曲线的颜色，默认为 'r'（红色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - connect_points: 是否连接原始数据点，默认不连接。(因为数据点较多, 不连接可以看出走势, 连接后观感不好)
         - 但在数据点上下频繁跳动时, 连接数据点看得更加清楚 (特指辐照注量小的情况)
    """

    # 读取 Excel 文件, 提取电压电流数据
    x, y = pt.read_xlsx(file_path)

    # 多项式拟合
    p, y_fit = pt.polynomial_fit(x, y, degree)

    # 打印拟合的多项式系数
    print(f"拟合多项式的系数（从高次到低次）: {p}")

    # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
    equation_str = pt.format_equation(p, degree)

    # 计算 R²（决定系数）
    r_squared = pt.calculate_r_squared(y,y_fit)

    # 打印 R² 值
    print(f"决定系数: R^2 = {r_squared:.12f}")  # 12位保证在拟合效果较好时能看出差距

    # 作图, 原数据及拟合曲线
    pt.plot_single(x, y, y_fit, p, degree, show_equation, show_r_squared, line_style, line_color, line_width,
                    connect_points,use_log)


# # 使用例 : 以下两个路径分别对应不同类型的xlsx文件, 可分别运行测试
# file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径(一定要是.xlsx文件!)
# # file_path = "./datas_learn/B4.xlsx"  # 替换为你自己的文件路径(一定要是.xlsx文件!)
#
# # 分析file_path对应路径的文件, 用3次多项式进行拟合, 拟合多项式表达式和决定系数均展示, 拟合曲线的线型为虚线, 红色, 宽度为1
# analyze_data(file_path, degree=3, show_equation=False, show_r_squared=True, line_style='--', line_color='r',
#              line_width=1, connect_points=True)

''' --------------------------------------- 1(2). 单个表格画图分析函数(弹窗选择路径) -------------------------------------'''


def analyze_data_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
                          line_width=1.5, connect_points=False, use_log= False):
    """
    通过弹窗选择文件路径，读取数据，进行多项式拟合并绘制结果。

    参数：
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '--'（虚线）。
    - line_color: 曲线的颜色，默认为 'r'（红色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - connect_points: 是否连接原始数据点，默认不连接。
    """
    # 弹窗选择文件
    file_path = pt.select_file()
    if not file_path:
        # 如果没有选取文件或者读取失败, 通知用户
        print("未选择文件。")
        return

    # 读取 Excel 文件, 提取电压电流数据
    x, y = pt.read_xlsx(file_path)

    # 多项式拟合
    p, y_fit = pt.polynomial_fit(x, y, degree)

    # 计算 R²（决定系数）
    r_squared = pt.calculate_r_squared(y,y_fit)

    # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
    equation_str =pt.format_equation(p, degree)

    # 作图, 原数据及拟合曲线
    pt.plot_single(x, y, y_fit, p, degree, show_equation, show_r_squared, line_style, line_color, line_width,
                    connect_points, use_log)


# # 使用例
# analyze_data_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
#                          line_width=1.5, connect_points=False)

''' ------------------------------------- 2(1). 多个表格同一张图进行比较(无窗口, 需指定路径) --------------------------------'''


def plot_multiple_files(folder_path, colors=None, labels=None, line_styles=None, line_widths=None, use_log=False):
    """
    绘制文件夹中所有 Excel 文件的数据到同一张图中，方便对比。

    参数：
    - folder_path: 文件夹路径，例如 "./data"。
    - colors: 每个文件的曲线颜色列表，例如 ['b', 'r', 'g']。
    - labels: 每个文件的图例标签列表，例如 ["文件1", "文件2", "文件3"]。
    - line_styles: 每个文件的线型列表，例如 ['-', '--', ':']。
    - line_widths: 每个文件的线宽列表，例如 [1.5, 1.5, 1.5]。
    """
    # 获取文件夹中的所有 Excel 文件
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]

    # 设置默认值
    if colors is None:
        colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k'] * (len(file_paths))  # 默认颜色列表
    if labels is None:
        labels = [os.path.splitext(os.path.basename(f))[0] for f in file_paths]  # 默认标签为文件名
    if line_styles is None:
        line_styles = ['-'] * len(file_paths)  # 默认线型
    if line_widths is None:
        line_widths = [1.5] * len(file_paths)  # 默认线宽

    # 创建图表
    plt.figure(figsize=(10, 6))

    # 对数化处理
    if use_log:
        x_label = "电压-log10 (V)"
    else:
        x_label = "电压 (V)"

    # 遍历文件路径列表
    for i, file_path in enumerate(file_paths):
        # 读取 Excel 文件, 提取电压电流数据
        x, y = pt.read_xlsx(file_path)

        if use_log:
            x = np.log10(x)

        # 绘制数据
        plt.plot(x, y, linestyle=line_styles[i], color=colors[i], label=labels[i], linewidth=line_widths[i])


    # 图表设置
    plt.xlabel(x_label)
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线对比")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()


# # 使用例
# folder_path = './datas_learn/compare/compare2'  # 替换为你的文件夹路径
# # folder_path = './datas_learn/compare/compare1'  # 替换为你的文件夹路径
# plot_multiple_files(folder_path, colors=None, labels=None, line_styles=None, line_widths=None)

''' ------------------------------------- 2(2). 多个表格同一张图进行比较(弹窗选择路径) -------------------------------------'''


def plot_multiple_files_windowed(colors=None, labels=None, line_styles=None, line_widths=None, use_log=False):
    """
    通过弹窗选择文件夹，绘制文件夹中所有 Excel 文件的数据到同一张图中，方便对比。

    参数：
    - colors: 每个文件的曲线颜色列表，例如 ['b', 'r', 'g']。
    - labels: 每个文件的图例标签列表，例如 ["文件1", "文件2", "文件3"]。
    - line_styles: 每个文件的线型列表，例如 ['-', '--', ':']。
    - line_widths: 每个文件的线宽列表，例如 [1.5, 1.5, 1.5]。
    """
    # 弹窗选择文件夹
    folder_path = pt.select_folder()
    if not folder_path:
        print("未选择文件夹。")
        return

    # 获取文件夹中的所有 Excel 文件
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]

    # 设置默认值
    if colors is None:
        colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k'] * (len(file_paths))  # 默认颜色列表
    if labels is None:
        labels = [os.path.splitext(os.path.basename(f))[0] for f in file_paths]  # 默认标签为文件名
    if line_styles is None:
        line_styles = ['-'] * len(file_paths)  # 默认线型
    if line_widths is None:
        line_widths = [1.5] * len(file_paths)  # 默认线宽

    # 创建图表，设置固定大小
    plt.figure(figsize=(10, 6))  # 设置图表大小为 10x6 英寸

    # 对数化处理
    if use_log:
        x_label = "电压-log10 (V)"
    else:
        x_label = "电压 (V)"

    # 遍历文件路径列表
    for i, file_path in enumerate(file_paths):
        # 读取 Excel 文件, 提取电压电流数据
        x, y = pt.read_xlsx(file_path)

        # 对数化处理
        if use_log:
            x = np.log10(x)

        # 绘制数据
        plt.plot(x, y, linestyle=line_styles[i], color=colors[i], label=labels[i], linewidth=line_widths[i])

    # 图表设置
    plt.xlabel(x_label)
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线对比")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()


# # 使用例
# plot_multiple_files_windowed(colors=None, labels=None, line_styles=None, line_widths=None)


''' ------------------------------------- 3(1). 多个表格批量画图保存到文件夹(指定路径) -------------------------------------'''


def batch_analyze_data(folder_path, output_folder=None, degree=3, show_equation=True, show_r_squared=True,
                       line_style='--',line_color='r', line_width=1.5, connect_points=False, use_log=False):
    """
    批量处理文件夹中的 Excel 文件，进行多项式拟合并保存图像。

    参数：
    - folder_path: 包含 Excel 文件的文件夹路径。
    - output_folder: 保存图像的文件夹路径。如果为 None，将默认生成一个以'文件夹名_img'命名的子文件夹。
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '--'（虚线）。
    - line_color: 曲线的颜色，默认为 'r'（红色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - connect_points: 是否连接原始数据点，默认不连接。
    """
    # 如果未传入output_folder，生成一个默认路径
    if output_folder is None:
        folder_name = os.path.basename(folder_path.rstrip(os.sep))  # 获取文件夹的名称
        output_folder = os.path.join(folder_path, f"{folder_name}_{degree}degree_img")  # 拼接文件夹名称 + "_img"

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历文件夹中的所有 Excel 文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            file_path = os.path.join(folder_path, file_name)
            # 调用 analyze_data_no_display 函数生成图像
            fig = pt.analyze_data_no_display(file_path, degree, show_equation, show_r_squared, line_style, line_color,
                                          line_width, connect_points,use_log)
            # 保存图像
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.png")
            fig.savefig(output_file_path, dpi=240)
            plt.close(fig)
            print(f"已保存图像: {output_file_path}")
    print('分析完成.')


# # 使用例
# folder_path = './datas_learn/many1'
# batch_analyze_data(folder_path, degree= 3, line_style='--', line_color='r', connect_points=False)

''' ------------------------------------- 3(2). 多个表格批量画图保存到文件夹(弹窗选择路径) --------------------------------'''


def batch_analyze_data_windowed(output_folder=None, degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                line_color='r', line_width=1.5, connect_points=False, use_log=False):
    """
    通过弹窗选择文件夹，批量处理文件夹中的 Excel 文件，进行多项式拟合并保存图像。
    需要: from tkinter import Tk, filedialog

    参数：
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '--'(虚线)。
    - line_color: 曲线的颜色，默认为 'r'（红色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - connect_points: 是否连接原始数据点，默认不连接。
    """
    # 弹窗选择文件夹
    folder_path = pt.select_folder()
    if not folder_path:
        print("未选择文件夹。")
        return

    # 创建输出文件夹
    if output_folder is None:
        output_folder = os.path.join(folder_path, f"{os.path.basename(folder_path)}_{degree}degree_img")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历文件夹中的所有 Excel 文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            file_path = os.path.join(folder_path, file_name)
            # 调用 analyze_data_no_display 函数生成图像
            fig = pt.analyze_data_no_display(file_path, degree, show_equation, show_r_squared, line_style,
                                             line_color,line_width, connect_points,use_log)

            # 保存图像
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.png")
            plt.savefig(output_file_path, dpi=240)
            plt.close()
            print(f"已保存图像: {output_file_path}")

    print('分析完成.')


# # 使用弹窗选择文件夹路径并批量分析
# batch_analyze_data_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--',
#                             line_color='r', line_width=1.5, connect_points=False)

''' ------------------------------------- 3(3). 多文件夹多表格批量画图保存到文件夹(指定路径) --------------------------------'''

def plot_multiple_folders(base_folder, use_log=False):
    '''
    base_folder: 一级文件夹
    一级文件夹下有许多装有 xlsx表格的二级文件夹,
    函数会依次读取二级文件夹的文件夹路径, 并以之为参数传给 pt.plot_multiple_files_no_display函数画图
    画图后将图片统一存储到一级文件夹目录下的"multiple_img"文件夹中
    图片的名字是对应二级文件夹的名字
    '''
    # 创建img文件夹路径
    img_folder = os.path.join(base_folder, '0multiple_img')
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # 用于保存二级文件夹路径和名称的字典
    folder_info = {'paths': [], 'names': []}

    # 遍历一级文件夹下的所有二级文件夹
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path) and folder_name != '0multiple_img':  # 排除img文件夹
            folder_info['paths'].append(folder_path)
            folder_info['names'].append(folder_name)

    # 顺序处理每个二级文件夹
    for folder_path, folder_name in zip(folder_info['paths'], folder_info['names']):
        # 调用plot_multiple_files函数处理文件夹中的Excel文件
        pt.plot_multiple_files_no_display(folder_path,use_log=use_log)

        # 保存图像到multiple_img文件夹
        image_path = os.path.join(img_folder, f'{folder_name}.png')
        plt.savefig(image_path, dpi=225)  # 保存当前图像
        print(f'{folder_name}.png 保存成功!') # 提示保存成功
        plt.close()  # 关闭当前图像，避免内存泄漏


# # 示例调用
# base_folder = './datas_analyze/compare_t'
# plot_multiple_folders(base_folder)

''' ------------------------------------- 4(1). 单文件双法并行去除离群值曲线拟合(不迭代) ---------------------------------'''


# TIPS: 不可迭代多次清除离群值, 不可迭代拟合曲线最高次数
def analyze_data_OutlierRemoval(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                line_color='r', line_width=1.5, remove_outliers=True, threshold=3, use_log=False):
    """
    读取数据，进行多项式拟合并绘制结果，支持去除异常值。

    参数：
    - file_path: Excel 文件的路径。
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '--'（虚线）。
    - line_color: 曲线的颜色，默认为 'r'（红色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - remove_outliers: 是否去除异常值，默认 True。
    - threshold: 异常值判断的阈值（基于残差的标准差倍数），默认 3。
    """
    # 读取 Excel 文件, 提取电压电流数据
    x, y = pt.read_xlsx(file_path)

    # 第一次拟合（用于检测异常值）
    p, y_fit = pt.polynomial_fit(x, y, degree)
    residuals = y - y_fit  # 计算残差
    residual_std = np.std(residuals)  # 残差的标准差

    # 去除异常值 DETAIL: 两种清除离群值(异常值)方法, 并将两种清除后的数据取交集
    if remove_outliers:
        # 方法 1：基于残差的绝对值
        mask_residual = np.abs(residuals) <= threshold * residual_std

        # 方法 2：基于局部离群点检测（Isolation Forest）
        clf = IsolationForest(contamination=0.05)  # 假设 5% 的数据是异常值
        mask_isolation = clf.fit_predict(np.column_stack((x, y))) == 1

        # 结合两种方法
        mask = mask_residual & mask_isolation

        x_cleaned = x[mask]
        y_cleaned = y[mask]
    else:
        x_cleaned = x
        y_cleaned = y

    # 第二次拟合（使用去除异常值后的数据）
    p_cleaned, y_fit_cleaned = pt.polynomial_fit(x_cleaned, y_cleaned, degree)

    # 计算 R²（决定系数）
    r_squared = pt.calculate_r_squared(y,y_fit)

    # 计算 R²（决定系数）- 清除后
    r_squared_cleaned =pt.calculate_r_squared(y_cleaned,y_fit_cleaned)

    # 打印清除异常值前后的 R²
    print(f"清除异常值前的决定系数: R^2 = {r_squared:.12f}")
    print(f"清除异常值后的决定系数: R^2 = {r_squared_cleaned:.12f}")

    # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
    equation_str =pt.format_equation(p, degree)
    equation_str_cleaned =pt.format_equation(p_cleaned, degree)

    # 绘制图像
    pt.plot_removal_1(x, y, x_cleaned, y_cleaned, y_fit, y_fit_cleaned, equation_str, equation_str_cleaned,
                 r_squared, r_squared_cleaned, degree, line_style, line_color, line_width,
                 show_equation, show_r_squared, remove_outliers, use_log)


# # 使用例 : 使用 analyze_data_OutlierRemoval 进行分析
# file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径
# analyze_data_OutlierRemoval(file_path, degree=3, show_equation=True, show_r_squared=True,
#                                     line_style='--', line_color='r', line_width=1, remove_outliers=True, threshold=0.5)
''' ------------------------------------- 4(2). 单文件双法并行去除离群值曲线拟合(不迭代, 弹窗) ------------------------------'''


# TIPS: 不可迭代多次清除离群值, 不可迭代拟合曲线最高次数
def analyze_data_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                line_color='r', line_width=1.5, remove_outliers=True, threshold=3, use_log=False):
    """
    读取数据，进行多项式拟合并绘制结果，支持去除异常值。

    参数：
    - file_path: Excel 文件的路径。
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '--'（虚线）。
    - line_color: 曲线的颜色，默认为 'r'（红色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - remove_outliers: 是否去除异常值，默认 True。
    - threshold: 异常值判断的阈值（基于残差的标准差倍数），默认 3。
    """

    # 弹窗选择文件
    file_path = pt.select_file()
    if not file_path:
        print("未选择文件。")
        return


    # 读取 Excel 文件, 提取电压电流数据
    x, y = pt.read_xlsx(file_path)

    # 第一次拟合（用于检测异常值）
    p, y_fit = pt.polynomial_fit(x, y, degree)
    residuals = y - y_fit  # 计算残差
    residual_std = np.std(residuals)  # 残差的标准差

    # 去除异常值 DETAIL: 两种清除离群值(异常值)方法, 并将两种清除后的数据取交集
    if remove_outliers:
        # 方法 1：基于残差的绝对值
        mask_residual = np.abs(residuals) <= threshold * residual_std

        # 方法 2：基于局部离群点检测（Isolation Forest）
        clf = IsolationForest(contamination=0.05)  # 假设 5% 的数据是异常值
        mask_isolation = clf.fit_predict(np.column_stack((x, y))) == 1

        # 结合两种方法
        mask = mask_residual & mask_isolation

        x_cleaned = x[mask]
        y_cleaned = y[mask]
    else:
        x_cleaned = x
        y_cleaned = y

    # 第二次拟合（使用去除异常值后的数据）
    p_cleaned, y_fit_cleaned = pt.polynomial_fit(x_cleaned, y_cleaned, degree)

    # 计算 R²（决定系数）
    r_squared = pt.calculate_r_squared(y,y_fit)

    # 计算 R²（决定系数）- 清除后
    r_squared_cleaned =pt.calculate_r_squared(y_cleaned,y_fit_cleaned)

    # 打印清除异常值前后的 R²
    print(f"清除异常值前的决定系数: R^2 = {r_squared:.12f}")
    print(f"清除异常值后的决定系数: R^2 = {r_squared_cleaned:.12f}")

    # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
    equation_str =pt.format_equation(p, degree)
    equation_str_cleaned =pt.format_equation(p_cleaned, degree)

    # 绘制图像
    pt.plot_removal_1(x, y, x_cleaned, y_cleaned, y_fit, y_fit_cleaned, equation_str, equation_str_cleaned,
                 r_squared, r_squared_cleaned, degree, line_style, line_color, line_width,
                 show_equation, show_r_squared, remove_outliers, use_log)


# # 使用例 : 使用 analyze_data_OutlierRemoval_windowed 进行分析
# analyze_data_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True,
#                                     line_style='--', line_color='r', line_width=1, remove_outliers=True, threshold=2)

''' ------------------------------------- 5(1). 单文件双法并行去除离群值曲线拟合(可迭代) -----------------------------------'''


# TIPS: 迭代多次清除离群值, 不可迭代拟合曲线最高次数
def iterate_fitting_OutlierRemoval(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                  line_color='r', line_width=1.5, remove_outliers=True, target_r_squared=0.9,
                                  min_threshold=0.3, initial_threshold=3, use_log=False):
    """
    读取数据，进行多项式拟合并绘制结果，支持迭代去除异常值。

    参数：
    - file_path: Excel 文件的路径。
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '-'（实线）。
    - line_color: 曲线的颜色，默认为 'b'（蓝色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - remove_outliers: 是否去除异常值，默认 True。
    - target_r_squared: 目标决定系数 R²，默认 0.9。
    - min_threshold: threshold 的最小值，默认 0.3。
    - initial_threshold: threshold 的初始值，默认 3。
    """
    # 读取 Excel 文件, 提取电压电流数据
    x, y = pt.read_xlsx(file_path)

    # 初始化变量
    threshold = initial_threshold
    x_cleaned, y_cleaned = x, y
    r_squared_cleaned = 0

    # 迭代清除异常值 IMPT: 迭代清除数据, 直至达到效果
    if remove_outliers:
        while threshold >= min_threshold:
            x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned = pt.fit_and_remove_outliers(x_cleaned,
                                                                                                        y_cleaned,
                                                                                                        degree,
                                                                                                        threshold)
            print(f"当前 threshold: {threshold:.2f}, R²: {r_squared_cleaned:.4f}")

            # 如果达到目标 R²，停止迭代
            if r_squared_cleaned >= target_r_squared:
                print(f"达到目标 R²: {target_r_squared}")
                break

            # 降低 threshold
            threshold -= 0.1
        else:
            print(
                f"未达到目标 R²，当前 R²: {r_squared_cleaned:.4f}，threshold 已降至最小值 {min_threshold}，该方法不可行。")

    # 如果没有清除异常值，直接拟合
    else:
        p_cleaned, y_fit_cleaned = pt.polynomial_fit(x_cleaned, y_cleaned, degree)

        # 计算 R²（决定系数）- 清除后
        r_squared_cleaned = pt.calculate_r_squared(y_cleaned, y_fit_cleaned)


    # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
    equation_str_cleaned =pt.format_equation(p_cleaned, degree)

    # 调用画图函数
    pt.plot_removal_2(x, y, x_cleaned, y_cleaned, y_fit_cleaned, equation_str_cleaned, r_squared_cleaned, degree,
                   show_equation, show_r_squared, line_style, line_color, line_width, use_log)


# # 使用例: 使用 iterate_fitting_OutlierRemoval 进行分析
# file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径
# iterate_fitting_OutlierRemoval(file_path, degree=3, show_equation=False, show_r_squared=True,
#                               line_style='--', line_color='r', line_width=1, remove_outliers=True,
#                               target_r_squared=0.9, min_threshold=1, initial_threshold=3)


''' ------------------------------------- 5(2). 单文件双法并行去除离群值曲线拟合(可迭代, 弹窗) ------------------------------'''


# TIPS: 迭代多次清除离群值, 不可迭代拟合曲线最高次数
def iterate_fitting_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                  line_color='r', line_width=1.5, remove_outliers=True, target_r_squared=0.9,
                                  min_threshold=0.3, initial_threshold=3, use_log=False):
    """
    读取数据，进行多项式拟合并绘制结果，支持迭代去除异常值。

    参数：
    - file_path: Excel 文件的路径。
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 最终拟合曲线的线型，默认为 '-'（实线）。
    - line_color: 最终拟合曲线的颜色，默认为 'b'（蓝色）。
    - line_width: 最终拟合曲线的线宽，默认为 1.5。
    - remove_outliers: 是否去除异常值，默认 True。
    - target_r_squared: 目标决定系数 R²，默认 0.9。
    - min_threshold: threshold 的最小值，默认 0.3。
    - initial_threshold: threshold 的初始值，默认 3。
    """

    # 弹窗选择文件
    file_path = pt.select_file()
    if not file_path:
        print("未选择文件。")
        return

    # 读取 Excel 文件, 提取电压电流数据
    x, y = pt.read_xlsx(file_path)

    # 初始化变量
    threshold = initial_threshold
    x_cleaned, y_cleaned = x, y
    r_squared_cleaned = 0

    # 迭代清除异常值 IMPT: 迭代清除数据, 直至达到效果
    if remove_outliers:
        while threshold >= min_threshold:
            x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned = pt.fit_and_remove_outliers(x_cleaned,
                                                                                                        y_cleaned,
                                                                                                        degree,
                                                                                                        threshold, use_log)
            print(f"当前 threshold: {threshold:.2f}, R²: {r_squared_cleaned:.4f}")

            # 如果达到目标 R²，停止迭代
            if r_squared_cleaned >= target_r_squared:
                print(f"达到目标 R²: {target_r_squared}")
                break

            # 降低 threshold
            threshold -= 0.1
        else:
            print(
                f"未达到目标 R²，当前 R²: {r_squared_cleaned:.4f}，threshold 已降至最小值 {min_threshold}，该方法不可行。")

    # 如果没有清除异常值，直接拟合
    else:
        p_cleaned, y_fit_cleaned = pt.polynomial_fit(x_cleaned, y_cleaned, degree)

        # 计算 R²（决定系数）- 清除后
        r_squared_cleaned = pt.calculate_r_squared(y_cleaned, y_fit_cleaned)

    # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
    equation_str_cleaned =pt.format_equation(p_cleaned, degree)

    # 调用画图函数
    pt.plot_removal_2(x, y, x_cleaned, y_cleaned, y_fit_cleaned, equation_str_cleaned, r_squared_cleaned, degree,
                   show_equation, show_r_squared, line_style, line_color, line_width, use_log)


# # 使用例: 使用 iterate_fitting_OutlierRemove_windowed 进行分析
# iterate_fitting_OutlierRemoval_windowed(degree=3, show_equation=False, show_r_squared=True,
#                               line_style='--', line_color='r', line_width=1, remove_outliers=True,
#                               target_r_squared=0.9, min_threshold=1, initial_threshold=3)


''' ------------------------------------- *. 非画图分析类函数 ----------------------------------------------------------'''

''' ------------------------------------- 1. 按照变量进行文件分类 -------------------------------------------------------'''

def sort_variable(root_dir, sort_standard=None, sort_all=False, ignore_list=['n', 'g'], move_single=True, draw_plot=False, use_log=False):
    '''
    :param root_dir: 存放数据文件的一级文件夹, 其下的二级文件夹直接存放.xlsx文件
    :param sort_standard: 控制变量法中分析的变量, 't' 即以 t(实验次数) 为标准进行文件分类
    :param sort_all: 当sort_standard = None, sort_all = True 时, 直接对所有变量遍历分类
    :param ignore_list: 分类时忽略的变量, 一般默认忽略序号和组别, 因为它们不影响板子的物理性质
    :param move_single: 是否处理仅含单.xlsx文件的文件夹, 默认处理. 具体参看 Parts.py 中的 move_single_file_folders 函数
    :param draw_plot: 是否调用plot_multiple_files进行画图, 默认False(因为运行时间太长)
    '''
    if not sort_standard and not sort_all:
        print("No sort standard provided. Function will not execute.")
        return

    # 如果 sort_all 为 True，则遍历所有分类标准(此处忽略 n 与 g ,对其分类没有太大意义)
    if sort_all:
        for standard in ['P', 'd', 't', 'e', 'v']:
            sort_variable(root_dir, sort_standard=standard, sort_all=False, ignore_list=ignore_list, move_single=move_single, draw_plot=draw_plot, use_log=use_log)
        return

    # 检查 ignore_list 是否合法
    if ignore_list:
        valid_keys = {'P', 'd', 'n', 't', 'g', 'e', 'v'}
        if not set(ignore_list).issubset(valid_keys):
            print(f"Invalid ignore_list: {ignore_list}. It should only contain 'P', 'd', 'n', 't', 'g', 'e', 'v'.")
            return

    # 定义占位符规则
    placeholder_map = {
        'P': 'P',  # 走线类型
        'd': 'd',  # 导线间距
        'n': 'n',  # 序号
        't': 't',  # 实验次数
        'g': 'g',  # 实验组别
        'e': 'e',  # 辐照注量
        'v': 'v'   # 偏压
    }

    # 创建 compare_dir 目录
    compare_dir = os.path.join(os.path.dirname(root_dir), f"compare_{sort_standard}")
    os.makedirs(compare_dir, exist_ok=True)

    # 用于记录每个 group_key 的文件数量
    group_count = {}

    # 遍历二级文件夹
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(subdir, file)
                file_name = os.path.basename(file_path)
                # 解析文件名
                pattern = re.compile(r'([TB]\d(?:\.\d)?)-(\d+)-(\d+)(\d+)-(\d+)(\d+)(?:\(.*\))?')
                match = pattern.match(file_name)
                if not match:
                    continue

                # 提取文件名各部分
                layer_spacing = match.group(1)  # 走线类型和导线间距
                number = match.group(2)         # 序号
                experiment_num = match.group(3)  # 实验次数
                experiment_group = match.group(4)  # 实验组别
                fluence = match.group(5)        # 辐照注量
                bias = match.group(6)           # 偏压

                # 根据分类标准和 ignore_list 生成 group_key
                if sort_standard:
                    # 走线类型和导线间距
                    if sort_standard == 'P':
                        # 当 sort_standard 为 'P' 时，导线间距部分用占位符 'd' 表示
                        p_part = placeholder_map['P']
                        d_part = layer_spacing[1:] if 'd' not in ignore_list else placeholder_map['d']
                        pd_part = f"{p_part}{d_part}"
                    elif sort_standard == 'd':
                        # 当 sort_standard 为 'd' 时，走线类型部分用占位符 'P' 表示
                        p_part = layer_spacing[0] if 'P' not in ignore_list else placeholder_map['P']
                        d_part = placeholder_map['d']
                        pd_part = f"{p_part}{d_part}"
                    else:
                        p_part = layer_spacing[0] if 'P' not in ignore_list else placeholder_map['P']
                        d_part = layer_spacing[1:] if 'd' not in ignore_list else placeholder_map['d']
                        pd_part = f"{p_part}{d_part}"

                    # 序号
                    if sort_standard == 'n':
                        n_part = placeholder_map['n']
                    else:
                        n_part = number if 'n' not in ignore_list else placeholder_map['n']

                    # 实验次数和实验组别
                    if sort_standard == 't':
                        # 当 sort_standard 为 't' 时，实验组别部分用占位符 'g' 表示
                        t_part = placeholder_map['t']
                        g_part = experiment_group if 'g' not in ignore_list else placeholder_map['g']
                        tg_part = f"{t_part}{g_part}"
                    elif sort_standard == 'g':
                        tg_part = placeholder_map['g']
                    else:
                        t_part = experiment_num if 't' not in ignore_list else placeholder_map['t']
                        g_part = experiment_group if 'g' not in ignore_list else placeholder_map['g']
                        tg_part = f"{t_part}{g_part}"

                    # 辐照注量和偏压
                    if sort_standard == 'e':
                        # 当 sort_standard 为 'e' 时，偏压部分用占位符 'v' 表示
                        e_part = placeholder_map['e']
                        v_part = bias if 'v' not in ignore_list else placeholder_map['v']
                        ev_part = f"{e_part}{v_part}"
                    elif sort_standard == 'v':
                        # 当 sort_standard 为 'v' 时，辐照注量部分用占位符 'e' 表示
                        e_part = fluence if 'e' not in ignore_list else placeholder_map['e']
                        v_part = placeholder_map['v']
                        ev_part = f"{e_part}{v_part}"
                    else:
                        e_part = fluence if 'e' not in ignore_list else placeholder_map['e']
                        v_part = bias if 'v' not in ignore_list else placeholder_map['v']
                        ev_part = f"{e_part}{v_part}"

                    # 组合成 group_key
                    group_key = f"{pd_part}-{n_part}-{tg_part}-{ev_part}"
                else:
                    # 如果 sort_standard 为 None，且 sort_all 为 True，则直接返回(因为前面已经处理了这种情况)
                    return

                # 更新文件数量
                if group_key not in group_count:
                    group_count[group_key] = 0
                group_count[group_key] += 1

                # 创建分类文件夹并复制文件
                group_dir = os.path.join(compare_dir, group_key)
                os.makedirs(group_dir, exist_ok=True)
                shutil.copy(file_path, os.path.join(group_dir, file_name))

    # 遍历 compare_dir，重命名文件夹并添加 (count)
    for group_key, count in group_count.items():
        old_dir = os.path.join(compare_dir, group_key)
        new_dir = os.path.join(compare_dir, f"{group_key}({count})")
        # 如果目标文件夹已存在，则先删除它
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        os.rename(old_dir, new_dir)

    # 在 compare_dir 名称后加上二级文件夹的数量
    num_subdirs_before = len([name for name in os.listdir(compare_dir) if os.path.isdir(os.path.join(compare_dir, name))])
    new_compare_dir = os.path.join(os.path.dirname(root_dir), f"compare_{sort_standard}({num_subdirs_before})")

    # 如果目标文件夹已存在，则先删除它
    if os.path.exists(new_compare_dir):
        shutil.rmtree(new_compare_dir)
    os.rename(compare_dir, new_compare_dir)

    # 处理只含单个.xlsx文件的文件夹
    if move_single:
        pt.move_single_file_folders(new_compare_dir)

    # 更新 compare_dir 名称，添加处理后的文件夹数量
    num_subdirs_after = len([name for name in os.listdir(new_compare_dir) if os.path.isdir(os.path.join(new_compare_dir, name))])
    final_compare_dir = os.path.join(os.path.dirname(root_dir), f"compare_{sort_standard}({num_subdirs_before}_{num_subdirs_after})")
    os.rename(new_compare_dir, final_compare_dir)

    # 清理空文件夹
    for subdir, _, _ in os.walk(final_compare_dir):
        if not os.listdir(subdir):
            os.rmdir(subdir)

    # 如果 draw_plot 为 True，则调用 plot_multiple_folders 函数
    if draw_plot:
        pjc.plot_multiple_folders(final_compare_dir, use_log)


# # 示例调用
# root_dir = './datas_learn/sort_test/test_2/all_data'
# # root_dir = './datas_learn/sort_test/test_all/temp'
# sort_standard = 't'
# ignore_list = ['n', 'g']
#
# # 直接全部运行就是全都分类一次
# sort_variable(root_dir, sort_standard='P', sort_all=False, ignore_list=ignore_list, move_single=True)
# sort_variable(root_dir, sort_standard='d', sort_all=False, ignore_list=ignore_list, move_single=True)
# sort_variable(root_dir, sort_standard='t', sort_all=False, ignore_list=ignore_list, move_single=True)
# sort_variable(root_dir, sort_standard='e', sort_all=False, ignore_list=ignore_list, move_single=True)
# sort_variable(root_dir, sort_standard='v', sort_all=False, ignore_list=ignore_list, move_single=True)

# sort_variable(root_dir, sort_standard=None, sort_all=True, ignore_list=['n', 'g'], move_single=True)
