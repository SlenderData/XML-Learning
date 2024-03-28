<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
                <title>订单信息</title>
            </head>
            <body>
                <h1>订单信息</h1>
                <h2>1. 以表格的形式显示 XML 文档中存储的所有数据。</h2>
                <table border="1">
                    <tr>
                        <th>订单ID</th>
                        <th>订单日期</th>
                        <th>名称</th>
                        <th>数量</th>
                        <th>城市</th>
                        <th>邮编</th>
                    </tr>
                    <xsl:for-each select="Orders/Order">
                        <tr>
                            <td>
                                <xsl:value-of select="@orderID"/>
                            </td>
                            <td>
                                <xsl:value-of select="@orderDate"/>
                            </td>
                            <td>
                                <xsl:value-of select="name"/>
                            </td>
                            <td>
                                <xsl:value-of select="number"/>
                            </td>
                            <td>
                                <xsl:value-of select="city"/>
                            </td>
                            <td>
                                <xsl:value-of select="zip"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
                <h2>2. 显示 orderID 为 `A002` 的订单信息。</h2>
                <table border="1">
                    <tr>
                        <th>订单ID</th>
                        <th>订单日期</th>
                        <th>名称</th>
                        <th>数量</th>
                        <th>城市</th>
                        <th>邮编</th>
                    </tr>
                    <xsl:for-each select="Orders/Order">
                        <xsl:if test="@orderID='A002'">
                            <tr>
                                <td>
                                    <xsl:value-of select="@orderID"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@orderDate"/>
                                </td>
                                <td>
                                    <xsl:value-of select="name"/>
                                </td>
                                <td>
                                    <xsl:value-of select="number"/>
                                </td>
                                <td>
                                    <xsl:value-of select="city"/>
                                </td>
                                <td>
                                    <xsl:value-of select="zip"/>
                                </td>
                            </tr>
                        </xsl:if>
                    </xsl:for-each>
                </table>
                <h2>3. 显示北京的订单信息。</h2>
                <table border="1">
                    <tr>
                        <th>订单ID</th>
                        <th>订单日期</th>
                        <th>名称</th>
                        <th>数量</th>
                        <th>城市</th>
                        <th>邮编</th>
                    </tr>
                    <xsl:for-each select="Orders/Order">
                        <xsl:if test="city='北京'">
                            <tr>
                                <td>
                                    <xsl:value-of select="@orderID"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@orderDate"/>
                                </td>
                                <td>
                                    <xsl:value-of select="name"/>
                                </td>
                                <td>
                                    <xsl:value-of select="number"/>
                                </td>
                                <td>
                                    <xsl:value-of select="city"/>
                                </td>
                                <td>
                                    <xsl:value-of select="zip"/>
                                </td>
                            </tr>
                        </xsl:if>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>