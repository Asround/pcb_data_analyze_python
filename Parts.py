"""
说明:
对于读取类函数:
    1. 将 dataframe 参数传入本程序, 将获得提取出的电压和电流的数据列表
    2. 对各种 .xlsx表格均做了适配, 无需担心无法读取. (注意: 不支持 .csv表格, 若需读取请先转换为 .xlsx)
    3. 推荐在各类大型项目中, 导入本函数, 并用 'x, y =read_VA(df)'来调用. 电压/电流数据存储于 x/y中

其他函数:
    有各类可复用函数, 如画图, 拟合等等, 用于其他项目中函数引用.
"""

import os
import re
import shutil

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg') # 解决PyCharm的Matplotlib后端与当前Matplotlib版本不兼容问题
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog # 弹窗选择需要
from sklearn.ensemble import IsolationForest # 去除离群值函数需要

import Parts as pt

# 设置中文字体，解决字体显示问题
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 例如使用微软雅黑（SimHei）
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

''' ------------------------------------- 1. 提取电压电流数据并返回两个列表 ---------------------------------------------'''
'''
特化的, 转为读取项目.xlsx文件的读取函数, 返回电压电流数据
'''

def read_xlsx(file_path, clear=True):
    """
    读取 Excel 文件并提取电压电流数据。
    是read_VA的后续版本(功能有些许差异)

    :param file_path: Excel 文件的路径。
    :param clear: 用于去除过大过小值的参数

    :return: x: 电压数据,
     y: 电流数据。
    """
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name=0)

    B2 = df.iloc[0, 1]  # '.iloc[0,1]': 取表格索引为[0,1]单元格(即B2)的内容
    if 'V' in B2:  # 满足该条件, 即 "1.型表格"
        B2 = False
    else:  # 即"2/3.型表格"
        B2 = int(df.iloc[0, 1])  # 将 B2 强制转换为int类型, 作用和 B2 = True 相同

    # if 判断实现不同文件分类读取
    if B2:
        # "2/3.型表格"是非零数字(真), 满足 if 条件 则读取 C36 到 D536 的数据
        df_filtered = df.iloc[34:34 + B2 - 1, [2, 3]].dropna()
        # [34: 34 + B2 - 1,[2,3]]对应 C36 到 D536
        # 34 对应 36 是因为自动丢弃第一行, 并且从 0 开始索引
        # 2 对应 C 是因为 0 是开始索引, 对应 A
        # [34 + B2 - 1, 3] 即 D(B2+33)单元格, 数学上易知是最后一个电流对应单元格
        # # 这样规定的原因是, "2.型表格" 的电压电流数据后有统计量, 不希望它们被读入

    else:
        # "1.型表格" 对应False(假), 则读取 B3 到 C503 的数据
        df_filtered = df.iloc[1:501, [1, 2]].dropna()
        # [2,501]对应 C503, 相当于我们默认读取 501 组数据
        # 因为"1.型表格" 的电压电流数据后面是空值, 会被 .dropna(丢弃), 不怕多读.

    # 重新命名列名 (左边是电压, 右边是电流)
    df_filtered.columns = ["电压 (V)", "电流 (A)"]

    # 转换数据为数值类型（防止字符串干扰）,方便绘图和后续曲线拟合
    df_filtered = df_filtered.astype(float)

    # 提取自变量（电压）和因变量（电流）
    x = df_filtered["电压 (V)"]
    y = df_filtered["电流 (A)"]

    if clear:
        # 功能 1: 去除大于 10000 的值（对 x 和 y 均适用）
        mask = (x <= 10000) & (y <= 10000)
        x = x[mask]
        y = y[mask]

        # 功能 2: 去除 x 小于 10 的值（同时删除对应的 y 值）
        mask = x >= 10
        x = x[mask]
        y = y[mask]

    return x, y


