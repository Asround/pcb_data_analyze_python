import numpy as np
import matplotlib.pyplot as plt

def plot_single(x, y, y_fit, p, degree, show_equation, show_r_squared, line_style, line_color, line_width, connect_points, use_log=False):
    """
    绘制数据和拟合曲线。

    参数：
    - x: 电压数据。
    - y: 原始电流数据。
    - y_fit: 拟合后的电流值。
    - p: 拟合多项式的系数。
    - degree: 多项式拟合的次数。
    - show_equation: 是否显示拟合函数表达式。
    - show_r_squared: 是否显示决定系数 R²。
    - line_style: 拟合曲线的线型。
    - line_color: 拟合曲线的颜色。
    - line_width: 拟合曲线的线宽。
    - connect_points: 是否连接原始数据点。
    - use_log: 是否对横轴进行对数化处理。
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


def plot_removal_1(x, y, x_cleaned, y_cleaned, y_fit, y_fit_cleaned, equation_str, equation_str_cleaned,
                 r_squared, r_squared_cleaned, degree, line_style, line_color, line_width,
                 show_equation=True, show_r_squared=True, remove_outliers=True, use_log=False):
    """
    绘制电压-电流曲线及拟合（清除异常值）

    Parameters:
    - x: 原始 x 数据（电压）
    - y: 原始 y 数据（电流）
    - x_cleaned: 清除异常值后的 x 数据
    - y_cleaned: 清除异常值后的 y 数据
    - y_fit: 清除前的拟合曲线 y 数据
    - y_fit_cleaned: 清除后的拟合曲线 y 数据
    - equation_str: 清除前拟合的函数表达式
    - equation_str_cleaned: 清除后拟合的函数表达式
    - r_squared: 清除前拟合的 R² 值
    - r_squared_cleaned: 清除后拟合的 R² 值
    - degree: 多项式拟合的次数
    - line_style: 拟合曲线的样式
    - line_color: 拟合曲线的颜色
    - line_width: 拟合曲线的宽度
    - show_equation: 是否显示拟合函数表达式 (默认 True)
    - show_r_squared: 是否显示 R² 值 (默认 True)
    - remove_outliers: 是否显示清除异常值后的数据点 (默认 True)
    - use_log: 是否对横轴进行对数化处理。
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


def plot_removal_2(x, y, x_cleaned, y_cleaned, y_fit_cleaned, equation_str_cleaned, r_squared_cleaned, degree,
                   show_equation=True, show_r_squared=True, line_style='--', line_color='r', line_width=1.5, use_log=False):
    """
    绘制数据和拟合曲线。

    参数：
    - x: 原始数据的 x 值。
    - y: 原始数据的 y 值。
    - x_cleaned: 清除异常值后的 x 值。
    - y_cleaned: 清除异常值后的 y 值。
    - y_fit_cleaned: 清除异常值后的拟合 y 值。
    - equation_str_cleaned: 清除异常值后的拟合函数表达式。
    - r_squared_cleaned: 清除异常值后的决定系数 R²。
    - degree: 多项式拟合的次数。
    - show_equation: 是否在图中显示拟合函数表达式，默认显示。
    - show_r_squared: 是否显示决定系数 R²，默认显示。
    - line_style: 曲线的线型，默认为 '-'（实线）。
    - line_color: 曲线的颜色，默认为 'b'（蓝色）。
    - line_width: 曲线的线宽，默认为 1.5。
    - use_log: 是否对横轴进行对数化处理。
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
