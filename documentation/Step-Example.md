##Introduction
For the example, we will recode our `greek` node tool. As you can see in our structure, we hope to be able to know when in our entries we have a German sentence and when we have a greek one. To do so, the simpler is to first identify Greek words. And that's easy, because they don't use the same alphabet !

##Define your "namespace"
In all our file, we try to use the same string to identify our step. For example, primarySource is used as a dictionary index all over the place, in normalization, regexp, etc. Ours will be `greek`.

##Regular Expression
A good thing to do first is to come up with a regular expression matching our needs. Kind of easy : `"((?:(?:[\p{Greek}µ']+)+[\s\.\,]*)+)"` will do the work. So next step ? We create a function to return that string

```python
def greek(self):
	regexp = "((?:(?:[\p{Greek}µ']+)+[\s\.\,]*)+)"),
	return regexp
```

We use the `self.generate` function so we don't care about modifying our matcher/grouper. This function will indeed return it with a global matcher group or with the group with no name we gave

```python
def self.generate(self, category, grouper = True)
	mappings = {
		...
		"greek" : self.greek
	}
```

We add it to our matrix in [tools.regexp.RegExp.matrix](../tools/regexp.py)

```python
class RegExp(object):
	def __init__(self):
		...
		self.matrices = {
			"greek" : {
				"matcher" : self.generate("greek", False),
				"grouper" : self.generate("greek")
			}
		}
```

##Node Generation function
So, now we have a regexp function. Great. What we need now is a function to create the node, which we will add to [tools/nodes.py](../tools/nodes.py). A Node Generation function takes 4 arguments, lets copy them.

```python
def Greek(text, node, regexp = None, normalizer = None):
```
The text we receive is something that got match against our `RegExp().matrices["greek"]["matcher"]`. In fact, there is no possible subnodes in a `<lang>` node. We won't need the `grouper` in this case... We now have to add the node generation and return the parent node. For clarity purpose, we put a `default = None` to the variable we won't use


```python
def Greek(text, node, regexp = None, normalizer = None):
	lang = cElementTree.SubElement(node, "lang")
	lang.set("lang", "greek")
	lang.text = text
	return node
```

##Create the Step
Now, let's add it to our workflow in [__main__.py](../__main__.py) ! First thing first, we import our Node Generator function `Greek` and give it a name which won't provoke any issue, adding Nodification at the end.

```python
from tools.nodes import Greek as GreekNodification
```

Then we instantiate our step before any other steps:
```python
Greek = Step(
	#We reuse our name here
		name = "greek", 

	#We reuse our RegExp object where we have our RegExp().matrices
		matrix = regexp.matrices, 

	#We use the name we used as alias
		fn = GreekNodification, 

	#We put the normalizer instance
		normalizer = normalizer,

	#And as we have no following step, we put the child to None
		child = None
	)
```

In our test case, the smallest step was PrimarySource. So we add at the end of it :
```python
PrimarySource = Step(
	...
	child = Greek
)
```

And here it is ! Run it, look at sample, enhance your regexp and node generator !