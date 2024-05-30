A Conversion Tool from DTD to XML Schema
----------------------------------------

-   [Download](#dow)
-   [Usage](#usa)
-   [Samples](#sam)
-   [How does it work?](#how)
-   [Copyright](#cop)
-   [History](#his)

------------------------------------------------------------------------

[Download]{#dow}
----------------

[dtd2xsd.pl](dtd2xsd.pl)

**Note:** the documentation below doesn\'t reflec the changes by MH; see
[her
announcement](http://lists.xml.org/archives/xml-dev/200101/msg00481.html)
of 11 Jan 2001 to xml-dev.

[Usage:]{#usa}
--------------

> +-----------------------------------------------------------------------+
> |     perl dtd2xsd.pl [-alias] [-prefix p] [-ns n] [file]               |
> |       -alias                                                          |
> |         enables special aliases (default off)                         |
> |       -prefix t                                                       |
> |         specify namespace prefix                                      |
> |       -ns http://www.w3.org/namespace/                                |
> |         specify namespace URI                                         |
> |       -simpletype pattern base                                        |
> |         treat parameter entities whose name match this pattern        |
> |         as simple datatypes derived from this base type               |
> |       -attrgroup pattern                                              |
> |         treat parameter entities whose name match this pattern        |
> |         as attribute groups                                           |
> |       -modelgroup pattern                                             |
> |         treat parameter entities whose name match this pattern        |
> |         as model groups                                               |
> +-----------------------------------------------------------------------+
>
> If no **file** is specified, STDIN will be used.

[**Samples:**]{#sam}

-   Simple sample: [DTD](sample.dtd) -\> [XML Schema](sample.xml)
-   [P3P DTD](https://www.w3.org/TR/2000/WD-P3P-20000404/#DTD) -\> [XML
    Schema](p3p.xml)
-   [SMIL DTD](https://www.w3.org/TR/1998/REC-smil-19980615/#dtd) -\>
    [XML Schema](smil.xml)
-   [XHTML Strict
    DTD](https://www.w3.org/TR/2000/REC-xhtml1-20000126/DTD/xhtml1-strict.dtd)
    -\> [XML Schema](xhtml.xml)
-   [MathML 2.0
    DTD](https://www.w3.org/TR/MathML2/appendixa.html#parsing:dtd) -\>
    [XML Schema](math.xml)

[How does it work?]{#how}
-------------------------

### 1. Encoding elements

+-----------------------------------+-----------------------------------+
| DTD                               | XML Schema                        |
+===================================+===================================+
|     <!ELEMENT ROOT (A,B) >        |     <element name="ROOT">         |
|                                   |      <c                           |
|                                   | omplexType content="elementOnly"> |
|                                   |       <element ref="t:A">         |
|                                   |       <element ref="t:B">         |
|                                   |      </complexType>               |
|                                   |     <element>                     |
+-----------------------------------+-----------------------------------+
|     <!ELEMENT ROOT (A|B) >        |     <element name="ROOT">         |
|                                   |      <c                           |
|                                   | omplexType content="elementOnly"> |
|                                   |       <choice>                    |
|                                   |        <element ref="t:A">        |
|                                   |        <element ref="t:B">        |
|                                   |       </choice>                   |
|                                   |      </complexType>               |
|                                   |     <element>                     |
+-----------------------------------+-----------------------------------+
|     <!ELEMENT ROOT (A|(B,C)) >    |     <element name="ROOT">         |
|                                   |      <c                           |
|                                   | omplexType content="elementOnly"> |
|                                   |       <choice>                    |
|                                   |        <element ref="t:A">        |
|                                   |        <sequence>                 |
|                                   |         <element ref="t:B">       |
|                                   |         <element ref="t:C">       |
|                                   |        </sequence>                |
|                                   |       </choice>                   |
|                                   |      </complexType>               |
|                                   |     <element>                     |
+-----------------------------------+-----------------------------------+
|     <!ELEMENT ROOT (A?,B+,C*) >   |     <element name="ROOT">         |
|                                   |      <c                           |
|                                   | omplexType content="elementOnly"> |
|                                   |                                   |
|                                   | <element ref="t:A" minOccurs="0"> |
|                                   |       <element                    |
|                                   |  ref="t:B" maxOccurs="unbounded"> |
|                                   |       <element ref="t:C" min      |
|                                   | Occurs="0" maxOccurs="unbounded"> |
|                                   |      </complexType>               |
|                                   |     <element>                     |
+-----------------------------------+-----------------------------------+

### 2. Encoding attributes

+-----------------------------------+-----------------------------------+
| DTD                               | XML Schema                        |
+===================================+===================================+
|     <!ATTLIST ROOT                |     <element name="ROOT">         |
|         a CDATA #REQUIRED>        |      <c                           |
|                                   | omplexType content="elementOnly"> |
|                                   |       <attribute name="           |
|                                   | a" type="string" use="required"/> |
|                                   |      </complexType>               |
|                                   |     <element>                     |
+-----------------------------------+-----------------------------------+
|     <!ATTLIST ROOT                |     <element name="ROOT">         |
|         a CDATA #IMPLIED>         |      <c                           |
|                                   | omplexType content="elementOnly"> |
|                                   |       <attribute name="           |
|                                   | a" type="string" use="optional"/> |
|                                   |      </complexType>               |
|                                   |     <element>                     |
+-----------------------------------+-----------------------------------+
|     <!ATTLIST ROOT                |     <element name="ROOT">         |
|         a (x|y|z) #REQUIRED;>     |      <c                           |
|                                   | omplexType content="elementOnly"> |
|                                   |       <attribute name="a">        |
|                                   |        <simpleType base="string"> |
|                                   |         <enumeration value="x"/>  |
|                                   |         <enumeration value="y"/>  |
|                                   |         <enumeration value="z"/>  |
|                                   |        </simpleType>              |
|                                   |       </attribute>                |
|                                   |      </complexType>               |
|                                   |     <element>                     |
+-----------------------------------+-----------------------------------+
|     <!ATTLIST ROOT                |     <element name="ROOT">         |
|         a CDATA #FIXED "x">       |      <c                           |
|                                   | omplexType content="elementOnly"> |
|                                   |       <attribute name="a" type    |
|                                   | ="string" use="fixed" value="x"/> |
|                                   |      </complexType>               |
|                                   |     <element>                     |
+-----------------------------------+-----------------------------------+

### 3. Simple Types, Attribute Groups, and Model Groups

Use `dtd2xsd.pl -simpleType ContentType string` to turn

    <!ENTITY % ContentType "CDATA">
        <!-- media type, as per [RFC2045] -->

into

      <simpleType name='ContentType' base='string'>
      </simpleType>

@\@along with references to %ContentType;

Use `dtd2xsd.pl -simpleType Number nonNegativeInteger` to turn

    <!ENTITY % Number "CDATA">

into

      <simpleType name='Number' base='nonNegativeInteger'>
      </simpleType>

@\@more on model groups, attribute groups. Meanwhile, see [the
makefile](Makefile) for examples.

[Copyright]{#cop}
-----------------

The program is Copyright © W3C® and provided under the [W3C Software
License](/Consortium/Legal/copyright-software)

[History:]{#his}
----------------

April 20 2000

:   -   Use `use` attribute instead of `minOccurs` attribute in
        `<attribute>` element.

    -   

        April 12 2000

        :   -   Understand `#FIXED` attribute.
            -   Treat external entities. **Limitation:** External files
                must be in the current directory.
            -   Treat conditional sections.

        April 11 2000

        :   -   The output is compliant with XML schema last call draft
                (change `<literal>`
            -   to `<enumerate value='...'>`).
            -   Added P3P special feature.

        April 10 2000

        :   -   Understand such patterns as `ELEM1?`, `ELEM2*`,
                `ELEM3+`, `#REQUIRED`, and `#IMPLIED`, and correctly
                procude `minOccurs` and `maxOccurs` attributes.
            -   Understand `(ELEM1|ELEM2|ELEM3)` pattern, and produce
                `<choice>` element.
            -   Understand `(attr1|attr2|attr3)` pattern, and produce
                `<literal>` element.
            -   Correctly understand nested bracket, and produce
                ` <sequence>` element.

        April 03 2000
        :   Dan connoly modified it, so that it can produce XML schema.

        March 17 1998
        :   Bert Bos originally created a conversion tool from DTD to
            BNF.

        ------------------------------------------------------------------------

        *Yuichi Koike (\$Date: 2017/11/22 16:53:40 \$)*
