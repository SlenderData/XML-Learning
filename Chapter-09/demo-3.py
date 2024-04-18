# 我在第 2 章就完成了符合要求的 python 实现，这里直接复制过来了，做了简单优化
# 这里的代码生成了一个包含 10 个员工信息的 XML 文件

from faker import Faker
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

# 创建 Faker 实例，指定中文环境
fake = Faker(locale='zh_CN')

# 创建一个 XML 的根元素
course = ET.Element('course')

# 生成10个学生成绩的信息
for i in range(10):
    student = ET.SubElement(course, 'student', number=str(i + 1))
    ET.SubElement(student, 'name').text = fake.name()
    ET.SubElement(student, 'score').text = str(fake.random_int(min=50, max=100))

# 将生成的XML转换为字节串
xml_bytes = ET.tostring(course, encoding='utf-8', method='xml')

# 使用minidom解析字符串
dom = parseString(xml_bytes)

# 打印格式化后的字符串
print(dom.toprettyxml())

# 将格式化后的XML字符串写入文件
with open('demo-3.xml', 'wb') as f:
    f.write(dom.toprettyxml().encode('utf-8'))