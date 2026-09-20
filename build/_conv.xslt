<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="*"/>

  <xsl:template match="/">
    <xsl:apply-templates select="//w:body"/>
  </xsl:template>

  <xsl:template match="w:body">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- tables -->
  <xsl:template match="w:tbl">
    <xsl:text>&#10;[[TABLE]]&#10;</xsl:text>
    <xsl:apply-templates select="w:tr"/>
    <xsl:text>&#10;[[/TABLE]]&#10;</xsl:text>
  </xsl:template>
  <xsl:template match="w:tr">
    <xsl:text>| </xsl:text>
    <xsl:for-each select="w:tc">
      <xsl:apply-templates select=".//w:t"/>
      <xsl:text> | </xsl:text>
    </xsl:for-each>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

  <!-- paragraphs -->
  <xsl:template match="w:p">
    <xsl:variable name="st">
      <xsl:for-each select="w:pPr/w:pStyle/@w:val"><xsl:value-of select="."/></xsl:for-each>
    </xsl:variable>
    <xsl:variable name="txt">
      <xsl:apply-templates select=".//w:t"/>
    </xsl:variable>
    <xsl:variable name="num">
      <xsl:for-each select="w:pPr/w:numPr/w:ilvl/@w:val"><xsl:value-of select="."/></xsl:for-each>
    </xsl:variable>
    <xsl:if test="string-length(normalize-space($txt)) &gt; 0">
      <xsl:choose>
        <xsl:when test="starts-with($st,'Heading') or starts-with($st,'heading')">
          <xsl:text>&#10;### </xsl:text>
        </xsl:when>
        <xsl:when test="string-length($num) &gt; 0">
          <xsl:text>- </xsl:text>
        </xsl:when>
        <xsl:otherwise><xsl:text></xsl:text></xsl:otherwise>
      </xsl:choose>
      <xsl:value-of select="normalize-space($txt)"/>
      <xsl:text>&#10;</xsl:text>
    </xsl:if>
  </xsl:template>

  <xsl:template match="w:tab"><xsl:text>&#9;</xsl:text></xsl:template>
  <xsl:template match="w:br"><xsl:text>&#10;</xsl:text></xsl:template>
  <xsl:template match="w:t"><xsl:value-of select="."/></xsl:template>
  <xsl:template match="text()"/>
</xsl:stylesheet>
