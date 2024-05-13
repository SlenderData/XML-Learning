import tkinter as tk
from tkinter import messagebox, simpledialog, font, filedialog, Scrollbar, Listbox, Toplevel, END
import xml.etree.ElementTree as ET
from os.path import exists
import platform
from PIL import Image, ImageOps, ImageTk
import base64
import io


def get_dpi_scale():
    if platform.system() == "Windows":
        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        dpi = user32.GetSystemMetrics(88)
        return dpi / 96  # 默认 DPI 为 96
    elif platform.system() == "Darwin":  # MacOS
        return 2  # Common scale factor for macOS (Retina display, etc.)
    else:
        return 1.5  # Default scale for other OSes like Linux


def get_scaled_font(size):
    scale = get_dpi_scale()
    return int(size * scale)


def init_xml():
    xml_file = 'contacts.xml'
    if not exists(xml_file):
        root = ET.Element('contacts')
        tree = ET.ElementTree(root)
        tree.write(xml_file)
    return xml_file


def resize_and_crop(image_path):
    image = Image.open(image_path)
    min_dim = min(image.size)
    image = ImageOps.fit(image, (min_dim, min_dim), method=Image.Resampling.LANCZOS,
                         centering=(0.5, 0.5))  # Crop the image to a square
    image = image.resize((64, 64), Image.Resampling.LANCZOS)  # Resize to 64x64 using high quality downscaling
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    photo_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return photo_base64


def display_photo(base64_string):
    if base64_string:
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        return ImageTk.PhotoImage(image)
    else:
        return None


def add_contact():
    def save_contact():
        name = name_entry.get()
        phone = phone_entry.get()
        photo_data = resize_and_crop(image_path.get()) if image_path.get() else ""
        if name and phone:
            contact = ET.Element('contact')
            ET.SubElement(contact, 'name').text = name
            ET.SubElement(contact, 'phone').text = phone
            if photo_data:
                ET.SubElement(contact, 'photo').text = photo_data
            root.append(contact)
            tree.write(xml_file)
            add_win.destroy()
            messagebox.showinfo("成功", "联系人已添加")
        else:
            messagebox.showerror("错误", "姓名和电话不能为空")

    def open_file_dialog():
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            image_path.set(filepath)

    add_win = Toplevel(main)
    add_win.title("添加联系人")
    image_path = tk.StringVar()

    tk.Label(add_win, text="姓名:", font=normal_font).grid(row=0, column=0)
    name_entry = tk.Entry(add_win, font=normal_font)
    name_entry.grid(row=0, column=1)

    tk.Label(add_win, text="电话:", font=normal_font).grid(row=1, column=0)
    phone_entry = tk.Entry(add_win, font=normal_font)
    phone_entry.grid(row=1, column=1)

    tk.Button(add_win, text="选择头像", font=normal_font, command=open_file_dialog).grid(row=2, column=0)
    tk.Button(add_win, text="保存", font=large_font, command=save_contact).grid(row=3, columnspan=2)


def delete_contact():
    name = simpledialog.askstring("删除联系人", "输入要删除的联系人姓名:", parent=main)
    if name:
        for contact in root.findall('contact'):
            if contact.find('name').text == name:
                root.remove(contact)
                tree.write(xml_file)
                messagebox.showinfo("成功", "联系人已删除")
                return
        messagebox.showerror("失败", "找不到该联系人")


def edit_contact():
    name = simpledialog.askstring("编辑联系人", "输入要编辑的联系人姓名:", parent=main)
    if name:
        for contact in root.findall('contact'):
            if contact.find('name').text == name:
                new_phone = simpledialog.askstring("编辑电话", "输入新的电话号码:", parent=main)
                if new_phone:
                    contact.find('phone').text = new_phone
                    tree.write(xml_file)
                    messagebox.showinfo("成功", "联系人电话已更新")
                return
        messagebox.showerror("失败", "找不到该联系人")


