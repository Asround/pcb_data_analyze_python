# plot_multiple_folders

## 基本说明

- 仅涉及一个函数

- 需要前置库,  不需要引用 Parts.py 中的 任何函数

- 主要用于给 sort_variable 函数引用

## 代码部分

- 代码功能:
  - 传入一个 一级文件夹 路径
  - 顺序搜索二级文件夹中的 .xlsx 文件, 将全部数据画到一张图中
    - 不做拟合
- 代码内容:

```python
def plot_multiple_folders(base_folder):
    '''
    base_folder: 一级文件夹
    一级文件夹下有许多装有 xlsx表格的二级文件夹,
    函数会依次读取二级文件夹的文件夹路径, 并以之为参数传给 pt.plot_multiple_files_no_display函数画图
    画图后将图片统一存储到一级文件夹目录下的"multiple_img"文件夹中
    图片的名字是对应二级文件夹的名字
    '''
    # 创建img文件夹路径
    img_folder = os.path.join(base_folder, 'multiple_img')
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # 用于保存二级文件夹路径和名称的字典
    folder_info = {'paths': [], 'names': []}

    # 遍历一级文件夹下的所有二级文件夹
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path) and folder_name != 'multiple_img':  # 排除img文件夹
            folder_info['paths'].append(folder_path)
            folder_info['names'].append(folder_name)

    # 顺序处理每个二级文件夹
    for folder_path, folder_name in zip(folder_info['paths'], folder_info['names']):
        # 调用plot_multiple_files函数处理文件夹中的Excel文件
        pt.plot_multiple_files_no_display(folder_path)

        # 保存图像到multiple_img文件夹
        image_path = os.path.join(img_folder, f'{folder_name}.png')
        plt.savefig(image_path, dpi=225)  # 保存当前图像
        print(f'{folder_name}.png 保存成功!') # 提示保存成功
        plt.close()  # 关闭当前图像，避免内存泄漏
```
