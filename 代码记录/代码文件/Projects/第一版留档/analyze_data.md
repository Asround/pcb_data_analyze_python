# analyze_data

- 主要涉及两个函数
  1. analyze_data
  2. analyze_data_windowed
  -  二者功能一样

- 需要前置库, 需要引用 Parts.py 中的 read_VA 函数

## analyze_data

- 代码功能:
  - 传入一个 .xlsx 表格文件
  - 读取其中的原始电压电流数据
    - 用数据: (1)画图	(2)做多项式拟合
- 代码内容:

```python
def analyze_data(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
                 line_width=1.5, connect_points=False):
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

    # 读取 Excel 文件
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name=0)

    # 提取电压电流数据
    x, y = pt.read_VA(df)

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


# # 使用例 : 以下两个路径分别对应不同类型的xlsx文件, 可分别运行测试
# file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径(一定要是.xlsx文件!)
# # file_path = "./datas_learn/B4.xlsx"  # 替换为你自己的文件路径(一定要是.xlsx文件!)
#
# # 分析file_path对应路径的文件, 用3次多项式进行拟合, 拟合多项式表达式和决定系数均展示, 拟合曲线的线型为虚线, 红色, 宽度为1
# analyze_data(file_path, degree=3, show_equation=False, show_r_squared=True, line_style='--', line_color='r',
#              line_width=1, connect_points=True)
```

## analyze_data_windowed

- 代码功能:
  - 和 analyze_data 一样, 只是选择路径通过弹窗选择
- 注意: 弹窗展示的图像字号会变小, 目前还未解决(2025.2.15)
- 代码内容:

```python
def analyze_data_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
                          line_width=1.5, connect_points=False):
    """
    通过弹窗选择文件路径，读取数据，进行多项式拟合并绘制结果。
    需要: from tkinter import Tk, filedialog


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
    Tk().withdraw()  # 隐藏 Tkinter 根窗口
    file_path = filedialog.askopenfilename(title="选择 Excel 文件", filetypes=[("Excel files", "*.xlsx *.xls")])

    if not file_path:
        print("未选择文件。")
        return

    # 读取 Excel 文件
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name=0)

    # 提取电压电流数据（假设电压在 'V' 列，电流在 'A' 列）
    x, y = pt.read_VA(df)

    # 多项式拟合
    p = np.polyfit(x, y, degree)
    poly = np.poly1d(p)
    y_fit = poly(x)

    # 计算 R²
    ss_residual = np.sum((y - y_fit) ** 2)
    ss_total = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_residual / ss_total)

    # 准备拟合函数的字符串表达式
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
    equation_str = " + ".join(equation_terms)

    # 绘制数据和拟合曲线
    plt.figure(figsize=(8, 6))

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
        plt.text(0.0, 0.06, f"拟合函数: $y = {equation_str}$", transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8))

    # 添加 R² 值
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


# # 使用例
# analyze_data_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
#                          line_width=1.5, connect_points=False)
```