# batch_analyze_data

- 主要涉及两个函数

  1. batch_analyze_data
  2. batch_analyze_data_windowed

  -  二者功能一样

- 需要前置库

- 需要引用 Parts.py 中的 read_VA 函数

- 需要引用 Parts.py 中的 analyze_data_no_display 函数

## batch_analyze_data

- 代码功能:
  - 传入一个装有多个 .xlsx 表格文件的文件夹
  - 读取其中每一个表格的原始电压电流数据
    - 将每一个表格单独作图并保存到原本目录下的 ..._img 文件夹中
    - 作图效果和 analyze_data 函数一致(原数据+多项式拟合)
- 代码内容:

```python
def batch_analyze_data(folder_path, output_folder=None, degree=3, show_equation=True, show_r_squared=True,
                       line_style='--',line_color='r', line_width=1.5, connect_points=False):
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
                                          line_width, connect_points)
            # 保存图像
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.png")
            fig.savefig(output_file_path, dpi=240)
            plt.close(fig)
            print(f"已保存图像: {output_file_path}")
    print('分析完成.')


# # 使用例
# folder_path = './datas_learn/many1'
# batch_analyze_data(folder_path, degree= 3, line_style='--', line_color='r', connect_points=False)

```

## batch_analyze_data_windowed

- 代码功能:
  - 和 batch_analyze_data 一样, 只是选择路径通过弹窗选择
- 注意: 弹窗展示的图像字号会变小, 目前还未解决(2025.2.15)
- 代码内容:

```python
def batch_analyze_data_windowed(output_folder=None, degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                line_color='r', line_width=1.5, connect_points=False):
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
    Tk().withdraw()  # 隐藏 Tkinter 根窗口
    folder_path = filedialog.askdirectory(title="选择包含 .xlsx 文件的文件夹")

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
                                             line_color,
                                             line_width, connect_points)

            # 保存图像
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.png")
            plt.savefig(output_file_path, dpi=240)
            plt.close()
            print(f"已保存图像: {output_file_path}")

    print('分析完成.')


# # 使用弹窗选择文件夹路径并批量分析
# batch_analyze_data_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--',
#                             line_color='r', line_width=1.5, connect_points=False)
```

