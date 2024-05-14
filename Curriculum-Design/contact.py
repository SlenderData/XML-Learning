import xml.etree.ElementTree as ET
import os
import uuid
from utils import save_xml_tree, encode_photo_to_base64
from user import UserManager

class ContactManager:
    def __init__(self):
        self.file = "contacts.xml"
        if not os.path.exists(self.file):
            self.create_default_contact_file()
        self.tree = ET.parse(self.file)
        self.root = self.tree.getroot()

    def create_default_contact_file(self):
        root = ET.Element("contacts")
        tree = ET.ElementTree(root)
        save_xml_tree(tree, self.file)

    def add_contact(self, username, name, phone, photo=None):
        contact_id = str(uuid.uuid4())  # 使用UUID生成唯一的联系人ID
        contact = ET.SubElement(self.root, 'contact', id=contact_id)
        ET.SubElement(contact, 'name').text = name
        ET.SubElement(contact, 'phone').text = phone
        if photo:
            encoded_photo = encode_photo_to_base64(photo)
            ET.SubElement(contact, 'photo').text = encoded_photo
        self.save()

        user_manager = UserManager()
        user = user_manager.get_user(username)
        contacts_element = user.find('contacts')
        if contacts_element is None:
            contacts_element = ET.SubElement(user, 'contacts')
        ET.SubElement(contacts_element, 'contact', id=contact_id)
        user_manager.save()

    def get_contacts(self, username):
        user_manager = UserManager()
        if username == "root":
            contacts = []
            for contact in self.root.findall('contact'):
                contacts.append({
                    'id': contact.get('id'),
                    'name': contact.find('name').text,
                    'phone': contact.find('phone').text,
                    'photo': contact.find('photo').text if contact.find('photo') is not None else None
                })
            return contacts

        user = user_manager.get_user(username)
        contact_elements = user.find('contacts').findall('contact')
        contact_ids = [c.get('id') for c in contact_elements]
        contacts = []
        for contact_id in contact_ids:
            contact = self.root.find(f"./contact[@id='{contact_id}']")
            if contact is not None:
                contacts.append({
                    'id': contact_id,
                    'name': contact.find('name').text,
                    'phone': contact.find('phone').text,
                    'photo': contact.find('photo').text if contact.find('photo') is not None else None
                })
        return contacts

    def update_contact(self, contact_id, name, phone, photo=None):
        contact = self.root.find(f"./contact[@id='{contact_id}']")
        if contact is not None:
            contact.find('name').text = name
            contact.find('phone').text = phone
            if photo:
                encoded_photo = encode_photo_to_base64(photo)
                if contact.find('photo') is not None:
                    contact.find('photo').text = encoded_photo
                else:
                    ET.SubElement(contact, 'photo').text = encoded_photo
            self.save()

    def delete_contact(self, contact_id):
        contact = self.root.find(f"./contact[@id='{contact_id}']")
        if contact is not None:
            self.root.remove(contact)
            self.save()
            user_manager = UserManager()
            for user in user_manager.root.findall('user'):
                contacts_element = user.find('contacts')
                if contacts_element:
                    contact_to_remove = contacts_element.find(f"./contact[@id='{contact_id}']")
                    if contact_to_remove is not None:
                        contacts_element.remove(contact_to_remove)
            user_manager.save()

    def search_contacts(self, username, keyword):
        user_manager = UserManager()
        if username == "root":
            contacts = []
            for contact in self.root.findall('contact'):
                name = contact.find('name').text
                phone = contact.find('phone').text
                if keyword.lower() in name.lower() or keyword.lower() in phone.lower():
                    contacts.append({
                        'id': contact.get('id'),
                        'name': name,
                        'phone': phone,
                        'photo': contact.find('photo').text if contact.find('photo') is not None else None
                    })
            return contacts

        user = user_manager.get_user(username)
        contact_elements = user.find('contacts').findall('contact')
        contact_ids = [c.get('id') for c in contact_elements]
        contacts = []
        for contact_id in contact_ids:
            contact = self.root.find(f"./contact[@id='{contact_id}']")
            if contact is not None:
                name = contact.find('name').text
                phone = contact.find('phone').text
                if keyword.lower() in name.lower() or keyword.lower() in phone.lower():
                    contacts.append({
                        'id': contact_id,
                        'name': name,
                        'phone': phone,
                        'photo': contact.find('photo').text if contact.find('photo') is not None else None
                    })
        return contacts

    def save(self):
        save_xml_tree(self.tree, self.file)
