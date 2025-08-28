"""
用于测试各种函数的先行版本.
测试好后会放到 Parts 或者 Projects 中.
个别早期版本和垃圾版本放到 Others 文件夹的 Old_Functions 和 Trash 中.
"""
import os
import re
import shutil

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') # 解决PyCharm的Matplotlib后端与当前Matplotlib版本不兼容问题
import numpy as np
from pygame.examples.testsprite import use_rle
from sklearn.ensemble import IsolationForest # 去除离群值函数需要

from tkinter import Tk, filedialog
from tkinter.filedialog import askdirectory

import Parts as pt
import Projects as pjc


# 设置中文字体，解决字体显示问题
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 例如使用微软雅黑（SimHei）
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""-------------------全函数统一测试 (注意画图的函数 batch_analyze_data 需要到文件夹中自行查看画图结果)-------------------------"""
'''
修改任意函数后在此处可以快速解除注释并运行查看情况
'''
# #
# folder_path = './datas_learn/compare/d_B_compare2'
# file_path = './datas_learn/B00.xlsx'
# batch_path = './datas_learn/csv/csv2/xlsx'
#
# pjc.analyze_data(file_path)
# pjc.analyze_data_windowed()
#
# pjc.plot_multiple_files(folder_path)
# pjc.plot_multiple_files_windowed()
#
# pjc.analyze_data_OutlierRemoval(file_path)
# pjc.analyze_data_OutlierRemoval_windowed()
#
# pjc.iterate_fitting_OutlierRemoval(file_path)
# pjc.iterate_fitting_OutlierRemoval_windowed()

# pjc.batch_analyze_data(batch_path)
# pjc.batch_analyze_data_windowed()

"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""
'''
查看对数处理后的函数运行情况
'''
# #
# folder_path = './datas_learn/compare/d_B_compare2'
# file_path = './datas_learn/B00.xlsx'
# batch_path = './datas_learn/csv/csv2/xlsx'

# pjc.analyze_data(file_path, use_log=True)
# pjc.analyze_data_windowed(use_log=True)
#
# pjc.plot_multiple_files(folder_path, use_log=True)
# pjc.plot_multiple_files_windowed(use_log=True)
#
# pjc.analyze_data_OutlierRemoval(file_path, use_log=True)
# pjc.analyze_data_OutlierRemoval_windowed(use_log=True)
#
# pjc.iterate_fitting_OutlierRemoval(file_path, use_log=True)
# pjc.iterate_fitting_OutlierRemoval_windowed(use_log=True)
#
# # pjc.batch_analyze_data(batch_path, use_log=True)
# # pjc.batch_analyze_data_windowed(use_log=True)


"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""
"""
分类文件测试
"""
# import os
# import shutil
# import re
#
# def sort_variable(root_dir, sort_standard=None, sort_all=False):
#     if not sort_standard and not sort_all:
#         print("No sort standard provided. Function will not execute.")
#         return
#
#     # 定义占位符规则
#     placeholder_map = {
#         'P': 'P',  # 走线类型
#         'd': 'd',  # 导线间距
#         'n': 'n',  # 序号
#         't': 't',  # 实验次数
#         'g': 'g',  # 实验组别
#         'e': 'e',  # 辐照注量
#         'v': 'v'   # 偏压
#     }
#
#     # 创建 compare_dir 目录
#     compare_dir = os.path.join(os.path.dirname(root_dir), f"compare_{sort_standard}")
#     os.makedirs(compare_dir, exist_ok=True)
#
#     # 遍历二级文件夹
#     for subdir, _, files in os.walk(root_dir):
#         for file in files:
#             if file.endswith('.xlsx'):
#                 file_path = os.path.join(subdir, file)
#                 file_name = os.path.basename(file_path)
#                 # 解析文件名
#                 pattern = re.compile(r'([TB]\d(?:\.\d)?)-(\d+)-(\d+)(\d+)-(\d+)(\d+)(?:\(.*\))?')
#                 match = pattern.match(file_name)
#                 if not match:
#                     continue
#
#                 # 提取文件名各部分
#                 layer_spacing = match.group(1)  # 走线类型和导线间距
#                 number = match.group(2)         # 序号
#                 experiment_num = match.group(3)  # 实验次数
#                 experiment_group = match.group(4)  # 实验组别
#                 fluence = match.group(5)        # 辐照注量
#                 bias = match.group(6)           # 偏压
#
#                 # 根据分类标准生成占位符
#                 if sort_standard:
#                     if sort_standard == 'P':  # 按走线类型分类
#                         group_key = f"{placeholder_map['P']}-{number}-{experiment_num}{experiment_group}-{fluence}{bias}"
#                     elif sort_standard == 'd':  # 按导线间距分类
#                         group_key = f"{layer_spacing[0]}{placeholder_map['d']}-{number}-{experiment_num}{experiment_group}-{fluence}{bias}"
#                     elif sort_standard == 'n':  # 按序号分类
#                         group_key = f"{layer_spacing}-{placeholder_map['n']}-{experiment_num}{experiment_group}-{fluence}{bias}"
#                     elif sort_standard == 't':  # 按实验次数分类
#                         group_key = f"{layer_spacing}-{number}-{placeholder_map['t']}{experiment_group}-{fluence}{bias}"
#                     elif sort_standard == 'g':  # 按实验组别分类
#                         group_key = f"{layer_spacing}-{number}-{experiment_num}{placeholder_map['g']}-{fluence}{bias}"
#                     elif sort_standard == 'e':  # 按辐照注量分类
#                         group_key = f"{layer_spacing}-{number}-{experiment_num}{experiment_group}-{placeholder_map['e']}{bias}"
#                     elif sort_standard == 'v':  # 按偏压分类
#                         group_key = f"{layer_spacing}-{number}-{experiment_num}{experiment_group}-{fluence}{placeholder_map['v']}"
#                     else:
#                         print(f"Invalid sort_standard: {sort_standard}")
#                         return
#                 else:
#                     # 如果 sort_standard 为 None，且 sort_all 为 True，则全分类
#                     group_key = f"{layer_spacing}-{number}-{experiment_num}{experiment_group}-{fluence}{bias}"
#
#                 # 创建分类文件夹并移动文件
#                 group_dir = os.path.join(compare_dir, group_key)
#                 os.makedirs(group_dir, exist_ok=True)
#                 shutil.move(file_path, os.path.join(group_dir, file_name))
#
#     # 清理空文件夹
#     for subdir, _, _ in os.walk(compare_dir):
#         if not os.listdir(subdir):
#             os.rmdir(subdir)
#
# # 分类文件
# root_dir = './datas_learn/sort_test/temp'
# sort_variable(root_dir, sort_standard='d')

"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""
"""
分类文件使用例
"""

# 分类文件
# root_dir = './datas_learn/sort_test/test_2/all_data'

# pjc.sort_variable(root_dir, sort_standard='P')
# pjc.sort_variable(root_dir, sort_standard='d', ignore_list=['n', 'g'], move_single=True, draw_plot=True, use_log=True)
# pjc.sort_variable(root_dir, sort_standard='n')

# pjc.sort_variable(root_dir, sort_standard='t')
# pjc.sort_variable(root_dir, sort_standard='g')
# pjc.sort_variable(root_dir, sort_standard='e')
# pjc.sort_variable(root_dir, sort_standard='v')

# pjc.sort_variable(root_dir, sort_standard=None, sort_all=True, ignore_list=['n', 'g'], move_single=True, draw_plot=True, use_log=True)


"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""
"""
单点(电压)相关性分析尝试(失败)
"""

# import os
# import pandas as pd
# import numpy as np
# from scipy.stats import pearsonr
# import matplotlib.pyplot as plt
# import re
# import shutil
#
#
# def analyze_voltage_correlation(file_path, analysis_var='t', voltage_step=2, tolerance=1):
#     """基于sort_variable解析逻辑的电压点级相关性分析"""
#     # 实验参数映射表
#     annealing_time_table = {
#         '0': {'group1': None, 'group2': None},
#         '1': {'group1': None, 'group2': None},
#         '2': {'group1': 0, 'group2': None},
#         '3': {'group1': 7, 'group2': None},
#         '4': {'group1': 14, 'group2': None},
#         '5': {'group1': 21, 'group2': None},
#         '6': {'group1': 28, 'group2': None},
#         '7': {'group1': None, 'group2': 0},
#         '8': {'group1': 72, 'group2': 16},
#         '9': {'group1': 79, 'group2': 23},
#         'A': {'group1': 105, 'group2': 49},
#         'B': {'group1': 112, 'group2': 56},
#         'C': {'group1': 119, 'group2': 63},
#     }
#
#     # 生成电压序列 (0-1000V)
#     target_voltages = np.arange(0, 1001, voltage_step)
#     correlation_data = {v: {'x': [], 'y': []} for v in target_voltages}
#
#     # 遍历文件夹 ----------------------------------------------------------------
#     for folder_name in os.listdir(file_path):
#         folder_dir = os.path.join(file_path, folder_name)
#         if not os.path.isdir(folder_dir):
#             continue
#
#         # 遍历文件
#         for file in os.listdir(folder_dir):
#             if not file.endswith('.xlsx'):
#                 continue
#
#             # 严格使用sort_variable的解析逻辑
#             match = re.match(
#                 r'^([TB]\d(?:\.\d)?)-(\d+)-(\d+)(\d+)-(\d+)(\d+)(?:\(.*\))?\.xlsx$',
#                 file
#             )
#             if not match:
#                 print(f"警告：文件 {file} 不符合命名规范（已跳过）")
#                 continue
#
#             # 提取参数（与sort_variable完全一致）
#             layer_spacing = match.group(1)  # 走线类型和间距（如B0）
#             number = match.group(2)  # 序号
#             experiment_num = match.group(3)  # 实验次数（如21）
#             experiment_group = match.group(4)  # 组别
#             fluence = match.group(5)  # 辐照注量
#             bias = match.group(6)  # 偏压
#
#             # 计算分析变量（以退火时间为例）
#             t_code = experiment_num[0]  # 实验次数代码
#             e_code = fluence[0]  # 辐照注量代码
#             group = 'group2' if e_code == '4' else 'group1'
#             var_value = annealing_time_table.get(t_code, {}).get(group, None)
#             if var_value is None:
#                 continue
#
#             # 读取数据
#             try:
#                 df = pd.read_excel(os.path.join(folder_dir, file))
#                 voltage_col = df.columns[0]
#                 current_col = df.columns[1]
#
#                 # 数据清洗
#                 df[voltage_col] = pd.to_numeric(df[voltage_col], errors='coerce')
#                 df.dropna(subset=[voltage_col, current_col], inplace=True)
#                 if df.empty:
#                     continue
#             except Exception as e:
#                 print(f"文件 {file} 读取失败: {str(e)}")
#                 continue
#
#             # 分配数据到电压点
#             for target_v in target_voltages:
#                 lower = target_v - tolerance
#                 upper = target_v + tolerance
#                 valid_data = df[(df[voltage_col] >= lower) & (df[voltage_col] <= upper)]
#                 if not valid_data.empty:
#                     closest_idx = (valid_data[voltage_col] - target_v).abs().idxmin()
#                     correlation_data[target_v]['x'].append(var_value)
#                     correlation_data[target_v]['y'].append(valid_data.loc[closest_idx, current_col])
#
#     # 结果分析与可视化 ----------------------------------------------------------
#     img_dir = os.path.join(file_path, '0multiple_img')
#     os.makedirs(img_dir, exist_ok=True)
#
#     # 计算相关系数
#     voltages = []
#     correlations = []
#     for v in target_voltages:
#         data = correlation_data[v]
#         if len(data['x']) >= 2:
#             try:
#                 corr = pearsonr(data['x'], data['y'])[0]
#                 voltages.append(v)
#                 correlations.append(corr)
#             except:
#                 print(f"电压 {v}V 数据无效")
#                 continue
#
#     # 生成图表（使用原文件夹名称）
#     if len(voltages) > 0:
#         plt.figure(figsize=(12, 6))
#         plt.plot(voltages, correlations, 'b-', linewidth=1.5)
#         plt.xlabel('Voltage (V)', fontsize=12)
#         plt.ylabel('Pearson Correlation Coefficient', fontsize=12)
#         plt.title(f'Voltage-Correlation Relationship ({analysis_var.upper()})', fontsize=14)
#         plt.grid(True, linestyle='--', alpha=0.7)
#
#         # 使用原文件夹名称保存
#         img_name = f"{os.path.basename(file_path)}_correlation.png"
#         plt.savefig(os.path.join(img_dir, img_name), dpi=300)
#         plt.close()
#         print(f"分析完成，图表已保存至: {img_name}")
#     else:
#         print("无有效数据可生成图表")
#
#
# if __name__ == "__main__":
#     analyze_voltage_correlation(
#         file_path='./datas_analyze/compare_t(45_45)',
#         voltage_step=2,
#         tolerance=1
#     )

"""----------------------------------------请在本分割线下放置需测试的代码--------------------------------------------------"""
"""
7-23数据分析
"""
# base_folder = 'E:\\拓展项目\\大创\\大创实验数据\\7-23_验证实验\\compare_t_old\\add'
# pjc.plot_multiple_folders(base_folder, use_log=False)
#
# base_folder = 'E:\\拓展项目\\大创\\大创实验数据\\7-23_验证实验\\compare_t_old\\origin'
# pjc.plot_multiple_folders(base_folder, use_log=False)

# base_folder = 'E:\\拓展项目\\大创\\大创实验数据\\7-23_验证实验\\正反通电\\一正一反'
# pjc.plot_multiple_folders(base_folder, use_log=False)

# base_folder = 'E:\\拓展项目\\大创\\大创实验数据\\7-23_验证实验\\正反通电\\多正多反'
# pjc.plot_multiple_folders(base_folder, use_log=False)

# base_folder = 'E:\\拓展项目\\大创\\大创实验数据\\7-23_验证实验\\compare_t_new'
# pjc.plot_multiple_folders(base_folder, use_log=False)


# pjc.plot_multiple_files_windowed(colors=None, labels=None, line_styles=None, line_widths=None, use_log=False)
