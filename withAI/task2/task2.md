# 题目完成思路

1. 直接复制题目要求给ai，让ai生成答案，并且调试保证答案可以正常运行。

2. 之后，开始学习里面每一个函数和语法，并且进行了笔记记录。

3. 学习完库函数，然后开始理解ai生成的代码的逻辑

4. 之后，自己抄一边代码，回顾逻辑，交上题目。

其实比前一个题，就多调用了一个datetime的库，之后就是def语法的应用（自己写函数）
# 代码逻辑
利用三个函数，分别进行：今天的日期检测、人的相关信息录入、计算之后什么时候接种


  1. 用try-expect来确排除是否有效输入！！！
  2. int类型转换，必须得是数字类型的字符串才能转换
	  `int()` 转换的关键是 ——**字符串必须能 “完整表示一个整数”**
  3. 今天的日期完全可以用datetime.now()
  4. 怎么让他输入正确才能跳出？：直接上无限循环+break

# 遇到的问题
1. 代码不能随便改......原本ai给我生成的代码逻辑严丝合缝，但是自从我想去解决：万一用户瞎输入怎么办的问题的时候：一改一个bug，要不是while true忘了退出，要不是改了之后，在内部的变量没有定义。至少改了我3个小时
2. if doses == (0,3) :
	- 这个写法错误。`doses` 是一个整数（比如 0、1、2、3），整数和元组永远不会相等
3. <font color="#c00000">我还有个疑问，我觉得我写了好多循环，这好吗？</font>


# 练习时候的代码如下

