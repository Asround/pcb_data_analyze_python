"""
存放各类函数的早期版本
基本没用
"""
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest

from Parts import read_VA
from Parts import analyze_data_no_display

# 设置中文字体，解决字体显示问题
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 例如使用微软雅黑（SimHei）
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

''' ------------------------------------- 1. 提取电压电流数据并返回两个列表 -----------------------------------------------'''


# 对应使用例 1
def analyze_data_0(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='-', line_color='b',
                   line_width=1.5):
    """
    读取数据，进行多项式拟合并绘制结果，同时可以控制图表的细节和拟合的显示内容。

    参数：
    - file_path: Excel 文件的路径。
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '-'（实线）。
    - line_color: 曲线的颜色，默认为 'b'（蓝色）。
    - line_width: 曲线的线宽，默认为 1.5。
    """

    # 读取 Excel 文件
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name=0)

    # 提取电压电流数据
    x, y = read_VA(df)

    # 多项式拟合函数
    def polynomial_fit(x, y, degree=3):
        p = np.polyfit(x, y, degree)  # 拟合多项式
        poly = np.poly1d(p)
        y_fit = poly(x)
        return p, y_fit

    # 调用多项式拟合
    p, y_fit = polynomial_fit(x, y, degree)

    # 打印拟合的多项式系数
    print(f"拟合多项式的系数（从高次到低次）: {p}")

    # 准备拟合函数的字符串表达式（优化科学计数法显示）
    equation_terms = []
    for i, coef in enumerate(p):
        power = degree - i
        # 将python中 "e数字" 的科学计数法格式更改为latex形式
        coef_str = f"{coef:.2e}".replace("e", "\\cdot10^{") + "}"
        # 处理负号和小数点
        if coef < 0:
            coef_str = f"({coef_str})"
        # 添加 x 的幂次
        if power == 0:
            term = coef_str
        else:
            term = f"{coef_str}x^{{{power}}}"
        equation_terms.append(term)  # 使用 {{}} 包裹幂次 防止出现x^10的情况出现 (LaTex规范:x^{10})

    # 拼接拟合函数表达式
    equation_str = " + ".join(equation_terms)

    # 计算 R²（决定系数）
    ss_residual = np.sum((y - y_fit) ** 2)  # 残差平方和
    ss_total = np.sum((y - np.mean(y)) ** 2)  # 总平方和
    r_squared = 1 - (ss_residual / ss_total)

    # 打印 R² 值
    print(f"决定系数: R^2 = {r_squared:.12f}")  # 12位保证在拟合效果较好时能看出差距

    # 绘制数据和拟合曲线
    plt.figure(figsize=(8, 6))

    # 设置原始数据点的样式和连接线的样式
    plt.plot(x, y, marker='o', linestyle='-', color='b', label="原始数据", markersize=3,
             markerfacecolor='white', markeredgewidth=1, linewidth=2)  # 数据点为白色，线条粗细为2

    # 绘制拟合曲线
    plt.plot(x, y_fit, linestyle=line_style, color=line_color, label=f"{degree}次多项式拟合", linewidth=line_width)
    # 不想传参就改这里即可

    # 当 show_equation == True, 在图形中添加拟合函数的表达式（使用 LaTeX 样式）
    if show_equation:
        plt.text(0.0, 0.06, f"拟合函数: $y = {equation_str}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8))

    # 当 show_r_squared == True, 在图形中添加 R² 值，使用 LaTeX 样式
    if show_r_squared:
        plt.text(0.8, 0.5, f"$R^2 = {r_squared:.4f}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left')

    # 图表设置
    plt.xlabel("电压 (V)")
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线及拟合")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()


# # 使用例 1: 使用 analyze_data 函数进行单文件作图和曲线拟合 TIPS: 在这里无法运行本函数, 放到 test中可测试.
# # file_path = "./datas_learn/25-1-23前所有数据表/数据24-10-29（辐照前）/辐照前_1000/T1-4-12-11.xlsx"  # 替换为你自己的文件路径(一定要是.xlsx文件!)
# file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径
#
# # 分析file_path对应路径的文件, 用3次多项式进行拟合, 拟合多项式表达式和决定系数均展示, 拟合曲线的线型为虚线, 红色, 宽度为1
# analyze_data_0(file_path, degree=3, show_equation=False, show_r_squared=True, line_style='--', line_color='r',
#              line_width=1)


''' ------------------------------------- 2. 含一种离群值移除的曲线拟合函数 ---------------------------------------------'''


# 对应使用例 3
def analyze_data_OutlierRemoval_1(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='-',
                                  line_color='b', line_width=1.5, remove_outliers=True, threshold=3):
    """
    读取数据，进行多项式拟合并绘制结果，支持去除异常值。

    参数：
    - file_path: Excel 文件的路径。
    - degree: 多项式拟合的次数，默认3。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数R²，默认显示。
    - line_style: 曲线的线型，默认为 '-'（实线）。
    - line_color: 曲线的颜色，默认为 'b'（蓝色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - remove_outliers: 是否去除异常值，默认 True。
    - threshold: 异常值判断的阈值（基于残差的标准差倍数），默认 3。
    """
    # 读取 Excel 文件
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name=0)

    # 提取电压电流数据
    x, y = read_VA(df)

    # 第一次拟合（用于检测异常值）
    p, y_fit = np.polyfit(x, y, degree), np.poly1d(np.polyfit(x, y, degree))(x)
    residuals = y - y_fit  # 计算残差
    residual_std = np.std(residuals)  # 残差的标准差

    # 去除异常值
    if remove_outliers:
        # 判断异常值：残差的绝对值大于 threshold * 残差的标准差
        mask = np.abs(residuals) <= threshold * residual_std
        x_cleaned = x[mask]
        y_cleaned = y[mask]
    else:
        x_cleaned = x
        y_cleaned = y

    # 第二次拟合（使用去除异常值后的数据）
    p_cleaned, y_fit_cleaned = np.polyfit(x_cleaned, y_cleaned, degree), np.poly1d(
        np.polyfit(x_cleaned, y_cleaned, degree))(x_cleaned)

    # 计算清除异常值前后的 R²
    ss_residual = np.sum((y - y_fit) ** 2)  # 清除前的残差平方和
    ss_total = np.sum((y - np.mean(y)) ** 2)  # 清除前的总平方和
    r_squared = 1 - (ss_residual / ss_total)

    ss_residual_cleaned = np.sum((y_cleaned - y_fit_cleaned) ** 2)  # 清除后的残差平方和
    ss_total_cleaned = np.sum((y_cleaned - np.mean(y_cleaned)) ** 2)  # 清除后的总平方和
    r_squared_cleaned = 1 - (ss_residual_cleaned / ss_total_cleaned)

    # 打印清除异常值前后的 R²
    print(f"清除异常值前的决定系数: R^2 = {r_squared:.12f}")
    print(f"清除异常值后的决定系数: R^2 = {r_squared_cleaned:.12f}")

    # 准备拟合函数的字符串表达式（优化科学计数法显示）
    def format_equation(p):
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

    equation_str = format_equation(p)
    equation_str_cleaned = format_equation(p_cleaned)

    # 绘制数据和拟合曲线
    plt.figure(figsize=(10, 6))

    # 绘制原始数据点
    plt.plot(x, y, marker='o', linestyle='', color='b', label="原始数据", markersize=3,
             markerfacecolor='white', markeredgewidth=1)

    # 绘制清除异常值后的数据点
    if remove_outliers:
        plt.plot(x_cleaned, y_cleaned, marker='o', linestyle='', color='g', label="清除异常值后的数据", markersize=3,
                 markerfacecolor='green', markeredgewidth=1)

    # 绘制清除前的拟合曲线
    plt.plot(x, y_fit, linestyle='--', color='r', label=f"清除前 {degree}次多项式拟合", linewidth=line_width)

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
    plt.xlabel("电压 (V)")
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线及拟合（清除异常值）")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()


# # 使用例 3: 使用 analyze_data_with_outlier_removal_1 进行分析
# file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径
# analyze_data_OutlierRemoval_1(file_path, degree=3, show_equation=True, show_r_squared=True,
#                                     line_style='--', line_color='r', line_width=1, remove_outliers=True, threshold=1)
