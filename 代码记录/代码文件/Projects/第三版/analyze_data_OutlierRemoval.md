# analyze_data_OutlierRemoval


## 基本说明

- 含 analyze_data_OutlierRemoval 和 analyze_data_OutlierRemoval_windowed 两个版本
  - 后者可以用弹窗选择路径, 稍方便
  - 但存在不同分辨率显示器显示不同的问题, 效果不好时请使用前者
- 需要前置库 (查看"所需库.md"文件)
- 需引用 Part.py 中的函数 (具体不列举)

## 代码部分

- 参数说明(更加具体的内容请看代码, 以及b站配套视频)

| 参数            | 参数说明                     |
| --------------- | ---------------------------- |
| file_path       | .xlsx表格路径                |
| degree          | 多项式拟合的最高次数         |
| show_eqution    | 是否在图片中展示多项式表达式 |
| show_r_squared  | 是否在图片中展示决定系数     |
| line_style      | 拟合曲线的线型               |
| line_color      | 拟合曲线的颜色               |
| line_width      | 拟合曲线的宽度               |
| remove_outliers | 是否进行去除离去值操作       |
| threshold       | 离群值去除阈值(具体看视频)   |

- 功能:

  - 对表格进行原数据画图, 多项式拟合, 依据首次拟合结果进行一次离群值去除操作后再进行二次多项式拟合. 弹窗出现图片, 在同一张图中进行比较 (不自动保存图像)

