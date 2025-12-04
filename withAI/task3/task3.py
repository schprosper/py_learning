# 通过while True + try-except + raise 处理无效输入.
# 通过引入typing库规范化输出.
# 不要在药瓶层面做这里做复杂的输入重试逻辑 , 会把UI逻辑混入业务逻辑
# 药瓶层面是计算逻辑,交互main那里是UI逻辑.

# 药瓶计算层,无交互逻辑
# 除了一开始的循环交互界面,while True包裹的都是对输入的检验
class MedicineBottle:
    def __init__(self,label:str,amount:float):
        if amount <0:  
            raise ValueError("药品质量不能为负数")
            # 这里的报错肯定需要被调用他之后的下一个语句接住

        ''' 
        # 这是业务规则，不是输入验证.在这个规则下能做业务操作就行
        # 如果说是输入验证,那么我们的确需要检验他是不是输入字符串
        # 但是,这里amount:float,明确表示,只要能够输入进来,说明他必定是浮点
        # 所以,我们在业务模块就默认他是浮点数,只对浮点数本身做防御
        '''
        
        self.label = label
        self.amount = amount

    def __repr__(self):
        return f"<药瓶 {self.label}: {self.amount:.2f} g>"
    
    # 加入药品
    def add_medicine (self,amount:float) -> None:
        if amount <= 0:
            raise ValueError("增加的质量必须为正数")
        self.amount += amount

    # 取出 药品的规则而非输入规则
    def take_medicine (self,amount:float) -> float:
        if amount <=0:
            raise ValueError("取出的质量必须为正数")
        
        if self.amount >= amount:
            self.amount -= amount
            return amount
        else:
            available = self.amount
            self.amount = 0
            return available
    
    def is_empty(self):
        return self.amount == 0
    
    def get_remaining(self) ->float:
        return self.amount
    

    

class MedicineCabinet :
    def __init__(self):
        self.bottles = []

    def find_bottle(self,label:str):
        for bottle in  self.bottles: #遍历列表
            if bottle.label == label: # 让输入和属性匹配
                return bottle
        return None #当为None的时候,就说名查找失败,这是交互输出的时候用到的
    
    def query_total_amount(self,label:str):
        total = 0.0
        has_bottle = False
        for bottle in self.bottles:
            if bottle.label == label:
                total +=bottle.amount
                has_bottle = True
        return total if has_bottle else None
        # 如果有这个药就返回它本身,如果没有就None来告诉没有
    
    #低于存量的药瓶数量
    def count_low_stock_bottles(self,threshold): #英语:临界值
        if threshold < 0:
            raise ValueError
        return sum(1 for bottle in self.bottles 
                   if bottle.amount < threshold)
    
    def take_medicine(self,label:str,amount:float,
                      take_all_if_insufficient: bool = False):
        '''
        结构化输入
        返回格式：{"status": 状态, "actual_taken": 实际取出量,
                  "message": 业务信息, "is_empty": 是否空瓶}
        状态值："success"（正常取药）、
                "insufficient"（存量不足）、
                "not_found"（药品不存在）
        '''
        #有没有药品

        bottle = self.find_bottle(label)
        if not bottle:
            return {
                "status": "not_found",
                "actual_taken": 0.0,
                "message": f"药品'{label}'不存在",
                "is_empty": False
            }
        
        remaining = bottle.get_remaining()

        # 存量充足(包含正好+多于)
        if remaining >= amount:
            actual_taken = bottle.take_medicine(amount)
            is_empty = bottle.is_empty()
            if is_empty:
                self.bottles.remove(bottle)
            return {
                    "status": "success",
                    "actual_taken": actual_taken,
                    "message": f"正常取出{actual_taken:.2f}g",
                    "is_empty": is_empty
                }
    
        # 处理存量不足情况
        if not take_all_if_insufficient :
            return {
                "status": "insufficient",
                "actual_taken": 0.0,
                "message": f"存量{remaining:.2f}g < 需求{amount:.2f}g",
                "is_empty": False
            }
        # 存量不足取出所有(不过这里不问你是否要去取出所有)
        actual_taken = bottle.take_medicine(remaining)
        self.bottles.remove(bottle)
        return {
            "status": "success",
            "actual_taken": actual_taken,
            "message": f"存量不足，取完所有{actual_taken:.2f}g",
            "is_empty": True
        }
    
    def add_medicine(self,label:str,amount:float):
        if amount <= 0:
            raise ValueError
        # 先看有没有这这瓶药
        bottle = self.find_bottle(label)
        # 如果有,那么通过return一个字典来保证我的输出就很方便了
        if bottle:
            bottle.add_medicine(amount)
            return {
                "status": "success",
                "bottle": bottle,
                "message": f"向已有药瓶添加{amount:.2f}g"
            }
        
        # 新建药瓶
        new_bottle = MedicineBottle(label,amount)
        self.bottles.append(new_bottle)
        return {
            "status": "success",
            "bottle": new_bottle,
            "message": "创建新药瓶并添加药品"
        }
    # 药柜状态
    def get_cabinet_status(self):
        if not self.bottles:
            return {"status": "empty", "message": "空药柜", "bottles": []}
        return {
            "status": "has_bottles",
            "message": f"共{len(self.bottles)}个药瓶",
            "bottles": self.bottles.copy()  # 返回副本，避免外部修改
        }
    


# 用户交互----保证我对业务层输入的数据是对的,保证对用户能看懂我的反馈
def main():

    print("药品管理系统")
    cab = MedicineCabinet()
