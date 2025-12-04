# 通过while True + try-except + raise 处理无效输入.

class MedicineBottle:
    """药瓶类，表示单个药品容器"""
    def __init__(self, label: str, amount: float):
        """
        构造函数：创建药瓶对象时的初始化方法
        :param label: 药品名称（字符串类型）
        :param amount: 药品质量（浮点数类型）
        """
        if amount < 0:
            # 异常处理：当条件不满足时抛出错误
            raise ValueError("药品质量不能为负数")
        self.label = label    # 实例变量：每个药瓶都有自己的标签
        self.amount = amount  # 实例变量：每个药瓶都有自己的质量

    def add_medicine(self, amount: float):
        """增加药品质量"""
        if amount <= 0:
            raise ValueError("增加的质量必须为正数")
        self.amount += amount  # 简写：self.amount = self.amount + amount

    def take_medicine(self, amount: float):
        """
        减少药品质量
        :param amount: 要取出的质量
        :return: 实际取出的质量
        """
        if amount <= 0:
            raise ValueError("取出的质量必须为正数")
        
        if self.amount >= amount:
            self.amount -= amount
            return amount
        else:
            available = self.amount
            self.amount = 0
            return available

    def is_empty(self):
        """检查是否为空瓶"""
        return self.amount == 0

    def __repr__(self):
        """定义对象的字符串表示形式"""
        return f"<药瓶 {self.label}: {self.amount:.2f} g>"

class MedicineCabinet:
    """药柜类，管理多个药瓶"""
    
    def __init__(self):
        """构造函数：初始化空药柜"""
        self.bottles = []  # 创建空列表存储药瓶对象

    def find_bottle(self, label: str):
        """根据药品名称查找药瓶，返回药瓶对象或None"""
        for bottle in self.bottles:
            if bottle.label == label:
                return bottle
        return None

    def query_medicine(self, label: str):
        """查询指定药品的总质量：存在返回总质量，不存在返回 None"""
        total = 0.0
        has_medicine = False  # 标记是否找到该药品
        for bottle in self.bottles:
            if bottle.label == label:
                total += bottle.amount
                has_medicine = True  # 确认存在该药品
        # 找到则返回总质量，没找到返回 None
        return total if has_medicine else None

    def count_bottles_less_than(self, threshold: float):
        """统计剩余质量小于指定值的药瓶数量"""
        count = 0
        for bottle in self.bottles:
            if bottle.amount < threshold:
                count += 1
        return count

    def take_medicine(self, label: str, amount: float):
        """
        从药柜中取药（包含用户交互）
        增强点：用户输入确认时，用 while True 确保输入有效（仅允许 y/n）
        """
        bottle = self.find_bottle(label)
        if bottle is None:
            print(f"❌ 药柜中没有找到药品 '{label}'")
            return 0
        
        if bottle.amount >= amount:
            taken = bottle.take_medicine(amount)
            print(f"✅ 成功取出 {taken:.2f} g 的 {label}")
        else:
            print(f"⚠️  药品 '{label}' 存量不足，需要 {amount:.2f} g，但只有 {bottle.amount:.2f} g")
            # 增强1：循环询问直到用户输入有效选项（y/n）
            while True:
                response = input("存量不足，是否取出所有存量？(y/n): ").strip().lower()
                if response in ("y", "yes", "n", "no"):  # 允许多种有效输入
                    break
                print("❌ 输入无效！请输入 'y'（是）或 'n'（否）")  # 无效输入提示
            
            if response in ("y", "yes"):
                taken = bottle.take_medicine(bottle.amount)
                print(f"✅ 已取出所有存量 {taken:.2f} g 的 {label}")
            else:
                print("ℹ️  取消取药")
                return 0
        
        # 检查并移除空瓶
        if bottle.is_empty():
            self.bottles.remove(bottle)
            print(f"ℹ️  已移除空瓶: {label}")
        
        return amount if bottle.amount >= amount else bottle.amount

    def add_medicine(self, label: str, amount: float):
        """添加药品到药柜"""
        if amount <= 0:
            raise ValueError("添加的药品质量必须为正数")
        
        bottle = self.find_bottle(label)
        if bottle:
            bottle.add_medicine(amount)
            print(f"✅ 已向现有药瓶添加 {amount:.2f} g 的 {label}")
        else:
            new_bottle = MedicineBottle(label, amount)
            self.bottles.append(new_bottle)
            print(f"✅ 已创建新药瓶: {new_bottle}")

    def __repr__(self):
        """返回药柜的字符串表示"""
        if not self.bottles:
            return "<空药柜>"
        return f"<药柜，共有 {len(self.bottles)} 个药瓶>"

