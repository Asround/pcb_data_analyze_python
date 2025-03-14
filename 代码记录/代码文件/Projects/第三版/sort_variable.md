# sort_variable


## 基本说明

- 仅一个函数 (如无必要不添加windowed版本)
- 需要前置库 (查看"所需库.md"文件)
- 需引用 Part.py 中的函数 (具体不列举)

## 代码部分

- 参数说明(更加具体的内容请看代码, 以及b站配套视频)

| 参数          | 参数说明                 |
| ------------- | ------------------------ |
| root_dir      | 一级文件夹路径           |
| sort_standard | 分类标准(变量)           |
| sort_all      | 按照顺序将所有变量都分类 |
| ignore_list   | 分类时忽略的变量列表     |
| move_single   | 是否处理单文件文件夹     |
| draw_plot     | 是否调用函数批量画图     |

- 功能:

  - 对所有数据按照指定规则分类处理, 并可调用其他函数进行批量画图 (程序自动保存图像)

- 代码内容:

  ```python
  def sort_variable(root_dir, sort_standard=None, sort_all=False, ignore_list=['n', 'g'], move_single=True, draw_plot=False):
      '''
      :param root_dir: 存放数据文件的一级文件夹, 其下的二级文件夹直接存放.xlsx文件
      :param sort_standard: 控制变量法中分析的变量, 't' 即以 t(实验次数) 为标准进行文件分类
      :param sort_all: 当sort_standard = None, sort_all = True 时, 直接对所有变量遍历分类
      :param ignore_list: 分类时忽略的变量, 一般默认忽略序号和组别, 因为它们不影响板子的物理性质
      :param move_single: 是否处理仅含单.xlsx文件的文件夹, 默认处理. 具体参看 Parts.py 中的 move_single_file_folders 函数
      :param draw_plot: 是否调用plot_multiple_files进行画图, 默认False(因为运行时间太长)
      '''
      if not sort_standard and not sort_all:
          print("No sort standard provided. Function will not execute.")
          return
  
      # 如果 sort_all 为 True，则遍历所有分类标准(此处忽略 n 与 g ,对其分类没有太大意义)
      if sort_all:
          for standard in ['P', 'd', 't', 'e', 'v']:
              sort_variable(root_dir, sort_standard=standard, sort_all=False, ignore_list=ignore_list, move_single=move_single, draw_plot=draw_plot)
          return
  
      # 检查 ignore_list 是否合法
      if ignore_list:
          valid_keys = {'P', 'd', 'n', 't', 'g', 'e', 'v'}
          if not set(ignore_list).issubset(valid_keys):
              print(f"Invalid ignore_list: {ignore_list}. It should only contain 'P', 'd', 'n', 't', 'g', 'e', 'v'.")
              return
  
      # 定义占位符规则
      placeholder_map = {
          'P': 'P',  # 走线类型
          'd': 'd',  # 导线间距
          'n': 'n',  # 序号
          't': 't',  # 实验次数
          'g': 'g',  # 实验组别
          'e': 'e',  # 辐照注量
          'v': 'v'   # 偏压
      }
  
      # 创建 compare_dir 目录
      compare_dir = os.path.join(os.path.dirname(root_dir), f"compare_{sort_standard}")
      os.makedirs(compare_dir, exist_ok=True)
  
      # 用于记录每个 group_key 的文件数量
      group_count = {}
  
      # 遍历二级文件夹
      for subdir, _, files in os.walk(root_dir):
          for file in files:
              if file.endswith('.xlsx'):
                  file_path = os.path.join(subdir, file)
                  file_name = os.path.basename(file_path)
                  # 解析文件名
                  pattern = re.compile(r'([TB]\d(?:\.\d)?)-(\d+)-(\d+)(\d+)-(\d+)(\d+)(?:\(.*\))?')
                  match = pattern.match(file_name)
                  if not match:
                      continue
  
                  # 提取文件名各部分
                  layer_spacing = match.group(1)  # 走线类型和导线间距
                  number = match.group(2)         # 序号
                  experiment_num = match.group(3)  # 实验次数
                  experiment_group = match.group(4)  # 实验组别
                  fluence = match.group(5)        # 辐照注量
                  bias = match.group(6)           # 偏压
  
                  # 根据分类标准和 ignore_list 生成 group_key
                  if sort_standard:
                      # 走线类型和导线间距
                      if sort_standard == 'P':
                          # 当 sort_standard 为 'P' 时，导线间距部分用占位符 'd' 表示
                          p_part = placeholder_map['P']
                          d_part = layer_spacing[1:] if 'd' not in ignore_list else placeholder_map['d']
                          pd_part = f"{p_part}{d_part}"
                      elif sort_standard == 'd':
                          # 当 sort_standard 为 'd' 时，走线类型部分用占位符 'P' 表示
                          p_part = layer_spacing[0] if 'P' not in ignore_list else placeholder_map['P']
                          d_part = placeholder_map['d']
                          pd_part = f"{p_part}{d_part}"
                      else:
                          p_part = layer_spacing[0] if 'P' not in ignore_list else placeholder_map['P']
                          d_part = layer_spacing[1:] if 'd' not in ignore_list else placeholder_map['d']
                          pd_part = f"{p_part}{d_part}"
  
                      # 序号
                      if sort_standard == 'n':
                          n_part = placeholder_map['n']
                      else:
                          n_part = number if 'n' not in ignore_list else placeholder_map['n']
  
                      # 实验次数和实验组别
                      if sort_standard == 't':
                          # 当 sort_standard 为 't' 时，实验组别部分用占位符 'g' 表示
                          t_part = placeholder_map['t']
                          g_part = experiment_group if 'g' not in ignore_list else placeholder_map['g']
                          tg_part = f"{t_part}{g_part}"
                      elif sort_standard == 'g':
                          tg_part = placeholder_map['g']
                      else:
                          t_part = experiment_num if 't' not in ignore_list else placeholder_map['t']
                          g_part = experiment_group if 'g' not in ignore_list else placeholder_map['g']
                          tg_part = f"{t_part}{g_part}"
  
                      # 辐照注量和偏压
                      if sort_standard == 'e':
                          # 当 sort_standard 为 'e' 时，偏压部分用占位符 'v' 表示
                          e_part = placeholder_map['e']
                          v_part = bias if 'v' not in ignore_list else placeholder_map['v']
                          ev_part = f"{e_part}{v_part}"
                      elif sort_standard == 'v':
                          # 当 sort_standard 为 'v' 时，辐照注量部分用占位符 'e' 表示
                          e_part = fluence if 'e' not in ignore_list else placeholder_map['e']
                          v_part = placeholder_map['v']
                          ev_part = f"{e_part}{v_part}"
                      else:
                          e_part = fluence if 'e' not in ignore_list else placeholder_map['e']
                          v_part = bias if 'v' not in ignore_list else placeholder_map['v']
                          ev_part = f"{e_part}{v_part}"
  
                      # 组合成 group_key
                      group_key = f"{pd_part}-{n_part}-{tg_part}-{ev_part}"
                  else:
                      # 如果 sort_standard 为 None，且 sort_all 为 True，则直接返回(因为前面已经处理了这种情况)
                      return
  
                  # 更新文件数量
                  if group_key not in group_count:
                      group_count[group_key] = 0
                  group_count[group_key] += 1
  
                  # 创建分类文件夹并复制文件
                  group_dir = os.path.join(compare_dir, group_key)
                  os.makedirs(group_dir, exist_ok=True)
                  shutil.copy(file_path, os.path.join(group_dir, file_name))
  
      # 遍历 compare_dir，重命名文件夹并添加 (count)
      for group_key, count in group_count.items():
          old_dir = os.path.join(compare_dir, group_key)
          new_dir = os.path.join(compare_dir, f"{group_key}({count})")
          # 如果目标文件夹已存在，则先删除它
          if os.path.exists(new_dir):
              shutil.rmtree(new_dir)
          os.rename(old_dir, new_dir)
  
      # 在 compare_dir 名称后加上二级文件夹的数量
      num_subdirs_before = len([name for name in os.listdir(compare_dir) if os.path.isdir(os.path.join(compare_dir, name))])
      new_compare_dir = os.path.join(os.path.dirname(root_dir), f"compare_{sort_standard}({num_subdirs_before})")
  
      # 如果目标文件夹已存在，则先删除它
      if os.path.exists(new_compare_dir):
          shutil.rmtree(new_compare_dir)
      os.rename(compare_dir, new_compare_dir)
  
      # 处理只含单个.xlsx文件的文件夹
      if move_single:
          pt.move_single_file_folders(new_compare_dir)
  
      # 更新 compare_dir 名称，添加处理后的文件夹数量
      num_subdirs_after = len([name for name in os.listdir(new_compare_dir) if os.path.isdir(os.path.join(new_compare_dir, name))])
      final_compare_dir = os.path.join(os.path.dirname(root_dir), f"compare_{sort_standard}({num_subdirs_before}_{num_subdirs_after})")
      os.rename(new_compare_dir, final_compare_dir)
  
      # 清理空文件夹
      for subdir, _, _ in os.walk(final_compare_dir):
          if not os.listdir(subdir):
              os.rmdir(subdir)
  
      # 如果 draw_plot 为 True，则调用 plot_multiple_folders 函数
      if draw_plot:
          pjc.plot_multiple_folders(final_compare_dir)
  
  
  # # 示例调用
  # root_dir = './datas_learn/sort_test/test_2/all_data'
  # sort_standard = 't'
  # ignore_list = ['n', 'g']
  #
  # # 直接全部运行就是全都分类一次
  # sort_variable(root_dir, sort_standard='P', sort_all=False, ignore_list=ignore_list, move_single=True)
  # sort_variable(root_dir, sort_standard='d', sort_all=False, ignore_list=ignore_list, move_single=True)
  # sort_variable(root_dir, sort_standard='t', sort_all=False, ignore_list=ignore_list, move_single=True)
  # sort_variable(root_dir, sort_standard='e', sort_all=False, ignore_list=ignore_list, move_single=True)
  # sort_variable(root_dir, sort_standard='v', sort_all=False, ignore_list=ignore_list, move_single=True)
  #
  # # 一条代码实现全部分类
  # sort_variable(root_dir, sort_standard=None, sort_all=True, ignore_list=['n', 'g'], move_single=True)
  ```

  
