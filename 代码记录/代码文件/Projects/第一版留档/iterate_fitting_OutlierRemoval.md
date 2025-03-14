# iterate_fitting_OutlierRemoval_windowed

- 主要涉及两个函数

  1. iterate_fitting_OutlierRemoval
  2. iterate_fitting_OutlierRemoval_windowed

  -  二者功能一样

- 需要前置库, 需要引用 Parts.py 中的 read_VA 函数

## iterate_fitting_OutlierRemoval

- 代码功能:
  - 首先具有和 analyze_data_OutlierRemoval 函数一样的功能
  - 并且可以将去除离群值和拟合操作反复进行下去, 直到达到某些限制或要求才停止
- 代码内容:

```python
def iterate_fitting_OutlierRemoval(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='-',
                                  line_color='b', line_width=1.5, remove_outliers=True, target_r_squared=0.9,
                                  min_threshold=0.3, initial_threshold=3):
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
    # 读取 Excel 文件
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name=0)

    # 提取电压电流数据
    x, y = pt.read_VA(df)

    # 定义异常值清除和拟合的函数
    def fit_and_remove_outliers(x, y, degree, threshold):
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

        # 计算 R²
        ss_residual_cleaned = np.sum((y_cleaned - y_fit_cleaned) ** 2)  # 清除后的残差平方和
        ss_total_cleaned = np.sum((y_cleaned - np.mean(y_cleaned)) ** 2)  # 清除后的总平方和
        r_squared_cleaned = 1 - (ss_residual_cleaned / ss_total_cleaned)

        return x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned

    # 初始化变量
    threshold = initial_threshold
    x_cleaned, y_cleaned = x, y
    r_squared_cleaned = 0

    # 迭代清除异常值 IMPT: 迭代清除数据, 直至达到效果
    if remove_outliers:
        while threshold >= min_threshold:
            x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned = fit_and_remove_outliers(x_cleaned,
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
        p_cleaned, y_fit_cleaned = np.polyfit(x_cleaned, y_cleaned, degree), np.poly1d(
            np.polyfit(x_cleaned, y_cleaned, degree))(x_cleaned)
        ss_residual_cleaned = np.sum((y_cleaned - y_fit_cleaned) ** 2)  # 清除后的残差平方和
        ss_total_cleaned = np.sum((y_cleaned - np.mean(y_cleaned)) ** 2)  # 清除后的总平方和
        r_squared_cleaned = 1 - (ss_residual_cleaned / ss_total_cleaned)

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
    plt.xlabel("电压 (V)")
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线及拟合（清除异常值）")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()


# # 使用例: 使用 iterate_fitting_OutlierRemoval 进行分析
# file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径
# iterate_fitting_OutlierRemoval(file_path, degree=3, show_equation=False, show_r_squared=True,
#                               line_style='--', line_color='r', line_width=1, remove_outliers=True,
#                               target_r_squared=0.9, min_threshold=1, initial_threshold=3)

```

## iterate_fitting_OutlierRemoval_windowed

- 代码功能:
  - 和 iterate_fitting_OutlierRemoval 一样, 只是选择路径通过弹窗选择
- 注意: 弹窗展示的图像字号会变小, 目前还未解决(2025.2.15)
- 代码内容:

```python
def iterate_fitting_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='-',
                                  line_color='b', line_width=1.5, remove_outliers=True, target_r_squared=0.9,
                                  min_threshold=0.3, initial_threshold=3):
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
    Tk().withdraw()  # 隐藏 Tkinter 根窗口
    file_path = filedialog.askopenfilename(title="选择 Excel 文件", filetypes=[("Excel files", "*.xlsx *.xls")])

    if not file_path:
        print("未选择文件。")
        return


    # 读取 Excel 文件
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name=0)

    # 提取电压电流数据
    x, y = pt.read_VA(df)

    # 定义异常值清除和拟合的函数
    def fit_and_remove_outliers(x, y, degree, threshold):
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

        # 计算 R²
        ss_residual_cleaned = np.sum((y_cleaned - y_fit_cleaned) ** 2)  # 清除后的残差平方和
        ss_total_cleaned = np.sum((y_cleaned - np.mean(y_cleaned)) ** 2)  # 清除后的总平方和
        r_squared_cleaned = 1 - (ss_residual_cleaned / ss_total_cleaned)

        return x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned

    # 初始化变量
    threshold = initial_threshold
    x_cleaned, y_cleaned = x, y
    r_squared_cleaned = 0

    # 迭代清除异常值 IMPT: 迭代清除数据, 直至达到效果
    if remove_outliers:
        while threshold >= min_threshold:
            x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned = fit_and_remove_outliers(x_cleaned,
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
        p_cleaned, y_fit_cleaned = np.polyfit(x_cleaned, y_cleaned, degree), np.poly1d(
            np.polyfit(x_cleaned, y_cleaned, degree))(x_cleaned)
        ss_residual_cleaned = np.sum((y_cleaned - y_fit_cleaned) ** 2)  # 清除后的残差平方和
        ss_total_cleaned = np.sum((y_cleaned - np.mean(y_cleaned)) ** 2)  # 清除后的总平方和
        r_squared_cleaned = 1 - (ss_residual_cleaned / ss_total_cleaned)

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
    plt.xlabel("电压 (V)")
    plt.ylabel("电流 (A)")
    plt.title("电压-电流曲线及拟合（清除异常值）")
    plt.legend()
    plt.grid(True)

    # 显示图像
    plt.show()


# # 使用例: 使用 iterate_fitting_OutlierRemove_windowed 进行分析
# iterate_fitting_OutlierRemoval_windowed(degree=3, show_equation=False, show_r_squared=True,
#                               line_style='--', line_color='r', line_width=1, remove_outliers=True,
#                               target_r_squared=0.9, min_threshold=1, initial_threshold=3)

```