```python
from datetime import datetime,timedelta

import sys # 原本AI没给我，但我觉得得用......

#好了现在没用了，原本想着直接退出程序，现在就算了

"""

- `datetime`类：管「具体的某一刻时间」（如 “现在”“2025 年元旦”）；

- `timedelta`类：管「两个时间的差 / 时间的加减」（如 “3 天后”“1 小时前”）；

"""

# 利用

def date_now():

    """

    询问今天日期和查询人数

    当然今天的日期完全可以用这个函数实现

  

TodayYMD = datetime.now()

  

    返回：(当前日期, 查询人数)

    """

    while True:#保证他输入对了（但这么多循环，我也不知道合不合适......)

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        change_date = input(f"查询知，今天的日期是{today},要更改日期请输入y，不更改请输入n：")

        if change_date == 'y':

            while True:  # 无限循环，直到break退出

                    today_str = input("请输入今天的日期(例如:2022-09-09): ")

            #input直接是带提示的对话框。输入类型是字符串

                    try:

                        today = datetime.strptime(today_str, "%Y-%m-%d")

                        print(f"日期已更新为：{today.strftime('%Y-%m-%d')}")

                        break  # 格式正确！跳出循环，不再让用户输入

                    except ValueError:

                        # 格式错误，不跳过，提示后让用户重新输入

                        print(f"日期格式错误！需严格符合 YYYY-MM-DD（例如 2025-11-08），请重新输入今天日期：")

            break

        # 兼容大小写：先转小写再判断

        elif change_date == 'n':

            # 不更改日期，仅保留年月日（忽略时分秒）

            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            break

        elif change_date not in ('y', 'n'):

            print("输入无效！请输入 'y' 或 'n'（小写）")

  

    # 当然这里用空格间隔也行，但是我懒得改ai一开始生成的代码

    # 将字符串转换为datetime对象

    while True:

        try:

            num_people = int(input("请问你要查询几个人: ").strip())

            if num_people <= 0:

                print("查询人数必须是正整数！请重新输入：")

                continue

            else:

                break

        except ValueError:

            print("输入无效！请输入一个整数（如 1、3）：")

    return today, num_people #这里可以return两种

        #break#这个是我为了防止死循环，写完while True直接写在这里的。

             #不过到最后发现return避免了死循环，不删了

  

def date_input(today,num_people):

    """

    根据查询人数，循环询问每个人的接种信息

    无效场景（不录入字典，提示信息无效）：

    1. 接种针数 ≤0 或 >3

    2. 日期格式不符合 YYYY-MM-DD

    返回：包含有效接种信息的列表（仅保留针数合理+日期格式正确的记录）

    """

    vaccination_records = []

    # 用try-expect来确排除是否有效输入！！！

    for i in range(num_people):

        print(f"\n--- 第{i+1}个人的信息 ---")

        # 标记当前人是否有效，默认无效

        is_valid = True

        doses = None  # 初始化针数变量

        # 1. 处理接种针数输入（双重校验：整数+合理范围，支持重新输入）

        max_attempts = 3  # 最大尝试次数（避免无限输错）

        attempts = 0      # 已尝试次数

        while attempts < max_attempts:

            try:

                # 第一步：检查是否为整数（非整数会触发ValueError）

                doses = int(input("请输入已经接种了几针: "))

                attempts += 1  # 尝试次数+1

  

                if doses < 0 or doses > 3:

                    print(f"❌ 第{i+1}个人：接种针数不合理（需1-2针）！还剩{max_attempts - attempts}次尝试，请重新输入：")

                else:

                    # 针数是整数且合理（0123针）→ 退出循环，继续后续逻辑

                    break

            except ValueError:

                # 捕获非整数输入（比如abc、1.5）

                attempts += 1

                print(f"❌ 第{i+1}个人：接种针数必须是整数！还剩{max_attempts - attempts}次尝试，请重新输入：")

        # 若3次尝试都失败 → 标记无效，跳过当前人

        if attempts >= max_attempts:

            print(f"❌ 第{i+1}个人：已连续{max_attempts}次输入错误，信息无效，跳过！")

            continue

        #continue永远是直接跳出本次循环

        #break是跳出全部循环

  

        # 针数检查在后面有QAQ

        """

        # 检查针数是否合理

        if doses > 3:

            print(f"第{i+1}个人的信息无效：不要开玩笑，接种针数超出合理范围！")

            is_valid = False

        elif doses == 3:

            print(f"第{i+1}个人的信息无效：已接种3针，不需要接种了！")

            is_valid = False

        elif doses <= 0:

            print(f"第{i+1}个人的信息无效：接种针数不能为0或负数！")

            is_valid = False

        # 针数无效直接跳过后续步骤

        if  is_valid == False :

            continue

        """

  

        while True:  # 无限循环，直到break退出

            if doses == 0 or doses == 3:

                last_date = today

                break

            last_date_str = input("请输入最近一次的接种日期(例如 2025-11-08） ： ")

            try:

                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")

                break  # 格式正确！跳出循环，不再让用户输入

            except ValueError:

                # 格式错误，不跳过，提示后让用户重新输入

                print(f"日期格式错误！需严格符合 YYYY-MM-DD（例如 2025-11-08），请重新输入第{i+1}个人的接种日期：")

        # 3. 仅当针数合理+日期正确时，才录入字典

        record = {

            'person_num' : i+1,

            'doses': doses,

            'last_date': last_date

        }

        vaccination_records.append(record)

        print(f"第{i+1}个人的信息录入成功！")

    return vaccination_records

  

def date_output(today, vaccination_records):

    """

    根据接种信息计算下一针接种时间和是否达到接种时间

    返回：包含每个人查询结果的列表

    """

    results = []

    for record in vaccination_records:

        #for 变量 in 列表: 是 专门用来遍历可迭代对象（比如列表）的循环

        doses = record['doses']

        last_date = record['last_date']

        if doses == 0:  # 未接种

            # 立即接种，所以显示True，日期为当前日期

            result_dict = {True: today.strftime("%Y-%m-%d")}

        elif doses == 1:  # 第一针

            # 第二针在第一针后30天

            next_date = last_date + timedelta(days=30)

            # 检查是否已达到接种时间

            can_vaccinate = today >= next_date

            result_dict = {can_vaccinate: next_date.strftime("%Y-%m-%d")}

        elif doses == 2:  # 第二针d

            # 第三针在第二针后180天

            next_date = last_date + timedelta(days=180)

            # 检查是否已达到接种时间

            can_vaccinate = today >= next_date

            result_dict = {can_vaccinate: next_date.strftime("%Y-%m-%d")}

        elif doses == 3:  # 第三针

            # 已完成所有接种

            result_dict = {False: ""}

  

        results.append(result_dict)

    return results

  

def main():

    """

    主函数，整合所有功能

    """

    # 获取当前日期和查询人数

    today, num_people = date_now()

    # 出来的两个数据要按顺序

    # 获取接种信息

    vaccination_records = date_input(today,num_people)

    # 计算并输出结果

    results = date_output(today, vaccination_records)

    # 显示结果

    print(f"\n查询结果: {results}")

  

if __name__ == "__main__":

    print('请正确输入数据，保证有效录入\n')

    main()
```

