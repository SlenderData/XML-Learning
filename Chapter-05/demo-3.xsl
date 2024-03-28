<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
                <title>产品信息</title>
            </head>
            <body>
                <xsl:for-each select="PRODUCTDATA/PRODUCT">
                    <div style="margin: 20px; color: green; font-size: 1.2em;">
                        <div style="color: red; font-size: 1.5em; font-weight: bold;">
                            <xsl:value-of select="PRODUCTNAME"/>
                        </div>
                        <div>
                            <xsl:value-of select="DESCRIPTION"/>
                        </div>
                        <div>
                            <xsl:value-of select="PRICE"/>
                        </div>
                        <div>
                            <xsl:value-of select="QUANTITY"/>
                        </div>
                    </div>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>