
import os

# 获取当前脚本（learn1.py）所在的文件夹路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接secret.daz的绝对路径（因为secret.daz和learn1.py在同一个task1文件夹里）
file_path = os.path.join(script_dir, 'secret.daz')

# 用构造好的绝对路径打开文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
# 读取secret.daz文件
# with代码块执行结束后（无论正常结束还是报错），会自动关闭文件
# 参数(变量）都是字符串数据类型,utf-8
# as f 起个别名 类似 import numpy as np
# encoding 本身open自己内置了这个变量，没必要再定义一次
"""
文本模式下，读取文件中从当前指针位置到文件末尾的全部内容
（默认指针在文件开头，所以读取全部文本），返回字符串类型。
不默认位置的方法
.seek(目标位置的字节数, 0) = 直接把书签插到 “文件第 N 字节” 的位置
文件里的换行（回车）会被视为 1 个普通字符
"""
# 以'X'分割内容，并过滤掉空字符串
#原AI写法： 
'''
hex_list = [item(输出) for item(搬运输出) in content.split('X') if item]
[ 最终要添加到列表的元素  for 变量名 in 要遍历的序列  if 过滤条件 ]

'''
hex_list = []
# 先按 'X' 分割 ，得到包含空字符串的临时列表
split_result = content.split('X')
# 遍历元素
for item in split_result:
    if item:
        hex_list.append(item)#把你分割出来的东西，加入列表里面

# 将16进制数字转换为Unicode字符
decoded_chars = [] # 变量名定义成这样......
for hex_str in hex_list:
    try:
        # 将16进制字符串转换为整数，再转换为对应的Unicode字符
        char_code = int(hex_str, 16)
        decoded_chars.append(chr(char_code))
    except ValueError:
        continue

# 组合成明文S
S = ''.join(decoded_chars)


# 计算可见字符数（除去空格、制表符、换行符）
visible_chars = [c for c in S if c not in [' ', '\t', '\n']]#再出来来个列表
visible_count = len(visible_chars)#之后去看列表的长度

student_id = "2025090912004"  # 请修改为您的实际学号

S1 = f"<解密人>{student_id}<情报总字数>{visible_count}"

# 拼接interpretation.txt的完整路径（生成在task1里）
interpretation_path = os.path.join(script_dir, 'interpretation.txt')

# 写入文件
with open(interpretation_path, 'w', encoding='utf-8') as f:
    f.write(S)
    f.write('\n')
    f.write(S1)
print(f"解密内容长度: {len(S)}")
print(f"可见字符数: {visible_count}")
print(f"签名: {S1}")