---



# 库和方法


**Python的架构：按层级封装代码，让代码整洁、好找、好用**

**顶层环境 → 库 / 包 → 模块 → 类 / 函数 → 对象 → 属性 / 方法**

兜兜转转半天发现可以自己写class。
```python
在vscode里面
蓝色（类）
绿色（方法）
self ——对象
self.name ——属性（其实name才叫属性）
class 里面是类
	def f()方法
```
- 类：可以写成 `变量 = 类名(...)`（创建对象），比如 `dt = datetime(2025, 11, 8)` —— 能这么写的一定是类；
	- **类的本质是「创建对象的模板 / 蓝图」—— 它只定义 “有什么属性、能做什么动作”，本身不是具体可用的东西，必须通过「变量 = 类名 (...)」的方式 “造” 出具体对象，才能真正用它的功能**。
	- 「用类（模板）造出了一个叫「dt」的变量 —— 这个变量的本质是「类的对象」」，只是我们习惯把「对象」存进变量里，方便后续调用～
- 方法（比如`now()`）：必须跟在「类或对象」后面（`datetime.now()`、`dt.strptime(...)`），不能单独写 `now()` 或 `strptime(...)`。

### 一、核心包含关系（从大到小）

| 架构层级                         | 通俗比喻                         | 核心作用                             | 对应之前的例子                                                                           |
| ---------------------------- | ---------------------------- | -------------------------------- | --------------------------------------------------------------------------------- |
| 1. Python 解释器                | 能驱动所有工具的 “发动机”               | 运行 Python 代码的核心环境（安装 Python 就自带） | 你双击运行`.py`文件时，背后工作的 “程序”                                                          |
| 2. 库 / 包（Library/Package）    | 装满工具的 “大衣柜”（或超市）             | 多个相关模块的集合，**提供一类完整功能**           | 标准库：os（操作系统工具）、datetime（时间工具）；第三方库：requests（网络请求）、pandas（数据处理）                    |
| 3. 模块（Module）                | 大衣柜里的 “抽屉”                   | **单个`.py`文件（或子文件夹），**分类存放相关代码    | os 库下的`pathlib`模块、datetime 库下的`datetime`模块                                        |
| 4. 类 / 函数（Class/Function）    | 抽屉里的 “收纳盒”（多功能）/“独立工具”（单一功能） | 封装具体逻辑：类是 “多功能工具集合”，函数是 “单一功能工具” | 类：`pathlib`模块下的`Path`、`datetime`模块下的`datetime`；<br>函数：`os`顶层的`getcwd()`、`print()` |
| 5. 对象 / 实例（Object/Instance）  | 拿出收纳盒准备用的 “具体工具”             | 类的 “实际使用版本”（类是模板，对象是模板造出来的具体工具）  | `folder = Path("./test")` 里的`folder`就是`Path`类的对象                                  |
| 6. 属性 / 方法（Attribute/Method） | 工具的 “部件 / 按钮”                | 对象的具体功能：属性是 “工具的特性”，方法是 “工具的用法”  | 属性：`folder.name`（文件夹名）；方法：`folder.exists()`、`datetime.now()`                      |

| 递推关系（库→模块→类→方法）                               | 各部分作用说明                                                      |
| --------------------------------------------- | ------------------------------------------------------------ |
| os（库）--- pathlib（模块）--- Path（类）--- exists（方法） | exists ()：判断路径（文件 / 文件夹）是否存在（比如 `Path("test.txt").exists()`） |

## 二、对应到 `datetime` 的具体例子

