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

# 将生成的XML转换为字符串
xml_bytes = ET.tostring(course, encoding='utf-8', method='xml')

# 使用minidom解析字符串
dom = parseString(xml_bytes)

# 使用minidom的toprettyxml方法格式化输出，缩进使用4个空格，并指定编码为utf-8
pretty_xml_as_string = dom.toprettyxml(indent="    ", encoding="utf-8")

# 打印格式化后的字符串
# 注意：由于现在pretty_xml_as_string是字节串，如果想打印出来，需要先解码
print(pretty_xml_as_string.decode('utf-8'))

# 将格式化后的XML字符串写入文件
with open('demo-3.xml', 'wb') as f:
    f.write(pretty_xml_as_string)