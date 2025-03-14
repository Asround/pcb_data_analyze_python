# batch_analyze_data


## 基本说明

- 含 batch_analyze_data 和 batch_analyze_data_windowed 两个版本
  - 后者可以用弹窗选择路径, 稍方便
  - 但存在不同分辨率显示器显示不同的问题, 效果不好时请使用前者
- 需要前置库 (查看"所需库.md"文件)
- 需引用 Part.py 中的函数 (具体不列举)

## 代码部分

- 参数说明(更加具体的内容请看代码, 以及b站配套视频)

| 参数           | 参数说明                           |
| -------------- | ---------------------------------- |
| folder_path    | 含.xlsx表格文件的文件夹路径        |
| output_folder  | 指定图像输出路径(可以且建议不指定) |
| degree         | 多项式拟合的最高次数               |
| show_eqution   | 是否在图片中展示多项式表达式       |
| show_r_squared | 是否在图片中展示决定系数           |
| line_style     | 拟合曲线的线型                     |
| line_color     | 拟合曲线的颜色                     |
| line_width     | 拟合曲线的宽度                     |
| connect_points | 是否将原数据点依次连接             |

- 功能:

  - 对文件夹内多表格进行原数据画图, 无弹窗, 在同一张图中进行比较 (程序自动保存图像)

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
  
  - windowed 版本
  
    ```py
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