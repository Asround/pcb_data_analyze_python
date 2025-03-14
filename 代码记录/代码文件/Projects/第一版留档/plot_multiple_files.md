# plot_multiple_files

- 主要涉及两个函数

  1. plot_multiple_files
  2. plot_multiple_files_windowed

  -  二者功能一样

- 需要前置库, 需要引用 Parts.py 中的 read_VA 函数

## plot_multiple_files

- 代码功能:
  - 传入一个装有多个 .xlsx 表格文件的文件夹
  - 读取其中每一个表格的原始电压电流数据
    - 将多个表格的数据作图到同一个图中
- 代码内容:

```python
def plot_multiple_files(folder_path, colors=None, labels=None, line_styles=None, line_widths=None):
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

    # 遍历文件路径列表
    for i, file_path in enumerate(file_paths):
        # 读取 Excel 文件
        xls = pd.ExcelFile(file_path)
        df = xls.parse(sheet_name=0)

        # 读取 Excel 文件到 pd 中
        xls = pd.ExcelFile(file_path)
        df = xls.parse(sheet_name=0)

        # 提取电压电流数据
        x, y = pt.read_VA(df)

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


# # 使用例
# folder_path = './datas_learn/compare/compare2'  # 替换为你的文件夹路径
# # folder_path = './datas_learn/compare/compare1'  # 替换为你的文件夹路径
# plot_multiple_files(folder_path, colors=None, labels=None, line_styles=None, line_widths=None)

```

## plot_multiple_files

- 代码功能:
  - 和 plot_multiple_files 一样, 只是选择路径通过弹窗选择
- 注意: 弹窗展示的图像字号会变小, 目前还未解决(2025.2.15)
- 代码内容:

```python
def plot_multiple_files_windowed(colors=None, labels=None, line_styles=None, line_widths=None):
    """
    通过弹窗选择文件夹，绘制文件夹中所有 Excel 文件的数据到同一张图中，方便对比。
    需要: from tkinter.filedialog import askdirectory

    参数：
    - colors: 每个文件的曲线颜色列表，例如 ['b', 'r', 'g']。
    - labels: 每个文件的图例标签列表，例如 ["文件1", "文件2", "文件3"]。
    - line_styles: 每个文件的线型列表，例如 ['-', '--', ':']。
    - line_widths: 每个文件的线宽列表，例如 [1.5, 1.5, 1.5]。
    """
    # 弹窗选择文件夹
    Tk().withdraw()  # 隐藏 Tkinter 根窗口
    folder_path = askdirectory(title="选择一个 .xlsx 文件")

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

    # 遍历文件路径列表
    for i, file_path in enumerate(file_paths):
        # 读取 Excel 文件
        xls = pd.ExcelFile(file_path)
        df = xls.parse(sheet_name=0)

        # 提取电压电流数据
        x, y = pt.read_VA(df)

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


# # 使用例
# plot_multiple_files_windowed(colors=None, labels=None, line_styles=None, line_widths=None)
```