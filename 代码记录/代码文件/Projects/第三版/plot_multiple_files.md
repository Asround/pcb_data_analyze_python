# plot_multiple_files


## 基本说明

- 含 plot_multiple_files 和 plot_multiple_files_windowed 两个版本
  - 后者可以用弹窗选择路径, 稍方便
  - 但存在不同分辨率显示器显示不同的问题, 效果不好时请使用前者
- 需要前置库 (查看"所需库.md"文件)
- 需引用 Part.py 中的函数 (具体不列举)

## 代码部分

- 参数说明(更加具体的内容请看代码, 以及b站配套视频)

| 参数        | 参数说明                    |
| ----------- | --------------------------- |
| folder_path | 含.xlsx表格文件的文件夹路径 |
| line_styles | 拟合曲线的线型列表          |
| line_colors | 拟合曲线的颜色列表          |
| line_widths | 拟合曲线的宽度列表          |

- 功能:

  - 对文件夹内多表格进行原数据画图, 弹窗出现图片, 在同一张图中进行比较 (不自动保存图像)

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
          # 读取 Excel 文件, 提取电压电流数据
          x, y = pt.read_xlsx(file_path)
  
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
  
  - windowed 版本
  
    ```py
    def plot_multiple_files_windowed(colors=None, labels=None, line_styles=None, line_widths=None):
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
    
        # 遍历文件路径列表
        for i, file_path in enumerate(file_paths):
            # 读取 Excel 文件, 提取电压电流数据
            x, y = pt.read_xlsx(file_path)
    
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