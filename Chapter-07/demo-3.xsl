<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
                <title>图书信息</title>
            </head>
            <body>
                <h1>图书信息</h1>
                <table border="1">
                    <tr>
                        <th>id</th>
                        <th>图书标题</th>
                        <th>作者</th>
                        <th>出版社</th>
                        <th>ISBN</th>
                    </tr>
                    <xsl:for-each select="//book">
                        <tr>
                            <td>
                                <xsl:value-of select="@id"/>
                            </td>
                            <td>
                                <xsl:value-of select="title"/>
                            </td>
                            <td>
                                <xsl:value-of select="author"/>
                            </td>
                            <td>
                                <xsl:value-of select="publisher"/>
                            </td>
                            <td>
                                <xsl:value-of select="isbn"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>