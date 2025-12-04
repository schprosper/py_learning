from datetime import datetime, timedelta
# 今日日期以及需要查询的人数
def date_now():
    while True:
        today = datetime.now().replace(hour=0 , minute=0 , second=0 , microsecond=0 )
        change_date = input(f"查询知，今天的日期是{today},要更改日期请输入y，不更改请输入n：")
        if change_date == 'y':
                while True:
                        today_str = input("输入今天的日期(例如:2025-11-09): ")
                        try :
                            today = datetime.strptime(today_str,"%Y-%m-%d")
                            print(f"日期已更新为：{today.strftime('%Y-%m-%d')}")
                            break
                        except ValueError:
                              print(f"日期格式错误！需严格符合 YYYY-MM-DD（例如 2025-11-09），请重新输入今天日期：")
                break
        
        elif change_date == 'n':
              today = datetime.now().replace(hour=0 , minute=0 , second=0 , microsecond=0 )
              break
        elif change_date not in ('y', 'n'):
              print("输入无效！请输入 'y' 或 'n'（小写）")

    while True:
        try:
              num_people = int(input("请问你要查询几个人:").strip())
              if num_people <= 0:
                    print("查询人数必须是正整数！请重新输入：")
                    continue
              else: 
                break
        except ValueError:
            print("输入无效！请输入一个整数（如 1、3）：")

    return today, num_people

# 确定每个人的疫苗接种情况
def date_input(today,num_people):
    vaccination_records = []

    for i in range(num_people):
        print(f"\n--- 第{i+1}个人的信息 ---")
        is_valid = True
        doses = None

        while True:
             try:
                  doses = int(input("请输入已经接种了几针: "))
                  if doses <0 or doses >3:
                       print(f"❌ 第{i+1}个人：接种针数不合理（需0-3针）！请重新输入：")
                  else:
                       break
                  
             except ValueError:
                  print(f"❌ 第{i+1}个人：接种针数必须是整数！请重新输入：")

        while True:  # 无限循环，直到break退出
            if doses == 0 or doses == 3: 
                last_date = today
                break
            last_date_str = input("请输入最近一次的接种日期(例如 2025-11-09） ： ")
            try:
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                break  # 格式正确！跳出循环，不再让用户输入
            except ValueError:
                # 格式错误，不跳过，提示后让用户重新输入
                print(f"日期格式错误！需严格符合 YYYY-MM-DD（例如 2025-11-09），请重新输入第{i+1}个人的接种日期：")
        record ={
        'person_num' : i+1,
        'doses': doses,
        'last_date': last_date
                }
    vaccination_records.append(record)
    print(f"第{i+1}个人的信息录入成功！")

    return vaccination_records

def date_output(today, vaccination_records):

    results = []
    
    for record in vaccination_records:
        
        doses = record['doses']
        last_date = record['last_date']
        
        if doses == 0:  
            result_dict = {True: today.strftime("%Y-%m-%d")}
        
        elif doses == 1:  
            
            next_date = last_date + timedelta(days=30)

            can_vaccinate = (today >= next_date)
            result_dict = {can_vaccinate: next_date.strftime("%Y-%m-%d")}
        
        elif doses == 2:  
            
            next_date = last_date + timedelta(days=180)
            
            can_vaccinate = today >= next_date
            result_dict = {can_vaccinate: next_date.strftime("%Y-%m-%d")}
        
        elif doses == 3:  
            
            result_dict = {False: ""}
        

        
        results.append(result_dict)
    
    return results

def main():

    today, num_people = date_now() 

    vaccination_records = date_input(today,num_people)
    
    results = date_output(today, vaccination_records)
    
    print(f"\n查询结果: {results}")

if __name__ == "__main__":
    print('请正确输入数据，保证有效录入\n')
    main()
