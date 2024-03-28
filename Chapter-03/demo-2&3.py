from faker import Faker
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

# 初始化Faker，设置为中文环境
fake = Faker('zh_CN')

# 创建XML根元素
root = ET.Element("NEWSPAPER")

# 生成10个不同的ARTICLE实例
for _ in range(10):
    author_name = fake.name()  # 先生成作者名
    article = ET.SubElement(root, "ARTICLE", {
        "AUTHOR": author_name,
        "EDITOR": fake.name(),
        "DATE": fake.date(),
        "EDITION": fake.random_element(elements=('Morning', 'Evening'))  # 表示早报或晚报
    })

    # 为每个ARTICLE添加子元素并填充内容
    ET.SubElement(article, "HEADLINE").text = fake.sentence(nb_words=6)
    ET.SubElement(article, "BYLINE").text = f"{author_name}, {fake.job()}"
    ET.SubElement(article, "LEAD").text = fake.paragraph(nb_sentences=3)
    ET.SubElement(article, "BODY").text = fake.text(max_nb_chars=50)
    ET.SubElement(article, "NOTES").text = "&COPYRIGHT; " + fake.text(max_nb_chars=50)

# 将生成的XML转换为字符串
xml_bytes = ET.tostring(root, encoding='utf-8', method='xml')

# 构造XML声明和DTD引用
dtd_declaration = f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE NEWSPAPER SYSTEM "demo-2.dtd">\n'

# 解码XML内容为字符串并在前面加上DTD声明
xml_content_with_dtd = dtd_declaration + xml_bytes.decode('utf-8')

# 使用minidom解析字符串
dom = parseString(xml_content_with_dtd)

# 使用minidom的toprettyxml方法格式化输出，缩进使用4个空格，并指定编码为utf-8
pretty_xml_as_string = dom.toprettyxml(indent="    ", encoding="utf-8")

# 生成的pretty_xml_as_string是经过格式化的XML字符串
# 使用replace方法确保DOCTYPE中的SYSTEM identifier使用双引号
pretty_xml_as_string = pretty_xml_as_string.decode('utf-8').replace("\n  SYSTEM 'demo-2.dtd'", ' SYSTEM "demo-2.dtd"')

# 使用replace方法确保被转义的字符被正确还原
pretty_xml_as_string = pretty_xml_as_string.replace("&amp;", "&")

# 打印和保存格式化后的XML
print(pretty_xml_as_string)

with open('demo-2.xml', 'wb') as f:
    f.write(pretty_xml_as_string.encode('utf-8'))

# 完成第 3 题

# 读取demo-2.dtd的内容
with open('demo-2.dtd', 'r', encoding='utf-8') as dtd_file:
    dtd_content = dtd_file.read()

# 构造带有内部DTD的XML声明
xml_content_with_internal_dtd = pretty_xml_as_string
xml_content_with_internal_dtd = xml_content_with_internal_dtd.replace('<!DOCTYPE NEWSPAPER SYSTEM "demo-2.dtd">', f'{dtd_content}')

# 保存带有内部DTD的XML文件
with open('demo-3.xml', 'wb') as f:
    f.write(xml_content_with_internal_dtd.encode('utf-8'))
