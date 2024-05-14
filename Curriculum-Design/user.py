import xml.etree.ElementTree as ET
import os
from utils import save_xml_tree

class UserManager:
    def __init__(self):
        self.file = "users.xml"
        if not os.path.exists(self.file):
            self.create_default_user_file()
        self.tree = ET.parse(self.file)
        self.root = self.tree.getroot()

    def create_default_user_file(self):
        root = ET.Element("users")
        user = ET.SubElement(root, "user")
        ET.SubElement(user, "username").text = "root"
        ET.SubElement(user, "password").text = "root"
        ET.SubElement(user, "contacts").text = ""
        tree = ET.ElementTree(root)
        save_xml_tree(tree, self.file)

    def add_user(self, username, password):
        if self.get_user(username) is not None:
            return False
        user = ET.SubElement(self.root, "user")
        ET.SubElement(user, "username").text = username
        ET.SubElement(user, "password").text = password
        ET.SubElement(user, "contacts").text = ""
        self.save()
        return True

    def validate_user(self, username, password):
        user = self.get_user(username)
        if user is not None and user.find("password").text == password:
            return True
        return False

    def get_user(self, username):
        for user in self.root.findall("user"):
            if user.find("username").text == username:
                return user
        return None

    def save(self):
        save_xml_tree(self.tree, self.file)