**根本不需要记这么多**<font color="#4bacc6">，你就知道有个函数是这样的就ojbk</font>
- `datetime` 类：管「具体的某一刻时间」（如 “现在”“2025 年元旦”）；
语法：`datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0)`

```python
today = datetime.strptime(today_str, "%Y-%m-%d")
`str` = string（字符串），`p` = parse（解析）
```


语法：`timedelta(days=0, seconds=0, minutes=0, hours=0, weeks=0)`


### 4. `datetime` 具体的某一刻时间
- `datetime` 类：管「具体的某一刻时间」（如 “现在”“2025 年元旦”）；
语法：`datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0)`

##### （1）把对象转成「自定义格式的字符串」（格式化输出，和 `strptime` 反向）

语法：`对象.strftime(格式符)`
format 格式化

```python
dt = datetime(2025, 11, 8, 14, 30, 5)
# 转成“2025年11月08日 14时30分”
print(dt.strftime("%Y年%m月%d日 %H时%M分"))  # 输出：2025年11月08日 14时30分
# 转成“25-11-08 02:30 PM”（12小时制）
print(dt.strftime("%y-%m-%d %I:%M %p"))  # 输出：25-11-08 02:30 PM
```

##### （2）转成「时间戳」（和其他系统交互常用，如前端、数据库）——方便改时间的

时间戳：从「1970-01-01 00:00:00 UTC」到当前时间的总秒数（浮点数）；

语法：`对象.timestamp()`


```python
dt = datetime(2025, 11, 8, 14, 30, 0)
timestamp = dt.timestamp()
print(timestamp)  # 输出：1757346600.0（具体值因时区略有差异）
```

##### （3）从「时间戳」转回对象（反向操作）

语法：`datetime.fromtimestamp(时间戳)`


```python
timestamp = 1757346600.0
dt = datetime.fromtimestamp(timestamp)
print(dt)  # 输出：2025-11-08 14:30:00（本地时区）
```

##### （4）修改时间（`datetime` 对象不可变，需生成新对象）

语法：`对象.replace(属性名=新值)`

```python
dt = datetime(2025, 11, 8, 14, 30)
# 修改年份为2026，小时为10
new_dt = dt.replace(year=2026, hour=10)
print(new_dt)  # 输出：2026-11-08 10:30:00
```
##### 快捷造「当前时间」对象（类方法，不用手动传参数）

- `datetime.now()`：造「本地时区」的当前时间对象（常用）；
- `datetime.utcnow()`：造「UTC 时区」的当前时间对象（比北京时间晚 8 小时）；

函数，（）传变量的，和c一样。

---
### 三、核心类 2：`timedelta` 类时间间隔
语法：`timedelta(days=0, seconds=0, minutes=0, hours=0, weeks=0)`

#### 1. 核心定位：

- 本质：「造时间间隔对象的模板」（比如 “2 天”“3 小时”“-10 分钟”）；
- 不能单独用，必须和 `datetime` 对象配合（时间 + 间隔 = 新时间，时间 - 时间 = 间隔）；
- 不支持「月份 / 年份」（因为 2 月可能 28/29 天，年份可能闰年，无法统一计算）。

#### 2. 创建 `timedelta` 对象的方式

语法：`timedelta(days=0, seconds=0, minutes=0, hours=0, weeks=0)`

- 所有参数都是可选的，默认 0；支持负数（表示 “过去的间隔”）；
- 单位换算：1 周 = 7 天，1 天 = 24 小时，1 小时 = 3600 秒；
- `timedelta` 类：管「两个时间的差 / 时间的加减」（如 “3 天后”“1 小时前”）；
```python
# 把字符串“2025/11/08 14:30:05”转成datetime对象
str_time = "2025/11/08 14:30:05"
dt = datetime.strptime(str_time, "%Y/%m/%d %H:%M:%S")  # 格式符要和字符串格式完全匹配
print(dt)  # 输出：2025-11-08 14:30:05（对象，可后续计算）

你比如说：

```


# 列表2
![[Pasted image 20251108110938.png]]

