# read_VA(df)

## 代码内容

```python
def read_VA(df):
    B2 = df.iloc[0, 1]  # '.iloc[0,1]': 取表格索引为[0,1]单元格(即B2)的内容
    if 'V' in B2:  # 满足该条件, 即 "1.型表格"
        B2 = False
    else:  # 即"2/3.型表格"
        B2 = int(df.iloc[0, 1])  # 将 B2 强制转换为int类型, 作用和 B2 = True 相同

    # if 判断实现不同文件分类读取
    if B2:
        # "2/3.型表格"是非零数字(真), 满足 if 条件 则读取 C36 到 D536 的数据
        df_filtered = df.iloc[34:34 + B2 - 1, [2, 3]].dropna()
        # [34: 34 + B2 - 1,[2,3]]对应 C36 到 D536
        # 34 对应 36 是因为自动丢弃第一行, 并且从 0 开始索引
        # 2 对应 C 是因为 0 是开始索引, 对应 A
        # [34 + B2 - 1, 3] 即 D(B2+33)单元格, 数学上易知是最后一个电流对应单元格
        # # 这样规定的原因是, "2.型表格" 的电压电流数据后有统计量, 不希望它们被读入

    else:
        # "1.型表格" 是False(假), ，则读取 B3 到 C503 的数据
        df_filtered = df.iloc[1:501, [1, 2]].dropna()
        # [2,501]对应 C503, 相当于我们默认读取 501 组数据
        # 因为"1.型表格" 的电压电流数据后面是空值, 会被 .dropna(丢弃), 不怕多读.

    # 重新命名列名 (左边是电压, 右边是电流)
    df_filtered.columns = ["电压 (V)", "电流 (A)"]

    # 转换数据为数值类型（防止字符串干扰）,方便绘图和后续曲线拟合
    df_filtered = df_filtered.astype(float)

    # 提取自变量（电压）和因变量（电流）
    x = df_filtered["电压 (V)"]
    y = df_filtered["电流 (A)"]

    return x,y
```

## 代码调用

- 前置:

  ```python
  import Parts as pt
  ```

  

- 调用:

  - 一般在如下代码后面:

    ```python
    # 读取 Excel 文件
        xls = pd.ExcelFile(file_path)
        df = xls.parse(sheet_name=0)
    ```

  - 直接接如下代码即可:

    ```python
    # 提取电压电流数据
        x, y = pt.read_VA(df)
    ```

  - x 存储电压数据, y 存储电流数据
