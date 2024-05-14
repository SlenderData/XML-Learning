import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from contact import ContactManager
from user import UserManager
import base64
import io

class ContactManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("通讯录管理系统")
        self.geometry("600x400")  # 增加窗口宽度以适应三列布局

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

        self.save_button = tk.Button(self, text="保存", command=self.save_contact)
        self.save_button.pack()

        self.back_button = tk.Button(self, text="返回", command=self.create_main_widgets)
        self.back_button.pack()

    def browse_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png")])
        self.photo_path.set(file_path)

    def save_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        photo = self.photo_path.get() if self.photo_path.get() else None
        self.contact_manager.add_contact(self.current_user, name, phone, photo)
        messagebox.showinfo("成功", "联系人添加成功")
        self.create_main_widgets()

    def view_contacts(self):
        self.clear_widgets()

        contacts = self.contact_manager.get_contacts(self.current_user)
        for i, contact in enumerate(contacts):
            contact_frame = tk.Frame(self)
            contact_frame.pack(fill=tk.X, padx=10, pady=5)

            if contact['photo']:
                img_data = base64.b64decode(contact['photo'])
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((50, 50))
                img_tk = ImageTk.PhotoImage(img)
                photo_label = tk.Label(contact_frame, image=img_tk)
                photo_label.image = img_tk
            else:
                photo_label = tk.Label(contact_frame, text="无照片")

            photo_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

            name_label = tk.Label(contact_frame, text=contact['name'])
            name_label.grid(row=i, column=1, padx=10, pady=5, sticky='w')

            phone_label = tk.Label(contact_frame, text=contact['phone'])
            phone_label.grid(row=i, column=2, padx=10, pady=5, sticky='w')

            edit_button = tk.Button(contact_frame, text="编辑", command=lambda c=contact: self.edit_contact(c))
            edit_button.grid(row=i, column=3, padx=10, pady=5, sticky='e')

            delete_button = tk.Button(contact_frame, text="删除", command=lambda c=contact: self.delete_contact(c))
            delete_button.grid(row=i, column=4, padx=10, pady=5, sticky='e')

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

        self.save_button = tk.Button(self, text="保存", command=lambda: self.save_edited_contact(contact['id']))
        self.save_button.pack()

        self.back_button = tk.Button(self, text="返回", command=self.view_contacts)
        self.back_button.pack()

    def save_edited_contact(self, contact_id):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        photo = self.photo_path.get() if self.photo_path.get() else None
        self.contact_manager.update_contact(contact_id, name, phone, photo)
        messagebox.showinfo("成功", "联系人信息更新成功")
        self.view_contacts()

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
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        for i, contact in enumerate(contacts):
            contact_frame = tk.Frame(self)
            contact_frame.pack(fill=tk.X, padx=10, pady=5)

            if contact['photo']:
                img_data = base64.b64decode(contact['photo'])
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((50, 50))
                img_tk = ImageTk.PhotoImage(img)
                photo_label = tk.Label(contact_frame, image=img_tk)
                photo_label.image = img_tk
            else:
                photo_label = tk.Label(contact_frame, text="无照片")

            photo_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

            name_label = tk.Label(contact_frame, text=contact['name'])
            name_label.grid(row=i, column=1, padx=10, pady=5, sticky='w')

            phone_label = tk.Label(contact_frame, text=contact['phone'])
            phone_label.grid(row=i, column=2, padx=10, pady=5, sticky='w')

            edit_button = tk.Button(contact_frame, text="编辑", command=lambda c=contact: self.edit_contact(c))
            edit_button.grid(row=i, column=3, padx=10, pady=5, sticky='e')

            delete_button = tk.Button(contact_frame, text="删除", command=lambda c=contact: self.delete_contact(c))
            delete_button.grid(row=i, column=4, padx=10, pady=5, sticky='e')

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
