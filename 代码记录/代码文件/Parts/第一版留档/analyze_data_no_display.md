# analyze_data_no_display

## 代码内容

```python
def analyze_data_no_display(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='-', line_color='b',
                           line_width=1.5, connect_points=True):
    """
    与 analyze_data 功能相同，但不显示图像。
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
        equation_terms.append(term)# 使用 {{}} 包裹幂次 防止出现x^10的情况出现 (LaTex规范:x^{10})

    # 拼接拟合函数表达式
    equation_str = " + ".join(equation_terms)

    # 计算 R²（决定系数）
    ss_residual = np.sum((y - y_fit) ** 2)  # 残差平方和
    ss_total = np.sum((y - np.mean(y)) ** 2)  # 总平方和
    r_squared = 1 - (ss_residual / ss_total)

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
        # plt.text(0.0, 0.06, f"拟合函数: $y = {equation_str}$", transform=plt.gca().transAxes, fontsize=12,
        #          verticalalignment='top', ha='left', bbox=dict(facecolor='white', alpha=0.8)
        plt.text(0.01, 0.06, f"$y = {equation_str}$", transform=plt.gca().transAxes, fontsize=12,
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

    # 返回图像对象
    return plt.gcf()
```

## 说明

和 Projects 中的 analyze_data 函数功能一致, 只是删去了展示功能

- 主要用在 Projects 的 batch_analyze_data 和 batch_analyze_data_windowed 函数中
  - 在循环体内被反复调用来画图