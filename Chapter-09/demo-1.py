from xml.dom import minidom

# 读取 XML 文件
doc = minidom.parse('demo-1-origin.xml')

# 定义一个函数来移除所有空白文本节点，以便于后续操作
def remove_blank_nodes(node):
    # 递归移除所有空白文本节点。
    if node.hasChildNodes():
        for child in list(node.childNodes):
            if child.nodeType == minidom.Node.TEXT_NODE and not child.data.strip():
                node.removeChild(child)
            else:
                remove_blank_nodes(child)

# 移除空白节点
remove_blank_nodes(doc)

# 找到根元素 purchaseOrder
root = doc.documentElement

# 找到 items 元素
items = root.getElementsByTagName('items')[0]

# 创建一个新的 item 元素并设置其属性
new_item = doc.createElement('item')
new_item.setAttribute('partNum', '926-AA')

# 创建并添加 productName 元素
product_name = doc.createElement('productName')
product_name.appendChild(doc.createTextNode('Baby Monitor'))
new_item.appendChild(product_name)

# 创建并添加 quantity 元素
quantity = doc.createElement('quantity')
quantity.appendChild(doc.createTextNode('1'))
new_item.appendChild(quantity)

# 创建并添加 USPrice 元素
us_price = doc.createElement('USPrice')
us_price.appendChild(doc.createTextNode('39.98'))
new_item.appendChild(us_price)

# 创建并添加 shipDate 元素
ship_date = doc.createElement('shipDate')
ship_date.appendChild(doc.createTextNode('1999-05-21'))
new_item.appendChild(ship_date)

# 将新创建的 item 元素添加到 items 元素中
items.appendChild(new_item)

# 输出修改后的 XML 结构
print(doc.toprettyxml())

# 将修改后的 XML 结构写入文件 demo-1-modified.xml
with open('demo-1-modified.xml', 'w') as f:
    f.write(doc.toprettyxml())