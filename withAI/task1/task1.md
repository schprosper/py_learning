  

# 学习流程

我先学习了吴恩达的ml方向的course1，了解基本概念然后看了看相关代码，花了两天时间。  

回来发现这个题好像和机器学习没什么关系.......  

于是：

1. 直接复制题目要求给ai，让ai生成答案，并且调试保证答案可以正常运行。

2. 之后，开始学习里面每一个库函数，并且进行了笔记记录

3. 学习完库函数，然后开始理解ai生成的代码的逻辑

4. 之后，自己抄一边代码，回顾逻辑，交上题目。

  
# 以下是学习过程中的代码
```python

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
```


# open()

```

open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)  

```

| 参数名         | 类型         | 是否必选 | 核心作用                                                                   |
| ----------- | ---------- | ---- | ---------------------------------------------------------------------- |
| `file`      | 字符串 / 路径   | 是    | 要打开的文件路径（相对路径或绝对路径）。<br><br>例：`"test.txt"`（相对）、`"C:/data/log.txt"`（绝对） |
| `mode`      | 字符串        | 否    | 打开文件的模式（读写模式 + 文本 / 二进制模式），默认值为 `'r'`（只读文本模式）。                         |
| `encoding`  | 字符串        | 否    | 文本模式（不加 `'b'`）下的编码格式（如 `utf-8`、`gbk`），二进制模式下无需指定。                      |
| `errors`    | 字符串        | 否    | 编码错误的处理方式（如 `'ignore'` 忽略、`'replace'` 替换），默认报错。                        |
| `buffering` | 整数         | 否    | 缓冲区大小（-1 表示默认缓冲，0 表示无缓冲，1 表示行缓冲，>1 表示指定字节数），一般无需手动设置。                  |
| `newline`   | 字符串 / None | 否    | 文本模式下的换行符处理（如 `'\n'`、`'\r\n'`），默认 `None` 自动适配系统。                       |
| 其他参数        | -          | 否    | `closefd`、`opener` 等为高级参数，日常开发极少用到，默认值即可满足需求。                          |
#### 三、最常用的 `mode` 模式（核心重点）

`mode` 由「读写权限」+「文件类型」组成，常见组合如下：

| 模式     | 类型  | 核心功能                                     |
| ------ | --- | ---------------------------------------- |
| `'r'`  | 文本  | 只读（默认），文件必须存在，否则报错。                      |
| `'w'`  | 文本  | 只写，文件不存在则创建，存在则清空原有内容（覆盖）。               |
| `'a'`  | 文本  | 追加，文件不存在则创建，存在则在末尾添加内容（不覆盖）。             |
| `'r+'` | 文本  | 读写，文件必须存在，写入时从指针位置覆盖（不清空全部）。             |
| `'w+'` | 文本  | 读写，文件不存在则创建，存在则清空（覆盖 + 读权限）。             |
| `'a+'` | 文本  | 读写，文件不存在则创建，写入时追加，读取前需移动指针（`f.seek(0)`）。 |
| `'rb'` | 二进制 | 二进制只读（如图片、音频、压缩包）。                       |
| `'wb'` | 二进制 | 二进制只写（生成 / 保存二进制文件）。                     |
| `'ab'` | 二进制 | 二进制追加（给二进制文件添加内容）。                       |
|        |     |                                          |
文本模式下，读取文件中从当前指针位置到文件末尾的全部内容

（默认指针在文件开头，所以读取全部文本），返回字符串类型。

不默认位置的方法

.seek(目标位置的字节数, 0) = 直接把书签插到 “文件第 N 字节” 的位置

文件里的换行（回车）会被视为 1 个普通字符
# 列表....
列表方法
![[Pasted image 20251108110938.png]]
# 字符串
 **.join(...)`：字符串的 “拼接方法”
- 作用：Python 中字符串（str）自带的方法，专门用来「把一个 “可迭代对象”（最常用是列表）里的所有元素，按 “胶水” 规则拼接成一个新字符串」。
- 注意：`join` 是「字符串的方法」，必须用字符串（比如 `''`、`','`）调用，不能用列表调用（比如 `decoded_chars.join('')` 会报错！）。
- S = ''.join(decoded_chars)  '这里面'是拼接起来的时候，中间用什么隔开
#### 天生false
Python 里，有些值天生是「假值」（判断时等于 `False`），有些是「真值」（判断时等于 `True`），不用写复杂条件，直接用 `if 变量` 就能判断：

| 假值（`if 变量` 结果为 `False`） | 真值（`if 变量` 结果为 `True`）   |
| ----------------------- | ------------------------ |
| 空字符串 `''`               | 非空字符串（如 'a'、'123'、'x\n'） |
| 数字 0、空列表 `[]`、`None`    | 非 0 数字、非空列表等             |
# 内置类型转换函数（类似c）
## int字符串 / 其他类型 ↔ 数字
```python

int(待转换的字符串, 你想让字符串转成什么整数)
```

```python

自动转成整数
# 1. 字符串转十进制整数（默认基数 10）
num1 = int("123")  # 把字符串"123"转成整数 123
print(num1)  # 输出：123，类型是 int

# 2. 浮点数转整数（直接舍弃小数部分，不是四舍五入）
num2 = int(3.99)  # 把 3.99 转成整数 3
print(num2)  # 输出：3

