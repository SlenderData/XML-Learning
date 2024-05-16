import xml.etree.ElementTree as ET
import uuid
from utils import save_xml_tree, encode_photo_to_base64

class ContactManager:
    def __init__(self):
        self.file = 'contacts.xml'
        self.tree = ET.parse(self.file)
        self.root = self.tree.getroot()

    def add_contact(self, username, name, phone, photo=None):
        contact_id = str(uuid.uuid4())
        contact_element = ET.Element("contact", id=contact_id)
        name_element = ET.SubElement(contact_element, "name")
        name_element.text = name
        phone_element = ET.SubElement(contact_element, "phone")
        phone_element.text = phone

        if photo:
            encoded_photo = encode_photo_to_base64(photo)
            photo_element = ET.SubElement(contact_element, "photo")
            photo_element.text = encoded_photo

        self.root.append(contact_element)
        save_xml_tree(self.tree, self.file)

        user_tree = ET.parse('users.xml')
        user_root = user_tree.getroot()
        user = user_root.find(f".//user[username='{username}']")
        if user is not None:
            contacts_element = user.find("contacts")
            if contacts_element is None:
                contacts_element = ET.SubElement(user, "contacts")
            ET.SubElement(contacts_element, "contact", id=contact_id)
            save_xml_tree(user_tree, 'users.xml')

    def get_contacts(self, username):
        user_tree = ET.parse('users.xml')
        user_root = user_tree.getroot()
        user = user_root.find(f".//user[username='{username}']")
        contact_ids = []
        if user is not None:
            contact_ids = [contact.get("id") for contact in user.find("contacts")]

        contacts = []
        for contact_element in self.root.findall("contact"):
            if contact_element.get("id") in contact_ids:
                contact = {
                    "id": contact_element.get("id"),
                    "name": contact_element.find("name").text,
                    "phone": contact_element.find("phone").text,
                    "photo": contact_element.find("photo").text if contact_element.find("photo") is not None else None
                }
                contacts.append(contact)

        return contacts

    def update_contact(self, contact_id, name, phone, photo=None):
        contact_element = self.root.find(f".//contact[@id='{contact_id}']")
        if contact_element is not None:
            contact_element.find("name").text = name
            contact_element.find("phone").text = phone

            if photo:
                encoded_photo = encode_photo_to_base64(photo)
                photo_element = contact_element.find("photo")
                if photo_element is None:
                    photo_element = ET.SubElement(contact_element, "photo")
                photo_element.text = encoded_photo

            save_xml_tree(self.tree, self.file)

    def delete_contact(self, contact_id):
        contact_element = self.root.find(f".//contact[@id='{contact_id}']")
        if contact_element is not None:
            self.root.remove(contact_element)
            save_xml_tree(self.tree, self.file)

        user_tree = ET.parse('users.xml')
        user_root = user_tree.getroot()
        for user in user_root.findall("user"):
            contacts_element = user.find("contacts")
            if contacts_element is not None:
                contact_to_remove = contacts_element.find(f"contact[@id='{contact_id}']")
                if contact_to_remove is not None:
                    contacts_element.remove(contact_to_remove)
                    save_xml_tree(user_tree, 'users.xml')

    def search_contacts(self, username, keyword):
        user_tree = ET.parse('users.xml')
        user_root = user_tree.getroot()
        user = user_root.find(f".//user[username='{username}']")
        contact_ids = []
        if user is not None:
            contact_ids = [contact.get("id") for contact in user.find("contacts")]

        contacts = []
        for contact_element in self.root.findall("contact"):
            if contact_element.get("id") in contact_ids:
                if keyword.lower() in contact_element.find("name").text.lower() or keyword.lower() in contact_element.find("phone").text.lower():
                    contact = {
                        "id": contact_element.get("id"),
                        "name": contact_element.find("name").text,
                        "phone": contact_element.find("phone").text,
                        "photo": contact_element.find("photo").text if contact_element.find("photo") is not None else None
                    }
                    contacts.append(contact)

        return contacts