''' ------------------------------------- 1.(1). 提取电压电流数据并返回两个列表 -----------------------------------------'''
'''
在1. 的基础上, 添加了移除异常过大值的功能.
其余功能与 read_xlsx 没有区别
主要考虑到某些表格前排的数据出现了 1e37数量级的数字, 显然不正常. 这十分影响画图.
所以用 0 代替了 大于 10000 的值(电压不明显大于1000, 电流不大于0.01, 故10000 不会导致正常数据被置零).
且异常大值目前只在开头见到, 所以 0 替换是合理的.
'''
def read_xlsx_clear(file_path, check_large_values=False):
    """
    读取 Excel 文件并提取电压电流数据。
    是read_VA的后续版本(功能有些许差异)

    :param file_path: Excel 文件的路径。
    :param check_large_values: 布尔类型参数，如果为True，检查并替换大于10000的值为0。

    :return: x: 电压数据,
    y: 电流数据。
    """
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name=0)

    B2 = df.iloc[0, 1]  # '.iloc[0,1]': 取表格索引为[0,1]单元格(即B2)的内容
    if 'V' in B2:  # 满足该条件, 即 "1.型表格"
        B2 = False
    else:  # 即"2/3.型表格"
        B2 = int(df.iloc[0, 1])  # 将 B2 强制转换为int类型, 作用和 B2 = True 相同

    # if 判断实现不同文件分类读取
    if B2:
        # "2/3.型表格"是非零数字(真), 满足 if 条件 则读取 C36 到 D536 的数据
        df_filtered = df.iloc[34:34 + B2 - 1, [2, 3]].dropna()
        # [34: 34 + B2 - 1,[2,3]]对应 C36 到 D536
        # 34 对应 36 是因为自动丢弃第一行, 并且从 0 开始索引
        # 2 对应 C 是因为 0 是开始索引, 对应 A
        # [34 + B2 - 1, 3] 即 D(B2+33)单元格, 数学上易知是最后一个电流对应单元格
        # # 这样规定的原因是, "2.型表格" 的电压电流数据后有统计量, 不希望它们被读入

    else:
        # "1.型表格" 对应False(假), 则读取 B3 到 C503 的数据
        df_filtered = df.iloc[1:501, [1, 2]].dropna()
        # [2,501]对应 C503, 相当于我们默认读取 501 组数据
        # 因为"1.型表格" 的电压电流数据后面是空值, 会被 .dropna(丢弃), 不怕多读.

    # 重新命名列名 (左边是电压, 右边是电流)
    df_filtered.columns = ["电压 (V)", "电流 (A)"]

    # 转换数据为数值类型（防止字符串干扰）,方便绘图和后续曲线拟合
    df_filtered = df_filtered.astype(float)

    # 提取自变量（电压）和因变量（电流）
    x = df_filtered["电压 (V)"]
    y = df_filtered["电流 (A)"]

    # 检查并替换大于10000的值
    if check_large_values:
        x = x.where(x <= 10000, 0)
        y = y.where(y <= 10000, 0)

    return x, y

