# 项目内容说明

## 功能说明

1. 主要为分析 .xlsx 表格格式中的数据.
2. 包括但不限于: 利用数据画图, 利用数据进行曲线拟合, 对多表格批量画图, 对多表格批量分类

## 使用注意

本项目内容服务于个人所在团队大创项目的数据分析, 并不服务于一般表格的数据读取和处理, 所以大概率是无法处理一般的的表格文件的. 若有需要, 请自行修改代码的读取规则, 已满足自我需求.

项目文件中, 每个函数都给出了示例调用在函数后(被注释). 一般其使用的 .xlsx 表格在 datas_learn 文件夹中. 但考虑到数据保密的问题, 并未给出完整的表格数据, 所以某些调用可能因为无法访问到指定路径而报错.

## 使用说明

1. 本项目主要文件为 Projects.py 和 Parts.py
   - 前者主要存放各类函数
   - 后者主要存放各类功能单体
2. 调用和运行代码时, 建议使用仓库内的 test.py 文件, 前置已经添加好
3. temp.py 请忽略, 其为写代码阶段临时存储所用.
4. 其他各类文件夹自行阅读即可, 内容不难理解.