def login(username, password):
    if username == "1" and password == "1":
        main_window()
    else:
        messagebox.showerror("登录失败", "用户名或密码错误")


def view_all_contacts():
    global photo_images  # 用于存储所有的图片对象
    photo_images = []

    view_win = Toplevel(main)
    view_win.title("所有联系人")
    scroll = Scrollbar(view_win)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = Listbox(view_win, yscrollcommand=scroll.set, font=normal_font, width=50)
    for contact in root.findall('contact'):
        name = contact.find('name').text
        phone = contact.find('phone').text
        photo_base64 = contact.find('photo').text if contact.find('photo') is not None else None
        photo_image = display_photo(photo_base64)
        listbox.insert(END, f"姓名: {name}, 电话: {phone}")
        if photo_image:
            photo_images.append(photo_image)  # 保存图片对象的引用
            tk.Label(view_win, image=photo_image).pack()  # 显示头像
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll.config(command=listbox.yview)


def find_contact():
    global photo_image  # 用于存储当前查找的联系人图片对象
    name = simpledialog.askstring("查找联系人", "请输入联系人姓名:", parent=main)
    if name:
        for contact in root.findall('contact'):
            if contact.find('name').text == name:
                phone = contact.find('phone').text
                photo_base64 = contact.find('photo').text if contact.find('photo') is not None else None
                photo_image = display_photo(photo_base64)
                info = f"姓名: {name}\n电话: {phone}"
                messagebox.showinfo("联系人信息", info)
                if photo_image:
                    photo_win = Toplevel(main)
                    photo_win.title("联系人头像")
                    tk.Label(photo_win, image=photo_image).pack()
                    return
        messagebox.showerror("查找失败", "找不到该联系人")
    else:
        messagebox.showerror("查找失败", "输入不能为空")


def main_window():
    global main, normal_font, large_font, root, tree, xml_file
    main = tk.Toplevel()
    main.title("通信录管理系统")
    main.geometry('400x300')

    normal_font = font.Font(size=get_scaled_font(12))
    large_font = font.Font(size=get_scaled_font(14))

    tk.Button(main, text="添加联系人", font=large_font, command=add_contact, height=2, width=20).grid(row=0, column=0,
                                                                                                      sticky="ew")
    tk.Button(main, text="删除联系人", font=large_font, command=delete_contact, height=2, width=20).grid(row=1,
                                                                                                         column=0,
                                                                                                         sticky="ew")
    tk.Button(main, text="编辑联系人", font=large_font, command=edit_contact, height=2, width=20).grid(row=2, column=0,
                                                                                                       sticky="ew")
    tk.Button(main, text="查找联系人", font=large_font, command=find_contact, height=2, width=20).grid(row=3, column=0,
                                                                                                       sticky="ew")
    tk.Button(main, text="查看所有联系人", font=large_font, command=view_all_contacts, height=2, width=20).grid(row=4,
                                                                                                                column=0,
                                                                                                                sticky="ew")

    xml_file = init_xml()
    tree = ET.parse(xml_file)
    root = tree.getroot()


def start_app():
    global normal_font, large_font
    root = tk.Tk()
    root.title("用户登录")
    root.geometry('300x200')

    normal_font = font.Font(size=get_scaled_font(12))
    large_font = font.Font(size=get_scaled_font(14))

    tk.Label(root, text="用户名:", font=normal_font).grid(row=0, column=0)
    username_entry = tk.Entry(root, font=normal_font)
    username_entry.grid(row=0, column=1)

    tk.Label(root, text="密码:", font=normal_font).grid(row=1, column=0)
    password_entry = tk.Entry(root, show='*', font=normal_font)
    password_entry.grid(row=1, column=1)

    tk.Button(root, text="登录", font=large_font, command=lambda: login(username_entry.get(), password_entry.get()),
              height=2, width=10).grid(row=2, columnspan=2)

    root.mainloop()


start_app()