''' ------------------------------------ 2(1). 弹窗选取文件的函数 -------------------------------------------------------'''
'''
引起选择文件的窗口函数
并默认让窗口在最前端
'''
def select_file():
    """
    弹窗选择文件路径，并确保弹窗始终保持在最前端。

    :return: file_path: 选择的文件路径，如果未选择则返回 None。
    """
    root = Tk()
    root.withdraw()  # 隐藏 Tkinter 根窗口
    root.attributes("-topmost", True)  # 确保弹窗始终在最前端
    file_path = filedialog.askopenfilename(title="选择 Excel 文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    root.destroy()  # 关闭 Tkinter 窗口

    return file_path

''' ------------------------------------- 2(2). 弹窗选取文件夹的函数 ----------------------------------------------------'''
'''
引起选择文件夹的窗口函数
并默认让窗口在最前端
'''
def select_folder():
    """
    弹窗选择文件夹路径，并确保弹窗始终保持在最前端。

    :return: folder_path: 选择的文件夹路径，如果未选择则返回 None。
    """
    root = Tk()
    root.withdraw()  # 隐藏 Tkinter 根窗口
    root.attributes("-topmost", True)  # 确保弹窗始终在最前端
    folder_path = filedialog.askdirectory(title="选择一个包含 .xlsx 文件的文件夹")
    root.destroy()  # 关闭 Tkinter 窗口

    return folder_path

''' ------------------------------------- 3. 多项式拟合函数 ------------------------------------------------------------'''

def polynomial_fit(x, y, degree):
    """
    对数据进行多项式拟合。

    :param x: 电压数据。
    :param y: 电流数据。
    :param degree: 多项式拟合的次数。

    :return: p: 拟合多项式的系数,
    y_fit: 拟合后的电流值。
    """
    p = np.polyfit(x, y, degree)
    y_fit = np.poly1d(p)(x)
    return p, y_fit
''' ------------------------------------- 4. 生成拟合函数的字符串表达式（LaTeX 格式） --------------------------------------'''
'''
将表达式Latex格式化
'''
def format_equation(p, degree):
    """
    生成拟合函数的字符串表达式（LaTeX 格式）。

    :param p: 拟合多项式的系数。
    :param degree: 多项式拟合的次数。

    :return: equation_str: 拟合函数的字符串表达式。
    """
    equation_terms = []
    for i, coef in enumerate(p):
        power = degree - i
        coef_str = f"{coef:.2e}".replace("e", "\\cdot10^{") + "}"
        if coef < 0:
            coef_str = f"({coef_str})"
        if power == 0:
            term = coef_str
        else:
            term = f"{coef_str}x^{{{power}}}"
        equation_terms.append(term)
    return " + ".join(equation_terms)

''' ------------------------------------- 5. 计算决定系数 R-squared ----------------------------------------------------'''
'''
依据实际数据和拟合后的数据, 进行决定系数计算
'''
def calculate_r_squared(y, y_fit):
    """
    计算决定系数 R²。

    :param y: 原始电流数据。
    :param y_fit: 拟合后的电流值。

    :return: r_squared: 决定系数 R²。
    """
    ss_residual = np.sum((y - y_fit) ** 2)
    ss_total = np.sum((y - np.mean(y)) ** 2)
    return 1 - (ss_residual / ss_total)

''' ------------------------------------- 6. 去除离群值, 并重新拟合 -----------------------------------------------------'''
'''
依照已有数据(x, y)进行曲线拟合(多项式), 并联合两种方式去除离群值
'''
def fit_and_remove_outliers(x, y, degree, threshold):
    """
    :param x: 原始电压数据
    :param y: 原始电流数据
    :param degree: 多项式阶数
    :param threshold: 接受阈值

    :return: x_cleaned: 去除离群值后的电压数据,
    y_cleaned: 去除离群值后的电流数据, p_cleaned: 去除群值后拟合的多项式系数,
    y_fit_cleaned: 基于去除离群值后的数据拟合的电流,
    r_squared_cleaned: 基于去除离群值后的拟合决定系数
    """
    # 第一次拟合（用于检测异常值）
    p, y_fit = np.polyfit(x, y, degree), np.poly1d(np.polyfit(x, y, degree))(x)
    residuals = y - y_fit  # 计算残差
    residual_std = np.std(residuals)  # 残差的标准差

    # 方法 1：基于残差的绝对值
    mask_residual = np.abs(residuals) <= threshold * residual_std

    # 方法 2：基于局部离群点检测（Isolation Forest）
    clf = IsolationForest(contamination=0.05)  # 假设 5% 的数据是异常值
    mask_isolation = clf.fit_predict(np.column_stack((x, y))) == 1

    # 结合两种方法
    mask = mask_residual & mask_isolation

    x_cleaned = x[mask]
    y_cleaned = y[mask]

    # 第二次拟合（使用去除异常值后的数据）
    p_cleaned, y_fit_cleaned = np.polyfit(x_cleaned, y_cleaned, degree), np.poly1d(
        np.polyfit(x_cleaned, y_cleaned, degree))(x_cleaned)

    # 计算 R²（决定系数）- 清除后
    r_squared_cleaned = pt.calculate_r_squared(y_cleaned, y_fit_cleaned)

    return x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned

''' ------------------------------------- 7. 读取文件名称, 解释含义 -----------------------------------------------------'''
'''
传入表格名称(str), 或者 .xlsx(表格文件路径), 均可返回解释文本
'''


def read_name(input_data, show_name=True, show_number=True, show_group=True, show_tip=True):
    '''
    :param input_data: 传入str 或者 .xlsx文件路径
    :param show_name: 是否输出原表格名称
    :param show_number: 是否输出板序号
    :param show_group: 是否输出实验组别
    :param show_tip: 当有备注内容时, 是否输出'有备注'

    :return: 包含解释内容的字符串
    '''
    # 判断输入是文件路径还是字符串
    if isinstance(input_data, str) and input_data.endswith('.xlsx'):
        file_name = os.path.basename(input_data)
    else:
        file_name = input_data

    # 提取文件名中的关键信息
    pattern = re.compile(r'([TB]\d(?:\.\d)?)-(\d+)-(\d+)(\d+)-(\d+)(\d+)(?:\(.*\))?')
    match = pattern.match(file_name)
    if not match:
        return "Invalid file name format"

    # 解析各部分信息
    layer, spacing = match.group(1)[0], match.group(1)[1:]
    number = match.group(2)
    experiment_num = match.group(3)
    experiment_group = match.group(4)
    fluence = match.group(5)
    bias = match.group(6)

    # 处理实验次数的字母表示
    if experiment_num.isalpha():
        experiment_num = str(ord(experiment_num.upper()) - 55)

    # 处理辐照注量和偏压
    fluence_map = {'0': '0', '1': '1e15', '2': '5e15', '3': '1e16', '4': '1e14'}
    bias_map = {'0': '0', '1': '50', '2': '120', '3': '240'}
    fluence_value = fluence_map.get(fluence, 'Unknown')
    bias_value = bias_map.get(bias, 'Unknown')

    # 构建返回字符串
    result = []
    if show_name:
        result.append(f"{file_name}: ")
    result.append(f"{'顶层' if layer == 'T' else '顶底两层'}走线, 导线间距{spacing}mm")
    if show_number:
        result.append(f", 序号{number}")
    result.append(f", 第{experiment_num}次实验")
    if show_group:
        result.append(f", 实验组别{experiment_group}")
    result.append(f", {fluence_value}辐照注量, {bias_value}V偏压")
    if show_tip and '(' or '（' in file_name:
        result.append(", 有备注")

    return ''.join(result)

# # 调用示例
# # 读取文件名信息
# print(read_name('T0.5-1-11-10(boom)'))
# print(read_name('T0.5-1-11-10（boom）'))
# print(read_name('T0.5-1-11-10(boom)', show_name=False, show_number=False, show_group=False, show_tip=False))
# print(read_name('B2-2-72-21.xlsx'))
# print(read_name('B2-2-72-21.xlsx', show_name=False, show_number=False, show_group=False, show_tip=False))

''' ------------------------------------ 9. 处理仅含单个.xlsx文件的文件夹 ------------------------------------------------'''
'''
用于sort_variable函数中引用, 参数 compare_dir 与 sort_variable 函数中的 compare_dir 一致.
由于按照某些变量进行分类, 分出来会有仅含单个.xlsx文件的情况, 即无对照组与之形成对照
所以此函数的作用, 就是将这些单个的.xlsx文件移动到一个统一的only_one文件夹中, 并删除原来存放这些单个文件的文件夹, 以防止(无意义)图片过多
'''
def move_single_file_folders(compare_dir):
    # 创建 only_one 文件夹
    only_one_dir = os.path.join(compare_dir, "1only_one")
    # 1前缀是为了放在前面, 方便找到.(图像文件夹前缀为0, 在1only_one文件夹前面)
    os.makedirs(only_one_dir, exist_ok=True)

    # 用于记录移动的文件数量
    file_count = 0

    # 遍历 compare_dir 下的所有二级文件夹
    for folder_name in os.listdir(compare_dir):
        folder_path = os.path.join(compare_dir, folder_name)
        if os.path.isdir(folder_path) and "(1)" in folder_name:
            # 找到文件夹中的 .xlsx 文件
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.xlsx'):
                    file_path = os.path.join(folder_path, file_name)
                    # 将文件移动到 only_one 文件夹
                    shutil.move(file_path, os.path.join(only_one_dir, file_name))
                    file_count += 1
            # 删除原文件夹
            os.rmdir(folder_path)

    # 重命名 only_one 文件夹，加上计数后缀
    if file_count > 0:
        new_only_one_dir = os.path.join(compare_dir, f"1only_one({file_count})")
        os.rename(only_one_dir, new_only_one_dir)
    else:
        # 如果没有文件被移动，则删除空的 only_one 文件夹
        os.rmdir(only_one_dir)


''' ------------------------------------------- *. 绘图类函数 ---------------------------------------------------------'''

'''
(1). 单文件简单分析画图
包含了原数据绘图 + 一次拟合曲线绘图 功能
用于: analyze_data 相关函数
'''
def plot_single(x, y, y_fit, p, degree, show_equation, show_r_squared, line_style, line_color, line_width, connect_points, use_log=False):
    """
    绘制数据和拟合曲线。

    参数：
    :param x: 电压数据。
    :param y: 原始电流数据。
    :param y_fit: 拟合后的电流值。
    :param p: 拟合多项式的系数。
    :param degree: 多项式拟合的次数。
    :param show_equation: 是否显示拟合函数表达式。
    :param show_r_squared: 是否显示决定系数 R²。
    :param line_style: 拟合曲线的线型。
    :param line_color: 拟合曲线的颜色。
    :param line_width: 拟合曲线的线宽。
    :param connect_points: 是否连接原始数据点。
    :param use_log: 是否对横轴进行对数化处理。
    """
    plt.figure(figsize=(8, 6))

    # 对数化处理
    if use_log:
        x = np.log10(x)
        x_label = "电压-log10 (V)"
    else:
        x_label = "电压 (V)"

    # 绘制原始数据点
    if connect_points:
        plt.plot(x, y, marker='o', linestyle='-', color='b', label="原始数据", markersize=3,
                 markerfacecolor='white', markeredgewidth=1, linewidth=2)
    else:
        plt.plot(x, y, marker='o', linestyle='', color='b', label="原始数据", markersize=3,
                 markerfacecolor='white', markeredgewidth=1)

    # 绘制拟合曲线
    plt.plot(x, y_fit, linestyle=line_style, color=line_color, label=f"{degree}次多项式拟合", linewidth=line_width)

    # 添加拟合函数表达式
    if show_equation:
        equation_str = pt.format_equation(p, degree)
        plt.text(0.0, 0.06, f"拟合函数: $y = {equation_str}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8))

    # 添加 R² 值
    if show_r_squared:
        r_squared = pt.calculate_r_squared(y, y_fit)
        plt.text(0.8, 0.5, f"$R^2 = {r_squared:.4f}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left')

    # 图表设置
    plt.xlabel(x_label)
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线及拟合")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()
'''
(2). 单文件 单次去除离群值 画图
包含了原数据绘图 + 两次拟合曲线绘图 功能
用于: analyze_data_OuterRemoval 相关函数
'''
def plot_removal_1(x, y, x_cleaned, y_cleaned, y_fit, y_fit_cleaned, equation_str, equation_str_cleaned,
                 r_squared, r_squared_cleaned, degree, line_style, line_color, line_width,
                 show_equation=True, show_r_squared=True, remove_outliers=True, use_log=False):
    """
    绘制电压-电流曲线及拟合（清除异常值）

    Parameters:
    :param x: 原始 x 数据（电压）
    :param y: 原始 y 数据（电流）
    :param x_cleaned: 清除异常值后的 x 数据
    :param y_cleaned: 清除异常值后的 y 数据
    :param y_fit: 清除前的拟合曲线 y 数据
    :param y_fit_cleaned: 清除后的拟合曲线 y 数据
    :param equation_str: 清除前拟合的函数表达式
    :param equation_str_cleaned: 清除后拟合的函数表达式
    :param r_squared: 清除前拟合的 R² 值
    :param r_squared_cleaned: 清除后拟合的 R² 值
    :param degree: 多项式拟合的次数
    :param line_style: 拟合曲线的样式
    :param line_color: 拟合曲线的颜色
    :param line_width: 拟合曲线的宽度
    :param show_equation: 是否显示拟合函数表达式 (默认 True)
    :param show_r_squared: 是否显示 R² 值 (默认 True)
    :param remove_outliers: 是否显示清除异常值后的数据点 (默认 True)
    :param use_log: 是否对横轴进行对数化处理。
    """

    # 对数化处理
    if use_log:
        x = np.log10(x)
        x_cleaned = np.log10(x_cleaned)
        x_label = "电压-log10 (V)"
    else:
        x_label = "电压 (V)"

    # 创建图像
    plt.figure(figsize=(10, 6))

    # 绘制原始数据点
    plt.plot(x, y, marker='o', linestyle='', color='b', label="原始数据", markersize=3,
             markerfacecolor='white', markeredgewidth=1)

    # 绘制清除异常值后的数据点
    if remove_outliers:
        plt.plot(x_cleaned, y_cleaned, marker='o', linestyle='', color='g', label="清除异常值后的数据", markersize=3,
                 markerfacecolor='green', markeredgewidth=1)

    # 绘制清除前的拟合曲线
    plt.plot(x, y_fit, linestyle=line_style, color=line_color, label=f"清除前 {degree}次多项式拟合", linewidth=line_width)

    # 绘制清除后的拟合曲线
    plt.plot(x_cleaned, y_fit_cleaned, linestyle='-', color='m', label=f"清除后 {degree}次多项式拟合",
             linewidth=line_width)

    # 添加拟合函数表达式
    if show_equation:
        plt.text(0.05, 0.95, f"清除前拟合函数: $y = {equation_str}$", transform=plt.gca().transAxes, fontsize=10,
                 verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8))
        plt.text(0.05, 0.85, f"清除后拟合函数: $y = {equation_str_cleaned}$", transform=plt.gca().transAxes,
                 fontsize=10,
                 verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8))

    # 添加 R² 值
    if show_r_squared:
        plt.text(0.8, 0.5, f"清除前 $R^2 = {r_squared:.4f}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left')
        plt.text(0.8, 0.4, f"清除后 $R^2 = {r_squared_cleaned:.4f}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left')

    # 图表设置
    plt.xlabel(x_label)
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线及拟合（清除异常值）")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()

'''
(3). 单文件 多次去除离群值 画图
包含了原数据绘图 + 最后一次拟合曲线绘图 功能 ( 和(2)有较高相似性 )
用于: iterate_fitting_OuterRemoval 相关函数
'''
def plot_removal_2(x, y, x_cleaned, y_cleaned, y_fit_cleaned, equation_str_cleaned, r_squared_cleaned, degree,
                   show_equation=True, show_r_squared=True, line_style='--', line_color='r', line_width=1.5, use_log=False):
    """
    绘制数据和拟合曲线。

    参数：
    :param x: 原始数据的 x 值。
    :param y: 原始数据的 y 值。
    :param x_cleaned: 清除异常值后的 x 值。
    :param y_cleaned: 清除异常值后的 y 值。
    :param y_fit_cleaned: 清除异常值后的拟合 y 值。
    :param- equation_str_cleaned: 清除异常值后的拟合函数表达式。
    :param- r_squared_cleaned: 清除异常值后的决定系数 R²。
    :param- degree: 多项式拟合的次数。
    :param- show_equation: 是否在图中显示拟合函数表达式，默认显示。
    :param- show_r_squared: 是否显示决定系数 R²，默认显示。
    :param- line_style: 曲线的线型，默认为 '-'（实线）。
    :param- line_color: 曲线的颜色，默认为 'b'（蓝色）。
    :param- line_width: 曲线的线宽，默认为 1.5。
    :param- use_log: 是否对横轴进行对数化处理。
    """
    # 对数化处理
    if use_log:
        x = np.log10(x)
        x_cleaned = np.log10(x_cleaned)
        x_label = "电压-log10 (V)"
    else:
        x_label = "电压 (V)"

    # 绘制数据和拟合曲线
    plt.figure(figsize=(10, 6))

    # 绘制原始数据点
    plt.plot(x, y, marker='o', linestyle='', color='b', label="原始数据", markersize=3,
             markerfacecolor='white', markeredgewidth=1)

    # 绘制清除异常值后的数据点
    plt.plot(x_cleaned, y_cleaned, marker='o', linestyle='', color='g', label="清除异常值后的数据", markersize=3,
             markerfacecolor='green', markeredgewidth=1)

    # 绘制清除后的拟合曲线
    plt.plot(x_cleaned, y_fit_cleaned, linestyle=line_style, color=line_color, label=f"清除后 {degree}次多项式拟合",
             linewidth=line_width)

    # 添加拟合函数表达式
    if show_equation:
        plt.text(0.05, 0.95, f"清除后拟合函数: $y = {equation_str_cleaned}$", transform=plt.gca().transAxes,
                 fontsize=10,
                 verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8))

    # 添加 R² 值
    if show_r_squared:
        plt.text(0.8, 0.5, f"清除后 $R^2 = {r_squared_cleaned:.4f}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left')

    # 图表设置
    plt.xlabel(x_label)
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线及拟合（清除异常值）")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()

''' ------------------------------------------- *. pjc改编函数 --------------------------------------------------------'''

''' ------------------------------------- 1. 分析单个文件并作图拟合, 返回图像但不弹窗展示 -----------------------------------'''
def analyze_data_no_display(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='-', line_color='b',
                           line_width=1.5, connect_points=True, use_log=False):
    """
    与 analyze_data 功能相同，但不显示图像。
    """
    # 读取 Excel 文件, 提取电压电流数据
    x, y = pt.read_xlsx(file_path)

    # 多项式拟合(未使用 polynomial_fit 函数)
    p, y_fit = np.polyfit(x, y, degree), np.poly1d(np.polyfit(x, y, degree))(x)

    # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
    equation_str = pt.format_equation(p, degree)

    # 计算 R²（决定系数）
    r_squared = pt.calculate_r_squared(y,y_fit)


    # 绘制数据和拟合曲线
    plt.figure(figsize=(8, 6))

    # 对数化处理
    if use_log:
        x = np.log10(x)
        x_label = "电压-log10 (V)"
    else:
        x_label = "电压 (V)"

    # 设置原始数据点的样式和连接线的样式
    if connect_points:
        plt.plot(x, y, marker='o', linestyle='-', color='b', label="原始数据", markersize=3,
                 markerfacecolor='white', markeredgewidth=1, linewidth=2)  # 数据点为白色，线条粗细为2
    else:
        plt.plot(x, y, marker='o', linestyle='', color='b', label="原始数据", markersize=3,
                 markerfacecolor='white', markeredgewidth=1)  # 数据点为白色，不连接

    # 绘制拟合曲线
    plt.plot(x, y_fit, linestyle=line_style, color=line_color, label=f"{degree}次多项式拟合", linewidth=line_width)

    # 当 show_equation == True, 在图形中添加拟合函数的表达式（使用 LaTeX 样式）
    if show_equation:
        # plt.text(0.0, 0.06, f"拟合函数: $y = {equation_str}$", transform=plt.gca().transAxes, fontsize=12,
        #          verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8)
        plt.text(0.01, 0.06, f"$y = {equation_str}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8))

    # 当 show_r_squared == True, 在图形中添加 R² 值，使用 LaTeX 样式
    if show_r_squared:
        plt.text(0.8, 0.5, f"$R^2 = {r_squared:.4f}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left')

    # 图表设置
    plt.xlabel(x_label)
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线及拟合")
    plt.legend()
    plt.grid(True)

    # 返回图像对象
    return plt.gcf()
''' ------------------------------------- 2. 分析多个文件并作图拟合, 不弹窗展示 -------------------------------------------'''

# def plot_multiple_files_no_display(folder_path, colors=None, labels=None, line_styles=None, line_widths=None, use_log=False):
#     """
#     绘制文件夹中所有 Excel 文件的数据到同一张图中，方便对比。
#     功能与plot_multiple_files相同, 只是不展示图像(删除最后一句语句)
#
#     参数：
#     - folder_path: 文件夹路径，例如 "./data"。
#     - colors: 每个文件的曲线颜色列表，例如 ['b', 'r', 'g']。
#     - labels: 每个文件的图例标签列表，例如 ["文件1", "文件2", "文件3"]。
#     - line_styles: 每个文件的线型列表，例如 ['-', '--', ':']。
#     - line_widths: 每个文件的线宽列表，例如 [1.5, 1.5, 1.5]。
#     """
#     # 获取文件夹中的所有 Excel 文件
#     file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]
#
#     # 设置默认值
#     if colors is None:
#         colors = [
#                      '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
#                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
#                      '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
#                  ] * (len(file_paths) // 15 + 1)  # 如果文件超过15个，循环使用颜色
#         '''
#             '#1f77b4',  # 蓝色
#             '#ff7f0e',  # 橙色
#             '#2ca02c',  # 绿色
#             '#d62728',  # 红色
#             '#9467bd',  # 紫色
#             '#8c564b',  # 棕色
#             '#e377c2',  # 粉色
#             '#7f7f7f',  # 灰色
#             '#bcbd22',  # 橄榄绿
#             '#17becf',  # 青色
#             '#aec7e8',  # 浅蓝色
#             '#ffbb78',  # 浅橙色
#             '#98df8a',  # 浅绿色
#             '#ff9896',  # 浅红色
#             '#c5b0d5',  # 浅紫色
#         '''
#     if labels is None:
#         labels = [os.path.splitext(os.path.basename(f))[0] for f in file_paths]  # 默认标签为文件名
#     if line_styles is None:
#         line_styles = ['-'] * len(file_paths)  # 默认线型
#     if line_widths is None:
#         line_widths = [1.5] * len(file_paths)  # 默认线宽
#
#     # 创建图表
#     plt.figure(figsize=(10, 6))
#
#     # 对数化处理
#     if use_log:
#         x_label = "电压-log10 (V)"
#     else:
#         x_label = "电压 (V)"
#
#     # 遍历文件路径列表
#     for i, file_path in enumerate(file_paths):
#         # 读取 Excel 文件, 提取电压电流数据
#         x, y = pt.read_xlsx(file_path)
#
#         # 对数化处理
#         if use_log:
#             x = np.log10(x)
#
#         # 绘制数据
#         plt.plot(x, y, linestyle=line_styles[i], color=colors[i], label=labels[i], linewidth=line_widths[i])
#
#     # 图表设置
#     plt.xlabel(x_label)
#     plt.ylabel("电流 (A)")
#     plt.title("电压-电流曲线对比")
#     plt.legend()
#     plt.grid(True)

def plot_multiple_files_no_display(folder_path, colors=None, labels=None, line_styles=None, line_widths=None, use_log=False):
    """
    绘制文件夹中所有 Excel 文件的数据到同一张图中，方便对比。
    功能与plot_multiple_files相同, 只是不展示图像(删除最后一句语句)

    参数：
    :param folder_path: 文件夹路径，例如 "./data"。
    :param colors: 每个文件的曲线颜色列表，例如 ['b', 'r', 'g']。
    :param- labels: 每个文件的图例标签列表，例如 ["文件1", "文件2", "文件3"]。
    :param- line_styles: 每个文件的线型列表，例如 ['-', '--', ':']。
    :param- line_widths: 每个文件的线宽列表，例如 [1.5, 1.5, 1.5]。
    :param- use_log: 是否对 x 轴数据进行对数化处理。
    """
    # 获取文件夹中的所有 Excel 文件
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]

    # 设置默认值
    if colors is None:
        colors = [
                     '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                     '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
                 ] * (len(file_paths) // 15 + 1)  # 如果文件超过15个，循环使用颜色

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
        x_label= "电压 (V)"

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