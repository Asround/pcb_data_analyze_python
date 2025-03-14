# analyze_data

## 基本说明

- 含 analyze_data 和 analyze_data_windowed 两个版本
  - 后者可以用弹窗选择路径, 稍方便
  - 但存在不同分辨率显示器显示不同的问题, 效果不好时请使用前者
- 需要前置库 (查看"所需库.md"文件)
- 需引用 Part.py 中的函数 (具体不列举)

## 代码部分

- 参数说明(更加具体的内容请看代码, 以及b站配套视频)

| 参数           | 参数说明                     |
| -------------- | ---------------------------- |
| file_path      | .xlsx表格路径                |
| degree         | 多项式拟合的最高次数         |
| show_eqution   | 是否在图片中展示多项式表达式 |
| show_r_squared | 是否在图片中展示决定系数     |
| line_style     | 拟合曲线的线型               |
| line_color     | 拟合曲线的颜色               |
| line_width     | 拟合曲线的宽度               |
| connect_points | 是否将原数据点依次连接       |

- 功能:

  - 对单个表格进行原数据画图 + 多项式曲线拟合 (不自动保存图像)

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
  
      # 读取 Excel 文件, 提取电压电流数据
      x, y = pt.read_xlsx(file_path)
  
      # 多项式拟合
      p, y_fit = pt.polynomial_fit(x, y, degree)
  
      # 打印拟合的多项式系数
      print(f"拟合多项式的系数（从高次到低次）: {p}")
  
      # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
      equation_str = pt.format_equation(p, degree)
  
      # 计算 R²（决定系数）
      r_squared = pt.calculate_r_squared(y,y_fit)
  
      # 打印 R² 值
      print(f"决定系数: R^2 = {r_squared:.12f}")  # 12位保证在拟合效果较好时能看出差距
  
      # 作图, 原数据及拟合曲线
      pt.plot_single(x, y, y_fit, p, degree, show_equation, show_r_squared, line_style, line_color, line_width,
                      connect_points)
  
  
  # # 使用例 : 以下两个路径分别对应不同类型的xlsx文件, 可分别运行测试
  # file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径(一定要是.xlsx文件!)
  # # file_path = "./datas_learn/B4.xlsx"  # 替换为你自己的文件路径(一定要是.xlsx文件!)
  #
  # # 分析file_path对应路径的文件, 用3次多项式进行拟合, 拟合多项式表达式和决定系数均展示, 拟合曲线的线型为虚线, 红色, 宽度为1
  # analyze_data(file_path, degree=3, show_equation=False, show_r_squared=True, line_style='--', line_color='r',
  #              line_width=1, connect_points=True)
  ```

  - windowed 版本

    ```py
    def analyze_data_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
                              line_width=1.5, connect_points=False):
        """
        通过弹窗选择文件路径，读取数据，进行多项式拟合并绘制结果。
    
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
        file_path = pt.select_file()
        if not file_path:
            # 如果没有选取文件或者读取失败, 通知用户
            print("未选择文件。")
            return
    
        # 读取 Excel 文件, 提取电压电流数据
        x, y = pt.read_xlsx(file_path)
    
        # 多项式拟合
        p, y_fit = pt.polynomial_fit(x, y, degree)
    
        # 计算 R²（决定系数）
        r_squared = pt.calculate_r_squared(y,y_fit)
    
        # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
        equation_str =pt.format_equation(p, degree)
    
        # 作图, 原数据及拟合曲线
        pt.plot_single(x, y, y_fit, p, degree, show_equation, show_r_squared, line_style, line_color, line_width,
                        connect_points)
    
    
    # # 使用例
    # analyze_data_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--', line_color='r',
    #                          line_width=1.5, connect_points=False)
    ```