#在这里新建一个药柜
#之后如果需要很多个药柜,我们就可以再次嵌套类:房间

    while True:
        #单纯是界面
        print("请选择操作：")
        print("1. 添加药品  2. 取出药品  3. 查询药品总量")
        print("4. 统计低存量药瓶  5. 查看药柜状态  6. 退出系统")

        # 优先处理选择业务种类的输入问题
        # 2. 选择操作（输入验证：交互层）
        while True:
            choice_input = input("请输入操作编号（1-6）：").strip()
            try:
                choice = int(choice_input)
                if 1 <= choice <= 6:
                    break
                print("❌ 请输入1-6之间的有效编号！")
            except ValueError:
                print(f"❌ '{choice_input}' 不是有效数字，请重新输入！")

        # 添加药品
        if choice == 1:
            print("\n---  添加药品 ---")
            # 输入标签
            while True:
                label = input("请输入药品名称：").strip()
                if label:
                    break
                print("❌ 药品名称不能为空！")
            # 输入质量
            while True:
                amount_input = input("请输入添加的质量（g）：").strip()
                try:
                    # 先验证到底是不是数字
                    amount = float(amount_input)
                    # 再自动验证数字是否合法(这里,由于之前写过判断,我们只需要保证这里输入的是浮点数即可)
                    result = cab.add_medicine(label, amount)# 返回一个字典
                    # 反馈结果
                    print(f"✅ {result['message']}：{result['bottle']}")
                    break
                except ValueError as e:# 在add_medicine出问题就返回错误原因
                    print(f"❌ 添加失败：{e}")

        elif choice == 2:
            print("\n---  🔔取出药品 ---")
            # 先检验药品是否存在
            while True:
                label = input("请输入药品名称：").strip()
                if not label:
                    print("❌ 药品名称不能为空！")
                    continue #其实这里直接回到了while循环,加不加一样,但是加了好看

                # 调用业务层：检查药品是否存在
                if not cab.find_bottle(label):

                    retry = input(f"❌ 未找到药品'{label}'，是否重新输入？（y/n）").strip().lower()
                    if retry != "y":
                        print("ℹ️  取消取药操作")
                        break
                    continue
                # 药品存在，进入下一步
                break
            if not cab.find_bottle(label):
                continue  # 已取消取药

            # 第二步：输入取出质量（交互层）,保证质量是整数并且不为负数
            while True:
                amount_input = input(f"请输入取出'{label}'的质量（g）：").strip()
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        print("❌ 取出质量必须大于0！")
                        continue 
                    break
                except ValueError:
                    print(f"❌ '{amount_input}' 不是有效数字，请重新输入！")
                    continue

            # 第三步：调用业务层取药（先检查存量）
            check_result = cab.take_medicine(label, amount, take_all_if_insufficient=False)
            if check_result["status"] == "insufficient":
                # 存量不足，交互层询问是否取完
                # 如果不足,那么返回来的值就是存量,至于说你用不用这个值,那看你
                while True:
                    response = input(f"⚠️ {check_result['message']}，是否取完所有存量？（y/n）").strip().lower()
                    if response in ("y", "n"):
                        break
                    print("❌ 请输入'y'（是）或'n'（否）！")
                if response == "n":
                    print("ℹ️  取消取药操作")
                    continue
                # 确认取完，调用业务层取所有
                final_result = cab.take_medicine(label, amount, take_all_if_insufficient=True)
            else:
                final_result = check_result

            # 反馈取药结果（交互层）
            if final_result["status"] == "success":
                print(f"✅ {final_result['message']}")
                if final_result["is_empty"]:
                    print(f"ℹ️  已自动移除空瓶：{label}")

        elif choice == 3:
            print("\n--- 🔔 查询药品总量 ---")
            label = input("请输入药品名称：").strip()
            # 调用业务层查询
            total = cab.query_total_amount(label)
            if total is None:
                print(f"❌ 未找到药品'{label}' TAT")
            else:
                print(f"ℹ️  药品'{label}'的总质量为：{total:.2f} g")

        elif choice == 4:
            print("\n--- 🔔 统计低存量药瓶 ---")
            while True:
                threshold_input = input("请输入阈值质量（g）：").strip()
                try:
                    threshold = float(threshold_input)
                    # 调用业务层统计
                    count = cab.count_low_stock_bottles(threshold)
                    print(f"ℹ️  剩余质量小于{threshold:.2f}g的药瓶数量：{count}个")
                    break
                except ValueError as e:
                    print(f"❌ 输入无效：{e}")

        elif choice == 5:
            print("\n--- 🔔 查看药柜状态 ---")
            # 调用业务层获取状态
            status = cab.get_cabinet_status()
            print(f"ℹ️ {status['message']}")
            if status["bottles"]:
                print("当前药瓶列表：")
                for idx, bottle in enumerate(status["bottles"], 1):
                    print(f"  {idx}. {bottle}")

        elif choice == 6:
            print("\n👋 感谢使用药品管理系统，再见！")
            break


if __name__ == "__main__":
    main()


    
    #如果要初始化一个有特定种类药的药柜，应该如何实现药柜的初始化函数？
    
    '''
        首先,需要用到已经有了的模块:复用＞新增，兼容＞重构
        首先保证基本功能:就算不传入一个 有了药的药柜A 我们也能运行代码
        所以,传进来的那个新的药柜应该是一个可选的参数,直接假设值是None
        def __init__(self, initial_medicines: list[tuple[str, float]] = None):
        

                # 处理预设药品：如果传入了列表，批量添加到药柜
        if initial_medicines is not None:
            # 遍历预设药品列表，逐个添加
            for label, amount in initial_medicines:
                # 复用 add_medicine 方法：自动处理验证（amount>0）、重复药品合并 
                self.add_medicine(label, amount)

    '''

def __init__(self, initial_medicines: list[tuple[str, float]] = None):
    if initial_medicines is not None:
        for label, amount in initial_medicines:
            self.add_medicine(label, amount)