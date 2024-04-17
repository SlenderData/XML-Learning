<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xlink="http://www.w3.org/1999/xlink">
    <xsl:template match="/">
        <html>
            <head>
                <title>XML链接示例</title>
            </head>
            <body>
                <h1>XML链接转换</h1>
                <xsl:for-each select="website/goto">
                    <a>
                        <xsl:attribute name="href">
                            <xsl:value-of select="@xlink:href"/>
                        </xsl:attribute>
                        <xsl:attribute name="title">
                            <xsl:value-of select="@xlink:title"/>
                        </xsl:attribute>
                        <xsl:value-of select="@xlink:title"/>
                    </a>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
