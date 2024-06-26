import tkinter as tk
from tkinter import messagebox, filedialog, font
from PIL import Image, ImageTk
from contact import ContactManager
from user import UserManager
from utils import fetch_random_photo
import base64
import io
from faker import Faker

fake = Faker(locale='zh_CN')

class ContactManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("通讯录管理系统")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.resizable(True, True)  # 允许用户调整窗口大小

        # 设置全局字体大小
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        self.option_add("*Font", default_font)

        self.user_manager = UserManager()
        self.contact_manager = ContactManager()

        self.current_user = None

        self.create_login_widgets()

    def create_login_widgets(self):
        self.clear_widgets()

        self.username_label = tk.Label(self, text="用户名")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="密码")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="登录", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self, text="注册", command=self.register)
        self.register_button.pack()

    def create_main_widgets(self):
        self.clear_widgets()

        self.add_contact_button = tk.Button(self, text="添加联系人", command=self.add_contact)
        self.add_contact_button.pack()

        self.view_contacts_button = tk.Button(self, text="查看联系人", command=self.view_contacts)
        self.view_contacts_button.pack()

        self.search_contacts_button = tk.Button(self, text="查找联系人", command=self.search_contacts)
        self.search_contacts_button.pack()

        self.logout_button = tk.Button(self, text="注销", command=self.logout)
        self.logout_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.validate_user(username, password):
            self.current_user = username
            self.create_main_widgets()
        else:
            messagebox.showerror("错误", "用户名或密码无效")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.add_user(username, password):
            messagebox.showinfo("成功", "用户注册成功")
        else:
            messagebox.showerror("错误", "用户名已存在")

    def logout(self):
        self.current_user = None
        self.create_login_widgets()

    def add_contact(self):
        self.clear_widgets()

        self.name_label = tk.Label(self, text="姓名")
        self.name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.phone_label = tk.Label(self, text="电话")
        self.phone_label.pack()

        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        self.photo_label = tk.Label(self, text="照片")
        self.photo_label.pack()

        self.photo_path = tk.StringVar()
        self.photo_entry = tk.Entry(self, textvariable=self.photo_path)
        self.photo_entry.pack()

        self.photo_button = tk.Button(self, text="浏览", command=self.browse_photo)
        self.photo_button.pack()

        self.random_button = tk.Button(self, text="随机生成", command=self.generate_random_contact)
        self.random_button.pack()

        self.save_button = tk.Button(self, text="保存", command=self.save_contact)
        self.save_button.pack()

        self.back_button = tk.Button(self, text="返回", command=self.create_main_widgets)
        self.back_button.pack()

    def browse_photo(self):
        self.after(100, self.open_file_dialog)

    def open_file_dialog(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg"), ("PNG files", "*.png")])
            if file_path:
                self.photo_path.set(file_path)
            else:
                print("No file selected")
        except Exception as e:
            print(f"Error selecting file: {e}")

    def generate_random_contact(self):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, fake.name())

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, fake.phone_number())

        try:
            photo_path = fetch_random_photo()
            self.photo_path.set(photo_path)
        except Exception as e:
            print(f"Error fetching random photo: {e}")
            messagebox.showerror("错误", "无法获取随机照片")

    def save_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        photo = self.photo_path.get() if self.photo_path.get() else None
        try:
            self.contact_manager.add_contact(self.current_user, name, phone, photo)
            messagebox.showinfo("成功", "联系人添加成功")
            self.create_main_widgets()
        except FileNotFoundError as fnf_error:
            print(f"FileNotFoundError: {fnf_error}")
            messagebox.showerror("错误", "文件未找到，请选择有效的图片文件")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("错误", "添加联系人时发生错误")

    def view_contacts(self):
        self.clear_widgets()

        # 创建一个Frame容器以包含Canvas和滚动条
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        # 创建一个Canvas以在其上绘制联系人信息
        canvas = tk.Canvas(container)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建滚动条并将其配置为滚动Canvas
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # 创建一个Frame作为Canvas的内容
        contact_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=contact_frame, anchor="nw")

        contacts = self.contact_manager.get_contacts(self.current_user)
        self.populate_contacts(contact_frame, contacts)
        contact_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        self.back_button = tk.Button(self, text="返回", command=self.create_main_widgets)
        self.back_button.pack(pady=10)

    def edit_contact(self, contact):
        self.clear_widgets()

        self.name_label = tk.Label(self, text="姓名")
        self.name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, contact['name'])
        self.name_entry.pack()

        self.phone_label = tk.Label(self, text="电话")
        self.phone_label.pack()

        self.phone_entry = tk.Entry(self)
        self.phone_entry.insert(0, contact['phone'])
        self.phone_entry.pack()

        self.photo_label = tk.Label(self, text="照片")
        self.photo_label.pack()

        self.photo_path = tk.StringVar()
        self.photo_entry = tk.Entry(self, textvariable=self.photo_path)
        self.photo_entry.pack()

        self.photo_button = tk.Button(self, text="浏览", command=self.browse_photo)
        self.photo_button.pack()

        self.save_button = tk.Button(self, text="保存", command=lambda: self.update_contact(contact['id']))
        self.save_button.pack()

        self.back_button = tk.Button(self, text="返回", command=self.create_main_widgets)
        self.back_button.pack()

    def update_contact(self, contact_id):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        photo = self.photo_path.get() if self.photo_path.get() else None
        try:
            self.contact_manager.update_contact(contact_id, name, phone, photo)
            messagebox.showinfo("成功", "联系人信息更新成功")
            self.view_contacts()
        except FileNotFoundError as fnf_error:
            print(f"FileNotFoundError: {fnf_error}")
            messagebox.showerror("错误", "文件未找到，请选择有效的图片文件")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("错误", "更新联系人时发生错误")

    def delete_contact(self, contact):
        self.contact_manager.delete_contact(contact['id'])
        messagebox.showinfo("成功", "联系人删除成功")
        self.view_contacts()

    def search_contacts(self):
        self.clear_widgets()

        self.search_label = tk.Label(self, text="查找联系人")
        self.search_label.pack()

        self.keyword_entry = tk.Entry(self)
        self.keyword_entry.pack()

        self.search_button = tk.Button(self, text="查找", command=self.perform_search)
        self.search_button.pack()

        self.back_button = tk.Button(self, text="返回", command=self.create_main_widgets)
        self.back_button.pack()

    def perform_search(self):
        keyword = self.keyword_entry.get()
        contacts = self.contact_manager.search_contacts(self.current_user, keyword)
        self.display_contacts(contacts)

    def display_contacts(self, contacts):
        self.clear_widgets()

        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        contact_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=contact_frame, anchor="nw")

        self.populate_contacts(contact_frame, contacts)
        contact_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        self.back_button = tk.Button(self, text="返回", command=self.create_main_widgets)
        self.back_button.pack(pady=10)

    def populate_contacts(self, parent_frame, contacts):
        for i, contact in enumerate(contacts):
            row_frame = tk.Frame(parent_frame)
            row_frame.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            if contact['photo']:
                img_data = base64.b64decode(contact['photo'])
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((50, 50))
                img_tk = ImageTk.PhotoImage(img)
                photo_label = tk.Label(row_frame, image=img_tk)
                photo_label.image = img_tk
            else:
                photo_label = tk.Label(row_frame, text="无照片")

            photo_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

            name_label = tk.Label(row_frame, text=contact['name'])
            name_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')

            phone_label = tk.Label(row_frame, text=contact['phone'])
            phone_label.grid(row=0, column=2, padx=10, pady=5, sticky='w')

            edit_button = tk.Button(row_frame, text="编辑", command=lambda c=contact: self.edit_contact(c))
            edit_button.grid(row=0, column=3, padx=10, pady=5, sticky='e')

            delete_button = tk.Button(row_frame, text="删除", command=lambda c=contact: self.delete_contact(c))
            delete_button.grid(row=0, column=4, padx=10, pady=5, sticky='e')

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
