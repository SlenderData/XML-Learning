from faker import Faker
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

# 创建 Faker 实例，指定中文环境
fake = Faker(locale='zh_CN')

# 创建一个 XML 的根元素
employees = ET.Element('employees')

# 生成10个员工的信息
for i in range(10):
    # 随机生成性别
    sex = fake.random_element(("女", "男"))
    # 根据性别生成相应的名字
    if sex == '男':
        name = fake.name_male()
    else:
        name = fake.name_female()

    employee = ET.SubElement(employees, 'employee', id=str(i + 1))
    ET.SubElement(employee, 'name').text = name
    ET.SubElement(employee, 'age').text = str(fake.random_int(min=20, max=28))
    ET.SubElement(employee, 'sex').text = sex
    ET.SubElement(employee, 'address').text = fake.address()

# 将生成的XML转换为字符串
xml_bytes = ET.tostring(employees, encoding='utf-8', method='xml')

# 使用minidom解析字符串
dom = parseString(xml_bytes)

# 使用minidom的toprettyxml方法格式化输出，缩进使用4个空格，并指定编码为utf-8
pretty_xml_as_string = dom.toprettyxml(indent="    ", encoding="utf-8")

# 打印格式化后的字符串
# 注意：由于现在pretty_xml_as_string是字节串，如果想打印出来，需要先解码
print(pretty_xml_as_string.decode('utf-8'))

# 将格式化后的XML字符串写入文件
with open('demo-2.xml', 'wb') as f:
    f.write(pretty_xml_as_string)