列表里面的元素可以是：字典、数字、字符串、列表等
**因为你要统计「多个人」的信息，列表是 Python 里最适合「批量收纳、统一管理多条结构化数据」的容器 —— 字典负责 “打包单个人的完整信息”，列表负责 “批量装下所有人的信息卡片”，两者配合才能高效处理 “多条记录” 的场景**。
# 字典
一般和列表一起用（本次也是）
### 2. 关于字典（`dict`）

- 核心是「键值对」，键唯一且不可变，值任意；
- 常用方法：`get()`（安全取值）、`items()`（遍历）、`update()`（批量增改）、`pop()`（安全删除）；
字典是另一种可变容器模型，且可存储任意类型对象。

字典的每个键值 key=>value 对用冒号 : 分割，每个对之间用逗号(**,**)分割，整个字典包括在花括号 {} 中 ,格式如下所示：
```
tinydict = {'name': 'runoob', 'likes': 123, 'url': 'www.runoob.com'}
键是字符串，其他的什么数据类型都可以
```
## 创建空字典

使用大括号 { } 创建空字典：
```
emptyDict = {}  
   
print(emptyDict)  
   
print("Length:", len(emptyDict))  
  
print(type(emptyDict))  

以上实例输出结果：

{}
Length: 0
<class 'dict'>
```
```
使用内建函数 dict() 创建字典：


emptyDict = dict()  
    
print(emptyDict)  
   
print("Length:",len(emptyDict))  
   
print(type(emptyDict))  

以上实例输出结果：
{}
Length: 0
<class 'dict'>
```
---

## 访问字典里的值

把**相应的键**放入到方括号中，如下实例:

```
tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'} 
print ("tinydict['Name']: ", tinydict['Name']) print ("tinydict['Age']: ", tinydict['Age'])

tinydict['Name']:  Runoob
tinydict['Age']:  7
```

## 改变已经搞好的字典
### 改变字典元素
tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'} tinydict['Age'] = 8 # 更新 Age tinydict['School'] = "菜鸟教程" # 添加信息

### 改变键
在 Python 中，**字典的键（key）不能直接修改**，但可以通过 “新增新键 + 删除旧键” 的方式间接实现 “替换键” 的效果。下面详细解释原因和具体方法：
### 各种删除
```
tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'} del tinydict['Name'] # 删除键 'Name' tinydict.clear() # 清空字典 del tinydict # 删除字典
```
### 特性
键必须不可变，所以可以用数字，字符串或元组充当，而用列表就不行。


## 字典内置函数&方法

Python字典包含了以下内置函数：

| 序号  | 函数及描述                                         | 实例                                                                                                                                     |
| --- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | len(dict)  <br>计算字典元素个数，即键的总数。                | >>> tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}<br>>>> len(tinydict)<br>3                                                |
| 2   | str(dict)  <br>输出字典，可以打印的字符串表示。               | >>> tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}<br>>>> str(tinydict)<br>"{'Name': 'Runoob', 'Class': 'First', 'Age': 7}" |
| 3   | type(variable)  <br>返回输入的变量类型，如果变量是字典就返回字典类型。 | >>> tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}<br>>>> type(tinydict)<br><class 'dict'>                                  |

Python字典包含了以下内置方法：

