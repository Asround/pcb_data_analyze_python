# iterate_fitting_OutlierRemoval


## 基本说明

- 含 iterate_fitting_OutlierRemoval 和 iterate_fitting_OutlierRemoval_windowed 两个版本
  - 后者可以用弹窗选择路径, 稍方便
  - 但存在不同分辨率显示器显示不同的问题, 效果不好时请使用前者
- 需要前置库 (查看"所需库.md"文件)
- 需引用 Part.py 中的函数 (具体不列举)

## 代码部分

- 参数说明(更加具体的内容请看代码, 以及b站配套视频)

| 参数              | 参数说明                     |
| ----------------- | ---------------------------- |
| file_path         | .xlsx表格路径                |
| degree            | 多项式拟合的最高次数         |
| show_eqution      | 是否在图片中展示多项式表达式 |
| show_r_squared    | 是否在图片中展示决定系数     |
| line_style        | 拟合曲线的线型               |
| line_color        | 拟合曲线的颜色               |
| line_width        | 拟合曲线的宽度               |
| remove_outliers   | 是否进行去除离去值操作       |
| target_r_squared  | 目标决定系数值               |
| min_threshold     | 最小可接受离群值去除阈值     |
| initial_threshold | 初始离群值去除阈值           |

- 功能:

  - analyze_data_OutlierRemoval 基础上, 连续去除离群值和再拟合. 直到达到一定程度停止.

- 代码内容:

  ```python
  def iterate_fitting_OutlierRemoval(file_path, degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                    line_color='r', line_width=1.5, remove_outliers=True, target_r_squared=0.9,
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
      # 读取 Excel 文件, 提取电压电流数据
      x, y = pt.read_xlsx(file_path)
  
      # 初始化变量
      threshold = initial_threshold
      x_cleaned, y_cleaned = x, y
      r_squared_cleaned = 0
  
      # 迭代清除异常值 IMPT: 迭代清除数据, 直至达到效果
      if remove_outliers:
          while threshold >= min_threshold:
              x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned = pt.fit_and_remove_outliers(x_cleaned,
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
          p_cleaned, y_fit_cleaned = pt.polynomial_fit(x_cleaned, y_cleaned, degree)
  
          # 计算 R²（决定系数）- 清除后
          r_squared_cleaned = pt.calculate_r_squared(y_cleaned, y_fit_cleaned)
  
  
      # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
      equation_str_cleaned =pt.format_equation(p_cleaned, degree)
  
      # 调用画图函数
      pt.plot_removal_2(x, y, x_cleaned, y_cleaned, y_fit_cleaned, equation_str_cleaned, r_squared_cleaned, degree,
                     show_equation, show_r_squared, line_style, line_color, line_width)
  
  
  # # 使用例: 使用 iterate_fitting_OutlierRemoval 进行分析
  # file_path = "./datas_learn/B00.xlsx"  # 替换为你自己的文件路径
  # iterate_fitting_OutlierRemoval(file_path, degree=3, show_equation=False, show_r_squared=True,
  #                               line_style='--', line_color='r', line_width=1, remove_outliers=True,
  #                               target_r_squared=0.9, min_threshold=1, initial_threshold=3)
  ```

  - windowed 版本

    ```py
    def iterate_fitting_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                      line_color='r', line_width=1.5, remove_outliers=True, target_r_squared=0.9,
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
        file_path = pt.select_file()
        if not file_path:
            print("未选择文件。")
            return
    
        # 读取 Excel 文件, 提取电压电流数据
        x, y = pt.read_xlsx(file_path)
    
        # 初始化变量
        threshold = initial_threshold
        x_cleaned, y_cleaned = x, y
        r_squared_cleaned = 0
    
        # 迭代清除异常值 IMPT: 迭代清除数据, 直至达到效果
        if remove_outliers:
            while threshold >= min_threshold:
                x_cleaned, y_cleaned, p_cleaned, y_fit_cleaned, r_squared_cleaned = pt.fit_and_remove_outliers(x_cleaned,
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
            p_cleaned, y_fit_cleaned = pt.polynomial_fit(x_cleaned, y_cleaned, degree)
    
            # 计算 R²（决定系数）- 清除后
            r_squared_cleaned = pt.calculate_r_squared(y_cleaned, y_fit_cleaned)
    
        # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
        equation_str_cleaned =pt.format_equation(p_cleaned, degree)
    
        # 调用画图函数
        pt.plot_removal_2(x, y, x_cleaned, y_cleaned, y_fit_cleaned, equation_str_cleaned, r_squared_cleaned, degree,
                       show_equation, show_r_squared, line_style, line_color, line_width)
    
    
    # # 使用例: 使用 iterate_fitting_OutlierRemove_windowed 进行分析
    # iterate_fitting_OutlierRemoval_windowed(degree=3, show_equation=False, show_r_squared=True,
    #                               line_style='--', line_color='r', line_width=1, remove_outliers=True,
    #                               target_r_squared=0.9, min_threshold=1, initial_threshold=3)
    ```