# 测试代码（完全重构为交互式，增强鲁棒性）
if __name__ == "__main__":

    print("药品管理系统")    
    cab = MedicineCabinet()
    
    # 增强2：主循环，让程序持续运行直到用户选择退出
    while True:
        print("\n请选择操作： 1. 添加药品 2. 取出药品 3. 查询药品总量 4. 统计低存量药瓶 5. 查看药柜状态 6. 退出系统")
        # 增强3：处理操作选项输入（确保输入是 1-6 的整数）
        while True:
            choice_input = input("\n请输入操作编号（1-6）：").strip()
            try:
                choice = int(choice_input)  # 尝试转为整数
                if 1 <= choice <= 6:
                    break  # 输入有效，退出循环
                else:
                    print("❌ 输入无效！请输入 1-6 之间的数字")
            except ValueError:
                # 捕获非数字输入异常
                print(f"❌ 输入无效！'{choice_input}' 不是有效的数字，请重新输入")
        
        # 增强4：每个操作都用 try-except 捕获异常（如负数质量、无效输入）
        if choice == 1:
            # 添加药品：处理标签和质量的有效输入
            print("\n--- 添加药品 ---")
            while True:
                label = input("请输入药品名称：").strip()
                if label:  # 确保标签不为空
                    break
                print("❌ 药品名称不能为空，请重新输入")
            
            while True:
                amount_input = input("请输入添加的质量（g）：").strip()
                try:
                    amount = float(amount_input)  # 尝试转为浮点数
                    cab.add_medicine(label, amount)  # 调用方法（可能抛 ValueError）
                    break
                except ValueError as e:
                    # 捕获两种异常：1. 非数字输入 2. 质量为负/零
                    print(f"❌ 添加失败：{e}，请重新输入")
        
        elif choice == 2:
            # 取出药品：先验证药品存在，再输入取出质量
            print("\n--- 取出药品 ---")
            while True:
                # 第一步：输入并验证药品标签（非空）
                label = input("请输入药品名称：").strip()
                if not label:
                    print("❌ 药品名称不能为空，请重新输入")
                    continue  # 重新输入标签
                
                # 第二步：判断药品是否存在（复用 find_bottle 函数）
                bottle = cab.find_bottle(label)
                if bottle is None:
                    # 药品不存在，询问是否重新输入标签
                    retry = input(f"❌ 没有找到药品 '{label}' TAT，是否重新输入药品名称？（y/n）").strip().lower()
                    if retry != 'y':
                        print("ℹ️  已取消取出操作")
                        break  # 退出取出流程，返回主菜单
                    continue  # 重新输入标签
                
                # 第三步：药品存在，再输入并验证取出质量
                while True:
                    amount_input = input(f"请输入取出 '{label}' 的质量（g）：").strip()
                    try:
                        amount = float(amount_input)
                        # 额外验证：取出质量不能为负数（避免误输入负数）
                        if amount <= 0:
                            print("❌ 取出质量必须大于0，请重新输入")
                            continue
                        # 调用取药方法（假设 take_medicine 已处理存量不足等逻辑）
                        cab.take_medicine(label, amount)
                        print(f"✅ 成功取出 '{label}' {amount:.2f} g")
                        break  # 质量输入正确，取药完成，退出质量循环
                    except ValueError as e:
                        print(f"❌ 取出失败：输入的质量不是有效数字（{e}），请重新输入")
                
                break  # 取药流程全部完成，退出总循环
        elif choice == 3:
            print("\n--- 查询药品总量 ---")
            label = input("请输入要查询的药品名称：").strip()
            total = cab.query_medicine(label)  # 接收优化后的返回值
            
            if total is None:
                # 没找到药品：友好提示
                print(f"❌ 没有找到药品 '{label}' TAT")
            else:
                # 找到药品：显示总质量（即使是0.0也会提示）
                print(f"ℹ️  药品 '{label}' 的总质量为：{total:.2f} g")
        
        elif choice == 4:
            # 统计低存量药瓶：处理阈值输入
            print("\n--- 统计低存量药瓶 ---")
            while True:
                threshold_input = input("请输入阈值质量（g）：").strip()
                try:
                    threshold = float(threshold_input)
                    if threshold >= 0:
                        count = cab.count_bottles_less_than(threshold)
                        print(f"ℹ️  剩余质量小于 {threshold:.2f} g 的药瓶数量：{count} 个")
                        break
                    else:
                        print("❌ 阈值不能为负数，请重新输入")
                except ValueError:
                    print(f"❌ 输入无效！'{threshold_input}' 不是有效的数字，请重新输入")
        
        elif choice == 5:
            # 查看药柜状态
            print("\n--- 药柜状态 ---")
            print(f"ℹ️  {cab}")
            if cab.bottles:
                print("当前药瓶列表：")
                for idx, bottle in enumerate(cab.bottles, 1):
                    print(f"  {idx}. {bottle}")
        
        elif choice == 6:
            # 退出系统
            print("\n👋 感谢使用药品管理系统，再见！")
            break