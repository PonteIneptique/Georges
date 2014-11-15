#Introduction
This document is defining the structure, in XML TEI, we want to achieve

It wont take care of the header, because the header is not generated with this tool. If you think we should add something about it, please feel free.

##Document general structure

###Structure

```xml
<text>
	<body>
		<pb n="1"/>
		<cb n="A"/>
		<div0 type="alphabetic letter" n="A">
			<head lang="la">A</head>
			<entryFree>
				<sense></sense>
			</entryFree>
		</div0>
	</body>
</text>
```

##Dictionary Entries

###Structure
```xml
<entryFree n="X">
	<sense level="1" n="1">
		<orth key="string">string</orth>
		<itype>The extension</itype>
		<gen>The grammatical nature or gender</gen>
		<etym>Etymology information</etym>
		<bibl>
			<author>Not Optional</author>
			<book>Optional</book>
			Some identifier for the part of the book
		</bibl>
	</sense>
</entryFree>
```

###Attributes
- `entryFree.n` represents the numeric index of this entry in the entire dictionary
- `orth.key` represents orthograph without diacritics
- `sense.level` represents the level in the hierarchy for the given sense
- `sense.n` represents the order of the sense at its own level. **e.g.** : *4.B* will have a `level="4" n="2"`

###Example
```xml
<entryFree n="9">
	<orth key="abaculus">abaculus</orth>
	<itype>ī</itype>
	<gen>m.</gen>
	<sense>
		 (Demin. v. abacus), ein kleiner Würfel von gefärbtem Glas zu Mosaikarbeiten, 
		<bibl>
			<author>Plin.</author>
			36, 199.
		</bibl>
	</sense>
</entryFree>
```

###Potential nodes
- `entryFree` > `<lang type="greek"></lang>` represents a part of the text which is in a specific language (mostly )greek here)


##Secondary Source

###Introduction

In the Georges, you can find secondary sources in the dictionary entries. To encode them, we decided to create a main `<bibl>` with its author name and then the primary sources used by the author of the secondary source.

###Structure
```xml
<bibl>
	<author>Name of the modern author.</author>
	<bibl>
		<author>Author of the Primary Source</author>
		<title>[Optional] Title of the Secondary Source</title>
		[Optional] Identifiers of the text's part
	</bibl>
</bibl>
```

###Example
```xml
<bibl>
	<author>Muncker</author>
	<bibl>
		<author>Hyg.</author>
		<title>fab.</title>
		257.
	</bibl>
</bibl>
```