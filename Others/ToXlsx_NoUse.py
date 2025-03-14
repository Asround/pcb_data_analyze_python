"""
此代码用于转换一般的 csv文件, 这种文件要求所有表头都在A行
然而我们的数据并不满足这个条件, 所以数据会有丢失
当做一个没用的 附加产物 即可
"""

import os
import pandas as pd
import easygui as eg


# xls文件转xlsx
def xls_save_as_xlsx(file_name):
    df = pd.read_excel(file_name)  # pandas读xls文件
    file, name = os.path.splitext(file_name)  # 分解扩展名
    df.to_excel(f"{file}.xlsx", index=False)  # pandas写入xlsx
    print(f'{file_name} 转换成功啦！O(∩_∩)O哈哈~')
    print('-----------------------------------------------------------------------------------------------------------')
    os.remove(file_name)  # 删除原xls文件


# csv文件转xlsx
def csv_save_as_xlsx(file_name):
    try:
        df = pd.read_csv(file_name, sep=',', on_bad_lines='skip')  # 读取CSV文件，跳过有问题的行
        file, name = os.path.splitext(file_name)  # 分解扩展名
        df.to_excel(f"{file}.xlsx", index=False)  # 写入Excel文件
        print(f'{file_name} 转换成功啦！O(∩_∩)O哈哈~')
        print('-----------------------------------------------------------------------------------------------------------')
        os.remove(file_name)  # 删除原CSV文件
    except Exception as e:
        print(f'转换失败: {file_name}, 错误信息: {e}')
# def csv_save_as_xlsx(file_name):
#     df = pd.read_csv(file_name)  # pandas读xls文件
#     file, name = os.path.splitext(file_name)  # 分解扩展名
#     df.to_excel(f"{file}.xlsx", index=False)
#     print(f'{file_name} 转换成功啦！O(∩_∩)O哈哈~')
#     print('-----------------------------------------------------------------------------------------------------------')
#     os.remove(file_name)  # 删除原csv文件


# 打开窗口，选择一个文件夹
def pick_package():
    return eg.diropenbox()


if __name__ == "__main__":
    print('欢迎来到文件转换系统,程序正在启动...')
    print('请选择要转换的文件夹')
    data_path = pick_package()
    for dirpath, dirname, filenames in os.walk(data_path):  # os.walk()遍历文件
        for fname in filenames:
            file_name = os.path.join(dirpath, fname)  # os.path.join()合并路径
            if file_name.endswith('.xls'):
                xls_save_as_xlsx(file_name)
            elif file_name.endswith('.csv'):
                csv_save_as_xlsx(file_name)
            else:
                print(f'跳过非xls文件:{file_name}')
    input('输入任意键退出')
    print('finished...')