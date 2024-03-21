<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
                <title>Orders</title>
            </head>
            <body>
                <h2>Orders</h2>
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
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>