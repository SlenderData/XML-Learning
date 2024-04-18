import xml.sax

class PurchaseOrderHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.item = None
        self.elements = {}

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        print(f"元素 {tag} 开始")
        if tag == "item":
            self.item = {'partNum': attributes['partNum']}
            print("item 元素的 partNum 属性值为:", self.item['partNum'])


    # 元素结束事件处理
    def endElement(self, tag):
        print(f"元素 {tag} 结束")

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData and content.strip():  # 避免空白字符触发
            print(f"元素 {self.CurrentData} 内的值为: {content.strip()}")
            if self.item is not None:
                self.item[self.CurrentData] = content.strip()

# 创建一个 XMLReader
parser = xml.sax.make_parser()

# 关闭命名空间
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# 重写 ContextHandler
Handler = PurchaseOrderHandler()
parser.setContentHandler(Handler)

# 读取并处理 XML 文件
parser.parse('demo-1-origin.xml')