- 代码内容:

  ```python
  def analyze_data_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                  line_color='r', line_width=1.5, remove_outliers=True, threshold=3):
      """
      读取数据，进行多项式拟合并绘制结果，支持去除异常值。
  
      参数：
      - file_path: Excel 文件的路径。
      - degree: 多项式拟合的次数，默认3。
      - show_equation: 是否在图中显示拟合函数表达式，默认显示。
      - show_r_squared: 是否显示决定系数R²，默认显示。
      - line_style: 曲线的线型，默认为 '--'（虚线）。
      - line_color: 曲线的颜色，默认为 'r'（红色）。
      - line_width: 曲线的线宽，默认为 1.5。
      - remove_outliers: 是否去除异常值，默认 True。
      - threshold: 异常值判断的阈值（基于残差的标准差倍数），默认 3。
      """
  
      # 弹窗选择文件
      file_path = pt.select_file()
      if not file_path:
          print("未选择文件。")
          return
  
  
      # 读取 Excel 文件, 提取电压电流数据
      x, y = pt.read_xlsx(file_path)
  
      # 第一次拟合（用于检测异常值）
      p, y_fit = pt.polynomial_fit(x, y, degree)
      residuals = y - y_fit  # 计算残差
      residual_std = np.std(residuals)  # 残差的标准差
  
      # 去除异常值 DETAIL: 两种清除离群值(异常值)方法, 并将两种清除后的数据取交集
      if remove_outliers:
          # 方法 1：基于残差的绝对值
          mask_residual = np.abs(residuals) <= threshold * residual_std
  
          # 方法 2：基于局部离群点检测（Isolation Forest）
          clf = IsolationForest(contamination=0.05)  # 假设 5% 的数据是异常值
          mask_isolation = clf.fit_predict(np.column_stack((x, y))) == 1
  
          # 结合两种方法
          mask = mask_residual & mask_isolation
  
          x_cleaned = x[mask]
          y_cleaned = y[mask]
      else:
          x_cleaned = x
          y_cleaned = y
  
      # 第二次拟合（使用去除异常值后的数据）
      p_cleaned, y_fit_cleaned = pt.polynomial_fit(x_cleaned, y_cleaned, degree)
  
      # 计算 R²（决定系数）
      r_squared = pt.calculate_r_squared(y,y_fit)
  
      # 计算 R²（决定系数）- 清除后
      r_squared_cleaned =pt.calculate_r_squared(y_cleaned,y_fit_cleaned)
  
      # 打印清除异常值前后的 R²
      print(f"清除异常值前的决定系数: R^2 = {r_squared:.12f}")
      print(f"清除异常值后的决定系数: R^2 = {r_squared_cleaned:.12f}")
  
      # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
      equation_str =pt.format_equation(p, degree)
      equation_str_cleaned =pt.format_equation(p_cleaned, degree)
  
      # 绘制图像
      pt.plot_removal_1(x, y, x_cleaned, y_cleaned, y_fit, y_fit_cleaned, equation_str, equation_str_cleaned,
                   r_squared, r_squared_cleaned, degree, line_style, line_color, line_width,
                   show_equation, show_r_squared, remove_outliers)
  
  
  # # 使用例 : 使用 analyze_data_OutlierRemoval_windowed 进行分析
  # analyze_data_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True,
  #                                     line_style='--', line_color='r', line_width=1, remove_outliers=True, threshold=2)
  ```

  - windowed 版本

    ```py
    def analyze_data_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True, line_style='--',
                                    line_color='r', line_width=1.5, remove_outliers=True, threshold=3):
        """
        读取数据，进行多项式拟合并绘制结果，支持去除异常值。
    
        参数：
        - file_path: Excel 文件的路径。
        - degree: 多项式拟合的次数，默认3。
        - show_equation: 是否在图中显示拟合函数表达式，默认显示。
        - show_r_squared: 是否显示决定系数R²，默认显示。
        - line_style: 曲线的线型，默认为 '--'（虚线）。
        - line_color: 曲线的颜色，默认为 'r'（红色）。
        - line_width: 曲线的线宽，默认为 1.5。
        - remove_outliers: 是否去除异常值，默认 True。
        - threshold: 异常值判断的阈值（基于残差的标准差倍数），默认 3。
        """
    
        # 弹窗选择文件
        file_path = pt.select_file()
        if not file_path:
            print("未选择文件。")
            return
    
    
        # 读取 Excel 文件, 提取电压电流数据
        x, y = pt.read_xlsx(file_path)
    
        # 第一次拟合（用于检测异常值）
        p, y_fit = pt.polynomial_fit(x, y, degree)
        residuals = y - y_fit  # 计算残差
        residual_std = np.std(residuals)  # 残差的标准差
    
        # 去除异常值 DETAIL: 两种清除离群值(异常值)方法, 并将两种清除后的数据取交集
        if remove_outliers:
            # 方法 1：基于残差的绝对值
            mask_residual = np.abs(residuals) <= threshold * residual_std
    
            # 方法 2：基于局部离群点检测（Isolation Forest）
            clf = IsolationForest(contamination=0.05)  # 假设 5% 的数据是异常值
            mask_isolation = clf.fit_predict(np.column_stack((x, y))) == 1
    
            # 结合两种方法
            mask = mask_residual & mask_isolation
    
            x_cleaned = x[mask]
            y_cleaned = y[mask]
        else:
            x_cleaned = x
            y_cleaned = y
    
        # 第二次拟合（使用去除异常值后的数据）
        p_cleaned, y_fit_cleaned = pt.polynomial_fit(x_cleaned, y_cleaned, degree)
    
        # 计算 R²（决定系数）
        r_squared = pt.calculate_r_squared(y,y_fit)
    
        # 计算 R²（决定系数）- 清除后
        r_squared_cleaned =pt.calculate_r_squared(y_cleaned,y_fit_cleaned)
    
        # 打印清除异常值前后的 R²
        print(f"清除异常值前的决定系数: R^2 = {r_squared:.12f}")
        print(f"清除异常值后的决定系数: R^2 = {r_squared_cleaned:.12f}")
    
        # 准备拟合函数的字符串表达式（优化科学计数法显示）, 并拼接拟合函数表达式
        equation_str =pt.format_equation(p, degree)
        equation_str_cleaned =pt.format_equation(p_cleaned, degree)
    
        # 绘制图像
        pt.plot_removal_1(x, y, x_cleaned, y_cleaned, y_fit, y_fit_cleaned, equation_str, equation_str_cleaned,
                     r_squared, r_squared_cleaned, degree, line_style, line_color, line_width,
                     show_equation=True, show_r_squared=True, remove_outliers=True)
    
    
    # # 使用例 : 使用 analyze_data_OutlierRemoval_windowed 进行分析
    # analyze_data_OutlierRemoval_windowed(degree=3, show_equation=True, show_r_squared=True,
    #                                     line_style='--', line_color='r', line_width=1, remove_outliers=True, threshold=2)
    ```