| 序号  | 函数及描述                                                                                                                                                    |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [dict.clear()](https://www.runoob.com/python3/python3-att-dictionary-clear.html)  <br>删除字典内所有元素                                                          |
| 2   | [dict.copy()](https://www.runoob.com/python3/python3-att-dictionary-copy.html)  <br>返回一个字典的浅复制                                                           |
| 3   | [dict.fromkeys()](https://www.runoob.com/python3/python3-att-dictionary-fromkeys.html)  <br>创建一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值                       |
| 4   | [dict.get(key, default=None)](https://www.runoob.com/python3/python3-att-dictionary-get.html)  <br>返回指定键的值，如果键不在字典中返回 default 设置的默认值                     |
| 5   | [key in dict](https://www.runoob.com/python3/python3-att-dictionary-in.html)  <br>如果键在字典dict里返回true，否则返回false                                            |
| 6   | [dict.items()](https://www.runoob.com/python3/python3-att-dictionary-items.html)  <br>以列表返回一个视图对象                                                        |
| 7   | [dict.keys()](https://www.runoob.com/python3/python3-att-dictionary-keys.html)  <br>返回一个视图对象                                                             |
| 8   | [dict.setdefault(key, default=None)](https://www.runoob.com/python3/python3-att-dictionary-setdefault.html)  <br>和get()类似, 但如果键不存在于字典中，将会添加键并将值设为default |
| 9   | [dict.update(dict2)](https://www.runoob.com/python3/python3-att-dictionary-update.html)  <br>把字典dict2的键/值对更新到dict里                                       |
| 10  | [dict.values()](https://www.runoob.com/python3/python3-att-dictionary-values.html)  <br>返回一个视图对象                                                         |
| 11  | [dict.pop(key[,default])](https://www.runoob.com/python3/python3-att-dictionary-pop.html)  <br>删除字典 key（键）所对应的值，返回被删除的值。                                 |
| 12  | [dict.popitem()](https://www.runoob.com/python3/python3-att-dictionary-popitem.html)  <br>返回并删除字典中的最后一对键和值。                                              |
|     |                                                                                                                                                          |

# Python sys 模块

`sys` 是 Python 标准库中的一个模块，提供了与 Python 解释器及其环境交互的功能。

通过 `sys` 库，你可以访问与 Python 解释器相关的变量和函数，例如命令行参数、标准输入输出、程序退出等。

### 列出库的内容
import sys  
print(dir(os))
**并没有用法和注释**
### 1. 命令行参数
`sys.argv` 是一个包含命令行参数的列表（也就是说typeof他是’list’）。`sys.argv[0]` 是脚本的名称，后续元素是传递给脚本的参数。
import sys  
  
print("脚本名称:", sys.argv[0])  
print("参数列表:", sys.argv[1:])
```bash
python demo.py 苹果 香蕉 100  True
参数列表: ['苹果', '香蕉', '100', 'True']
```
### 2. 程序退出
`sys.exit()` 用于退出程序。你可以传递一个整数作为退出状态码，通常 `0` 表示成功，非零值表示错误。
也就是 ctrl + Z

### 3. 标准输入输出

`sys.stdin`、`sys.stdout` 和 `sys.stderr` 分别代表标准输入、标准输出和标准错误流。你可以重定向这些流以实现
自定义的输入输出行为。
```
import sys  
  
# 重定向标准输出到文件  
with open('output.txt', 'w') as f:  
    sys.stdout = f  
    print("这行内容将写入 output.txt")  
  
# 恢复标准输出  
sys.stdout = sys.__stdout__  
print("这行内容将显示在控制台")
  
print("Python 版本:", sys.version)  
print("版本信息:", sys.version_info)
```

### 5. 模块搜索路径

`sys.path` 是一个列表，包含了 Python 解释器在导入模块时搜索的路径。你可以修改这个列表来添加自定义的模块搜索路径。
```
import sys  
  
print("模块搜索路径:", sys.path)  
sys.path.append('/custom/path')  
print("更新后的模块搜索路径:", sys.path)
```

# 字符串2
### `strip()` 的核心作用：去掉字符串「两端」的空白字符

# 脚本入口规范
只在你主动运行这个脚本时打开，别人想复用你代码里的函数时就关闭，不打扰别人。

#### 1. `__name__`：Python 的内置 “身份标识”

```
if __name__ == "__main__":

    print('请正确输入数据，保证有效录入\n')

    main()
```

每个 `.py` 文件（不管是你写的查询脚本，还是 Python 自带的模块），都有一个内置变量叫 `__name__`，它的值由 “文件的运行方式” 决定：

- 当你 **直接运行这个文件**（比如双击脚本、在终端输 `python 你的脚本名.py`）：`__name__` 会自动变成字符串 `"__main__"`；
	- 这时候，这个脚本就会全部运行，也就是运行main
- 
- 当你 **把这个文件当作模块导入到其他文件**（比如别人写了个新脚本，用 `import 你的脚本名` 复用 `date_now()` 函数）：`__name__` 会变成这个文件的文件名（比如你的脚本叫 `vaccine.py`，`__name__` 就变成 `"vaccine"`）。
	- 这时候，只要触及到vaccine脚本，那么他不会进入if里面，而是取用里面定义的函数。