# 3. 空字符串/非数字字符串会报错
num3 = int("abc")  # 报错：ValueError（"abc"不能转成整数）
```

`char_code = int(hex_str, 16)` 这个特定场景中，它的功能是 **把十六进制字符串 `hex_str` 转换成对应的十进制整数**

## float转换为浮点数
```python
# 2. 字符串转浮点数（支持整数、小数、科学计数法）
print(float("3.14")) # 输出：3.14
print(float("100"))  # 输出：100.0（字符串"100"→浮点数100.0）
print(float("1.2e3"))# 输出：1200.0（科学计数法"1.2e3"→1200.0）

# 3. 布尔值转浮点数（True=1.0，False=0.0）
print(float(True))   # 输出：1.0
print(float(False))  # 输出：0.0

# 4. 特殊值转换（NaN、无穷大）
print(float("nan"))  # 输出：nan（非数字）
print(float("inf"))  # 输出：inf（正无穷大）
```
### 4. `str(object)`：转换为字符串

```python
# 3. 序列/集合转字符串
print(str([1,2,3]))   # 输出："[1, 2, 3]"（列表→字符串）
print(str((1,2,3)))   # 输出："(1, 2, 3)"（元组→字符串）
print(str({1,2,3}))   # 输出："{1, 2, 3}"（集合→字符串）

# 4. 字典转字符串
print(str({"name":"Tom", "age":18}))  # 输出："{'name': 'Tom', 'age': 18}"

# 5. 自定义对象转字符串（默认输出对象信息，可通过 __str__ 方法自定义）
class Person:
    def __init__(self, name):
        self.name = name
print(str(Person("Alice")))  # 输出："<__main__.Person object at 0x000002...>"
```
### 6. `list(iterable)`：转换为列表

#### 功能说明：

将可迭代对象（元组、集合、字符串、字典、range 等）转换为列表（可变序列）。

#### 语法格式：

`list(可迭代对象)`（可迭代对象：能通过 `for` 循环遍历的对象）
### 12. `chr(i)`：整数 → Unicode 字符
```python
print(chr(65))        # 输出：'A'（ASCII 码 65）
```
### 13. `ord(c)`：Unicode 字符 → 整数
```python
print(ord('A'))       # 输出：65（'A' 的 ASCII 码）
print(ord('你'))      # 输出：20320（'你' 的 Unicode 编码）
```
### 14. `hex(x)`：十进制整数 → 十六进制字符串
### 15. `oct(x)`：十进制整数 → 八进制字符串

|需求场景|推荐函数|示例|
|---|---|---|
|字符串转整数|`int(x)`|`int("123") → 123`|
|字符串转浮点数|`float(x)`|`float("3.14") → 3.14`|
|数字转字符串|`str(x)`|`str(123) → "123"`|
|列表 / 元组 / 集合互转|`list(x)`/`tuple(x)`/`set(x)`|`list((1,2)) → [1,2]`|
|字符串转字节|`bytes(x, encoding)`|`bytes("你好", "utf-8")`|
|字节转字符串|`x.decode(encoding)`|`b'\xe4\xbd\xa0'.decode("utf-8") → "你"`|
|字符与编码值互转|`chr(x)`/`ord(c)`|`chr(65) → 'A'`、`ord('A') → 65`|
|十进制转其他进制字符串|`hex(x)`/`oct(x)`/`bin(x)`|`hex(255) → '0xff'`|
|其他进制字符串转十进制|`int(x, base)`|`int("ff", 16) → 255`|

核心原则：
# OS库——文件路径处理

### 本题有关
**不管你在电脑哪个目录下运行 `learn1.py` 脚本，都能精准找到和它放在同一个文件夹（`task1`）里的 `secret.daz` 文件**

```python

script_dir = os.path.dirname(os.path.abspath(__file__))
# os.path.dirname(),回到上一级目录
file_path = os.path.join(script_dir, 'secret.daz')

```

### 1. 获取当前工作目录

`os.getcwd()` 函数用于获取当前工作目录的路径。当前工作目录是 Python 脚本执行时所在的目录。

### 实例

current_directory = os.getcwd()  
print("当前工作目录:", current_directory)  

### 2. 改变当前工作目录

`os.chdir(path)` 函数用于改变当前工作目录。`path` 是你想要切换到的目录路径。

### 实例

os.chdir("/path/to/new/directory")  
print("新的工作目录:", os.getcwd())  

### 3. 列出目录内容

`os.listdir(path)` 函数用于列出指定目录中的所有文件和子目录。如果不提供 `path` 参数，则默认列出当前工作目录的内容。

### 实例

files_and_dirs = os.listdir()  
print("目录内容:", files_and_dirs)  

### 4. 创建目录

`os.mkdir(path)` 函数用于创建一个新的目录。如果目录已经存在，会抛出 `FileExistsError` 异常。

### 实例

os.mkdir("new_directory")  

### 5. 删除目录

`os.rmdir(path)` 函数用于删除一个空目录。如果目录不为空，会抛出 `OSError` 异常。

### 实例

os.rmdir("new_directory")  

### 6. 删除文件

`os.remove(path)` 函数用于删除一个文件。如果文件不存在，会抛出 `FileNotFoundError` 异常。

### 实例

os.remove("file_to_delete.txt")  

### 7. 重命名文件或目录

`os.rename(src, dst)` 函数用于重命名文件或目录。`src` 是原始路径，`dst` 是新的路径。

### 实例

os.rename("old_name.txt", "new_name.txt")  

### 8. 获取环境变量

`os.getenv(key)` 函数用于获取指定环境变量的值。如果环境变量不存在，返回 `None`。

### 实例

home_directory = os.getenv("HOME")  
print("HOME 目录:", home_directory)  

### 9. 执行系统命令

`os.system(command)` 函数用于在操作系统的 shell 中执行命令。命令执行后，返回命令的退出状态。

### 实例

os.system("ls -l")