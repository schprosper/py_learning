import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pygame
import os
import json
from datetime import timedelta
from tkinter import font as tkFont

# 配置文件路径
CONFIG_FILE = "timer_config.json"

class ModernTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("智能计时器 Pro")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        # 初始化 pygame 用于播放声音
        pygame.mixer.init()
        
        # 计时器状态
        self.is_running = False
        self.remaining_time = 0  # 剩余时间（秒）
        self.total_time = 0      # 总时间（秒）
        self.reminder_interval = 0  # 重复提醒间隔（秒）
        self.custom_reminder_times = []  # 自定义提醒时间点（秒）
        self.last_reminder_time = 0  # 上次重复提醒时间
        self.triggered_reminders = set()  # 已触发的单次提醒
        self.timer_thread = None
        
        # 加载提示音
        self.warning_sound = self.load_sound("warning.wav")
        self.finish_sound = self.load_sound("finish.wav")
        
        # 加载上次配置
        self.load_config()
        
        # 初始化界面样式
        self.setup_style()
        
        # 创建UI界面
        self.create_ui()
        
    def load_sound(self, filename):
        """加载提示音文件"""
        try:
            if os.path.exists(filename):
                return pygame.mixer.Sound(filename)
            else:
                return None
        except Exception as e:
            print(f"加载声音文件失败: {e}")
            return None
    
    def play_sound(self, sound):
        """播放提示音"""
        try:
            if sound:
                sound.play()
            else:
                # 系统蜂鸣音（三声，更醒目）
                for _ in range(3):
                    self.root.bell()
                    time.sleep(0.15)
        except:
            pass
    
    def setup_style(self):
        """设置界面样式"""
        self.style = ttk.Style()
        
        # 定义颜色主题
        self.colors = {
            "primary": "#4a90e2",
            "secondary": "#5cb85c",
            "warning": "#f0ad4e",
            "danger": "#d9534f",
            "light": "#f8f9fa",
            "dark": "#343a40",
            "gray": "#6c757d",
            "light_gray": "#e9ecef",
            "background": "#f5f7fa",
            "card_bg": "#ffffff",
            "progress": "#4a90e2"
        }
        
        # 配置样式
        self.style.configure(".", 
                           background=self.colors["background"],
                           foreground=self.colors["dark"],
                           font=("微软雅黑", 11))
        
        # 配置框架样式
        self.style.configure("Card.TFrame", 
                           background=self.colors["card_bg"],
                           relief="solid",
                           borderwidth=1)
        
        # 配置按钮样式
        self.style.configure("Primary.TButton",
                           background=self.colors["primary"],
                           foreground="white",
                           font=("微软雅黑", 12, "bold"),
                           padding=10)
        self.style.map("Primary.TButton",
                      background=[("active", self.darken_color(self.colors["primary"], 0.1))],
                      relief=[("pressed", "sunken"), ("active", "raised")])
        
        self.style.configure("Success.TButton",
                           background=self.colors["secondary"],
                           foreground="white",
                           font=("微软雅黑", 12, "bold"),
                           padding=10)
        self.style.map("Success.TButton",
                      background=[("active", self.darken_color(self.colors["secondary"], 0.1))])
        
        self.style.configure("Warning.TButton",
                           background=self.colors["warning"],
                           foreground="white",
                           font=("微软雅黑", 12, "bold"),
                           padding=10)
        self.style.map("Warning.TButton",
                      background=[("active", self.darken_color(self.colors["warning"], 0.1))])
        
        # 配置标签样式
        self.style.configure("Title.TLabel",
                           font=("微软雅黑", 24, "bold"),
                           foreground=self.colors["primary"],
                           background=self.colors["background"])
        
        self.style.configure("Time.TLabel",
                           font=("微软雅黑", 40, "bold"),
                           foreground=self.colors["dark"],
                           background=self.colors["card_bg"])
        
        self.style.configure("Subtitle.TLabel",
                           font=("微软雅黑", 14, "bold"),
                           foreground=self.colors["dark"],
                           background=self.colors["card_bg"])
        
        self.style.configure("Status.TLabel",
                           font=("微软雅黑", 11),
                           background=self.colors["background"])
        
        # 配置输入框样式
        self.style.configure("Modern.TEntry",
                           font=("微软雅黑", 12),
                           padding=8,
                           relief="solid",
                           borderwidth=1,
                           fieldbackground="white")
        self.style.map("Modern.TEntry",
                      bordercolor=[("focus", self.colors["primary"])],
                      relief=[("focus", "solid")])
        
        # 配置下拉框样式
        self.style.configure("Modern.TCombobox",
                           font=("微软雅黑", 12),
                           padding=8)
        self.style.map("Modern.TCombobox",
                      fieldbackground=[("readonly", "white")],
                      bordercolor=[("focus", self.colors["primary"])])
        
        # 配置进度条样式
        self.style.configure("Modern.Horizontal.TProgressbar",
                           background=self.colors["progress"],
                           troughcolor=self.colors["light_gray"],
                           borderwidth=0,
                           relief="flat")
        self.style.map("Modern.Horizontal.TProgressbar",
                      background=[("active", self.colors["primary"])])
    
    def darken_color(self, color, factor):
        """加深颜色"""
        hex_color = color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def create_ui(self):
        """创建现代化UI界面"""
        # 设置背景色
        self.root.configure(bg=self.colors["background"])
        
        # 主容器
        main_container = ttk.Frame(self.root, style="Card.TFrame")
        main_container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # 圆角效果（通过画布实现）
        self.add_rounded_corners(main_container, 15)
        
        # 标题区域
        title_frame = ttk.Frame(main_container, style="Card.TFrame")
        title_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ttk.Label(title_frame, text="智能计时器 Pro", style="Title.TLabel")
        title_label.pack(anchor="center")
        
        # 计时显示区域
        time_frame = ttk.Frame(main_container, style="Card.TFrame")
        time_frame.pack(pady=10, padx=30, fill="x")
        
        # 时间显示
        self.time_display = ttk.Label(time_frame, text="00:00:00", style="Time.TLabel")
        self.time_display.pack(anchor="center", pady=10)
        
        # 进度条
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            time_frame,
            variable=self.progress_var,
            maximum=100,
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=5, padx=20, fill="x")
        
        # 设置区域（使用网格布局）
        settings_frame = ttk.Frame(main_container, style="Card.TFrame")
        settings_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        # 总时间设置
        ttk.Label(settings_frame, text="总计时设置", style="Subtitle.TLabel").grid(
            row=0, column=0, columnspan=6, pady=(0, 15), sticky="w"
        )
        
        ttk.Label(settings_frame, text="时:", background=self.colors["card_bg"]).grid(
            row=1, column=0, padx=(0, 5), pady=5, sticky="e"
        )
        self.hour_var = tk.StringVar(value=str(self.last_config.get("hours", 0)))
        hour_entry = ttk.Entry(
            settings_frame, 
            textvariable=self.hour_var, 
            width=6, 
            style="Modern.TEntry",
            justify="center"
        )
        hour_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="分:", background=self.colors["card_bg"]).grid(
            row=1, column=2, padx=(5, 5), pady=5, sticky="e"
        )
        self.minute_var = tk.StringVar(value=str(self.last_config.get("minutes", 0)))
        minute_entry = ttk.Entry(
            settings_frame, 
            textvariable=self.minute_var, 
            width=6, 
            style="Modern.TEntry",
            justify="center"
        )
        minute_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="秒:", background=self.colors["card_bg"]).grid(
            row=1, column=4, padx=(5, 5), pady=5, sticky="e"
        )
        self.second_var = tk.StringVar(value=str(self.last_config.get("seconds", 0)))
        second_entry = ttk.Entry(
            settings_frame, 
            textvariable=self.second_var, 
            width=6, 
            style="Modern.TEntry",
            justify="center"
        )
        second_entry.grid(row=1, column=5, padx=5, pady=5)
        
        # 提醒设置
        ttk.Label(settings_frame, text="提醒设置", style="Subtitle.TLabel").grid(
            row=2, column=0, columnspan=6, pady=(15, 15), sticky="w"
        )
        
        # 自定义提醒时间
        ttk.Label(settings_frame, text="倒数提醒:", background=self.colors["card_bg"]).grid(
            row=3, column=0, padx=(0, 5), pady=5, sticky="e"
        )
        self.reminder_time_var = tk.StringVar(value=self.last_config.get("reminder_times", "1"))
        reminder_entry = ttk.Entry(
            settings_frame, 
            textvariable=self.reminder_time_var, 
            width=18, 
            style="Modern.TEntry"
        )
        reminder_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)
        
        # 提醒单位
        self.reminder_unit_var = tk.StringVar(value=self.last_config.get("reminder_unit", "分钟"))
        unit_combobox = ttk.Combobox(
            settings_frame, 
            textvariable=self.reminder_unit_var,
            values=["秒", "分钟"],
            width=10,
            style="Modern.TCombobox",
            state="readonly"
        )
        unit_combobox.grid(row=3, column=3, padx=5, pady=5)
        
        # 重复提醒
        ttk.Label(settings_frame, text="重复间隔:", background=self.colors["card_bg"]).grid(
            row=3, column=4, padx=(15, 5), pady=5, sticky="e"
        )
        self.repeat_interval_var = tk.StringVar(value=str(self.last_config.get("repeat_interval", 0)))
        repeat_entry = ttk.Entry(
            settings_frame, 
            textvariable=self.repeat_interval_var, 
            width=8, 
            style="Modern.TEntry",
            justify="center"
        )
        repeat_entry.grid(row=3, column=5, padx=5, pady=5)
        ttk.Label(settings_frame, text="分钟", background=self.colors["card_bg"]).grid(
            row=3, column=6, padx=(5, 0), pady=5, sticky="w"
        )
        
        # 控制按钮区域
        btn_frame = ttk.Frame(main_container, style="Card.TFrame")
        btn_frame.pack(pady=20, padx=30, fill="x")
        
        # 开始按钮
        self.start_btn = ttk.Button(
            btn_frame, 
            text="开始计时", 
            command=self.start_timer,
            style="Success.TButton",
            width=15
        )
        self.start_btn.pack(side="left", padx=10, fill="x", expand=True)
        
        # 暂停按钮
        self.pause_btn = ttk.Button(
            btn_frame, 
            text="暂停", 
            command=self.pause_timer,
            style="Warning.TButton",
            width=15,
            state="disabled"
        )
        self.pause_btn.pack(side="left", padx=10, fill="x", expand=True)
        
        # 重置按钮
        self.reset_btn = ttk.Button(
            btn_frame, 
            text="重置", 
            command=self.reset_timer,
            style="Primary.TButton",
            width=15
        )
        self.reset_btn.pack(side="left", padx=10, fill="x", expand=True)
        
        # 状态提示区域
        self.status_label = ttk.Label(
            self.root, 
            text="提示：可设置多个提醒时间（例：5,1,0.5 表示5分钟、1分钟、30秒时提醒）", 
            style="Status.TLabel",
            foreground=self.colors["gray"]
        )
        self.status_label.pack(pady=10)
        
        # 初始化时间显示
        self.update_display()
    
    def add_rounded_corners(self, widget, radius):
        """为控件添加圆角效果"""
        # 创建画布覆盖在控件上
        canvas = tk.Canvas(widget, bg=self.colors["background"], highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=1, pady=1)
        
        # 绘制圆角矩形
        def draw_rounded_rect():
            canvas.delete("all")
            w = widget.winfo_width()
            h = widget.winfo_height()
            
            # 绘制背景
            canvas.create_rectangle(
                0, 0, w, h,
                fill=self.colors["card_bg"],
                outline=""
            )
            
            # 绘制圆角遮罩
            canvas.create_arc(0, 0, radius*2, radius*2, start=90, extent=90, fill=self.colors["background"], outline="")
            canvas.create_arc(w-radius*2, 0, w, radius*2, start=0, extent=90, fill=self.colors["background"], outline="")
            canvas.create_arc(0, h-radius*2, radius*2, h, start=180, extent=90, fill=self.colors["background"], outline="")
            canvas.create_arc(w-radius*2, h-radius*2, w, h, start=270, extent=90, fill=self.colors["background"], outline="")
        
        # 初始绘制和大小变化时重绘
        draw_rounded_rect()
        widget.bind("<Configure>", lambda e: draw_rounded_rect())
    
    def load_config(self):
        """加载上次保存的配置"""
        self.last_config = {
            "hours": 0,
            "minutes": 0,
            "seconds": 0,
            "reminder_times": "1",
            "reminder_unit": "分钟",
            "repeat_interval": 0
        }
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved_config = json.load(f)
                    self.last_config.update(saved_config)
            except:
                pass
    
    def save_config(self):
        """保存当前配置"""
        try:
            config = {
                "hours": self.hour_var.get(),
                "minutes": self.minute_var.get(),
                "seconds": self.second_var.get(),
                "reminder_times": self.reminder_time_var.get(),
                "reminder_unit": self.reminder_unit_var.get(),
                "repeat_interval": self.repeat_interval_var.get()
            }
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def parse_time_input(self):
        """解析用户输入的时间"""
        try:
            # 解析总时间
            hours = int(self.hour_var.get()) if self.hour_var.get().strip() else 0
            minutes = int(self.minute_var.get()) if self.minute_var.get().strip() else 0
            seconds = int(self.second_var.get()) if self.second_var.get().strip() else 0
            
            # 解析重复提醒间隔（分钟转秒）
            repeat_interval = float(self.repeat_interval_var.get()) if self.repeat_interval_var.get().strip() else 0
            repeat_interval_sec = int(repeat_interval * 60)
            
            # 解析自定义提醒时间
            reminder_input = self.reminder_time_var.get().strip()
            custom_reminders = []
            if reminder_input:
                reminder_list = [x.strip() for x in reminder_input.split(",") if x.strip()]
                for rem in reminder_list:
                    rem_value = float(rem)
                    if self.reminder_unit_var.get() == "分钟":
                        rem_sec = int(rem_value * 60)
                    else:
                        rem_sec = int(rem_value)
                    if rem_sec > 0:
                        custom_reminders.append(rem_sec)
            
            # 验证输入
            if hours < 0 or minutes < 0 or seconds < 0:
                messagebox.showerror("输入错误", "总时间不能为负数！")
                return None
            
            if repeat_interval < 0:
                messagebox.showerror("输入错误", "重复间隔不能为负数！")
                return None
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if total_seconds <= 0:
                messagebox.showerror("输入错误", "总时间必须大于0！")
                return None
            
            # 去重并排序（从大到小）
            custom_reminders = sorted(list(set(custom_reminders)), reverse=True)
            # 过滤掉大于总时间的提醒时间
            custom_reminders = [rem for rem in custom_reminders if rem <= total_seconds]
            
            # 保存配置
            self.save_config()
            
            return total_seconds, repeat_interval_sec, custom_reminders
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字！\n提示：多个提醒时间用逗号分隔，例如 5,1,0.5")
            return None
    
    def format_time(self, seconds):
        """将秒格式化为 HH:MM:SS 格式"""
        return str(timedelta(seconds=seconds)).zfill(8)
    
    def update_progress(self):
        """更新进度条"""
        if self.total_time > 0:
            progress = (1 - self.remaining_time / self.total_time) * 100
            self.progress_var.set(progress)
    
    def timer_loop(self):
        """计时器核心循环"""
        self.last_reminder_time = self.remaining_time
        self.triggered_reminders.clear()
        
        while self.remaining_time > 0 and self.is_running:
            # 更新显示和进度条
            self.root.after(0, self.update_display)
            self.root.after(0, self.update_progress)
            
            # 自定义提醒触发
            for rem_time in self.custom_reminder_times:
                if self.remaining_time == rem_time and rem_time not in self.triggered_reminders:
                    self.root.after(0, self.play_sound, self.warning_sound)
                    rem_text = f"剩余{rem_time//60}分{rem_time%60}秒" if rem_time >=60 else f"剩余{rem_time}秒"
                    self.root.after(0, lambda t=rem_text: self.status_label.config(
                        text=f"⏰ 提醒：{t}！", 
                        foreground=self.colors["danger"],
                        font=("微软雅黑", 11, "bold")
                    ))
                    self.triggered_reminders.add(rem_time)
            
            # 重复提醒触发
            if self.reminder_interval > 0:
                if self.last_reminder_time - self.remaining_time >= self.reminder_interval:
                    self.root.after(0, self.play_sound, self.warning_sound)
                    elapsed_min = int((self.total_time - self.remaining_time)/60)
                    self.root.after(0, lambda m=elapsed_min: self.status_label.config(
                        text=f"🔔 重复提醒：已运行 {m} 分钟", 
                        foreground=self.colors["warning"],
                        font=("微软雅黑", 11, "bold")
                    ))
                    self.last_reminder_time = self.remaining_time
            
            time.sleep(1)
            self.remaining_time -= 1
        
        # 计时结束
        if self.is_running:
            self.root.after(0, self.update_display)
            self.root.after(0, self.update_progress)
            self.root.after(0, self.play_sound, self.finish_sound)
            self.root.after(0, lambda: messagebox.showinfo("计时结束", "⏰ 设定的时间已到！"))
            self.root.after(0, self.reset_timer)
    
    def update_display(self):
        """更新时间显示"""
        self.time_display.config(text=self.format_time(self.remaining_time))
    
    def start_timer(self):
        """开始计时器"""
        if not self.is_running:
            time_data = self.parse_time_input()
            if time_data:
                self.total_time, self.reminder_interval, self.custom_reminder_times = time_data
                self.remaining_time = self.total_time
                
                self.is_running = True
                self.start_btn.config(state="disabled")
                self.pause_btn.config(state="normal")
                
                # 显示设置的提醒时间
                if self.custom_reminder_times:
                    rem_info = []
                    for rem in self.custom_reminder_times:
                        if rem >= 60:
                            rem_info.append(f"{rem//60}分{rem%60}秒" if rem%60 !=0 else f"{rem//60}分钟")
                        else:
                            rem_info.append(f"{rem}秒")
                    self.status_label.config(
                        text=f"✅ 计时器已启动 | 提醒设置：{', '.join(rem_info)}", 
                        foreground=self.colors["secondary"],
                        font=("微软雅黑", 11, "bold")
                    )
                else:
                    self.status_label.config(
                        text="✅ 计时器已启动 | 未设置提醒", 
                        foreground=self.colors["secondary"],
                        font=("微软雅黑", 11, "bold")
                    )
                
                # 启动计时器线程
                self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
                self.timer_thread.start()
    
    def pause_timer(self):
        """暂停计时器"""
        self.is_running = not self.is_running
        
        if self.is_running:
            self.pause_btn.config(text="暂停")
            self.status_label.config(
                text="▶️ 计时器继续运行", 
                foreground=self.colors["secondary"],
                font=("微软雅黑", 11, "bold")
            )
            # 重新启动线程
            self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
            self.timer_thread.start()
        else:
            self.pause_btn.config(text="继续")
            self.status_label.config(
                text="⏸️ 计时器已暂停", 
                foreground=self.colors["warning"],
                font=("微软雅黑", 11, "bold")
            )
    
    def reset_timer(self):
        """重置计时器"""
        self.is_running = False
        self.remaining_time = 0
        self.total_time = 0
        self.reminder_interval = 0
        self.custom_reminder_times = []
        self.triggered_reminders.clear()
        
        self.update_display()
        self.update_progress()
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="暂停")
        self.status_label.config(
            text="提示：可设置多个提醒时间（例：5,1,0.5 表示5分钟、1分钟、30秒时提醒）", 
            foreground=self.colors["gray"],
            font=("微软雅黑", 11)
        )
        
        # 等待线程结束
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)

def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置程序图标（可选）
    try:
        if os.path.exists("timer.ico"):
            root.iconbitmap("timer.ico")
    except:
        pass
    
    # 解决Windows高分屏模糊问题
    try:
        root.tk.call('tk', 'scaling', 1.0)
    except:
        pass
    
    app = ModernTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()