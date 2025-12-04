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
                
            while True:  # 无限循环，直到break退出
                    today_str = input("请输入今天的日期(例如:2022-09-09): ")
            #input直接是带提示的对话框。输入类型是字符串
                    try:
                        today = datetime.strptime(today_str, "%Y-%m-%d")
                        print(f"日期已更新为：{today.strftime('%Y-%m-%d')}")
                        break  # 格式正确！跳出循环，不再让用户输入
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
        doses = None  # 初始化针数变量
        
        # 1. 处理接种针数输入（双重校验：整数+合理范围，支持重新输入）
        max_attempts = 3  # 最大尝试次数（避免无限输错）
        attempts = 0      # 已尝试次数
        while attempts < max_attempts:
            try:
                # 第一步：检查是否为整数（非整数会触发ValueError）
                doses = int(input("请输入已经接种了几针: "))
                attempts += 1  # 尝试次数+1
                

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
        if  is_valid == False :
            continue
        """

        while True:  # 无限循环，直到break退出
            if doses == 0 or doses == 3: 
                last_date = today
                break
            last_date_str = input("请输入最近一次的接种日期(例如 2025-11-08） ： ")
            try:
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                break  # 格式正确！跳出循环，不再让用户输入
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
        
        if doses == 0:  # 未接种
            # 立即接种，所以显示True，日期为当前日期
            result_dict = {True: today.strftime("%Y-%m-%d")}
        
        elif doses == 1:  # 第一针
            # 第二针在第一针后30天
            next_date = last_date + timedelta(days=30)
            # 检查是否已达到接种时间
            can_vaccinate = today >= next_date
            result_dict = {can_vaccinate: next_date.strftime("%Y-%m-%d")}
        
        elif doses == 2:  # 第二针d
            # 第三针在第二针后180天
            next_date = last_date + timedelta(days=180)
            # 检查是否已达到接种时间
            can_vaccinate = today >= next_date
            result_dict = {can_vaccinate: next_date.strftime("%Y-%m-%d")}
        
        elif doses == 3:  # 第三针
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