#Step

To simplify the addition of new node discovery service (which from a regular expression creates a new node), a Step object is available. You can find it in the file [tools/steps.py](../tools/steps.py). It is declared at the beginning of `__main__.py`

The Steps come in the process when `senses` have been drawn. **Steps will be performed on the content matched as a sense definition.** Let's have a look at is structure... 

##Example
If you want to see how to code your own step, go [there](Step-Example.md). But may be read the documentation before

##Structure of Step()
The Step object takes up to five parameters which are :
- `name` : The whole project is using dictionary. A good practice is to keep everything with the same name. So for example, if I wanted to get a new Step to identify Greek, you would name your step `greek` and remind of this string.
- `matrix` : The matrix is a dictionary where you can find sub-dictionary with your `name` as index. In this sub-dictionary, you'll often find a `matcher` and a `grouper`. See [below](#a-little-more-about-the-regexp-) for more information.
- `fn` : This is a function that your Step will call when there is a match. *Remind not to put the parenthesis at the end of your function name !* It will create the nodes for you and return the parent node. See the documentation about [Node Generator Function](#node-generator-function)
- `normalizer` : a `tools.normalization.Normalizer` instance, potentatially used in your `fn`
- `child` : The next step you want to perform. If None, the step will take care of the rest of unmatched strings as texts

##Node generator function
This function should be, if possible, in the `tools.nodes` [file](../tools/nodes.py), use your `name` with a capital and be imported in main as `name`Nodification. **eg** : 

```python
from tools.nodes import Greek as GreekNodification
```

The function should return the parent node. The function is built with the following given parameters. *All parameters have to be in the function declaration, it doesn't mean you have to use them.*
- `text` : The text which is matching your requirement
- `node` : The parent node that you will return when your additions are done
- `regexp` : The regular expression dictionary we talked about earlier as the `Step(matrix = _)`. It can be used to access the grouper but also for example to reuse a given regexp for a potential subnode of your node
- `normalizer` : The same normalizer that can be used

##A little more about the regexp ?
In the situation where what your are trying to match can contain subnodes, such as a bibliography, you will want to avoid having subgroups when you do a `re.match()`. To avoid this kind of situation, we use two different regular expression.

Those two types of regular expression are used for different things: 
- the `matcher` will be used to return or split a global element matching your regular expression; 
- the `grouper` will be used to find - if needed - subgroups. 

The good thing with this ? In the RegExp class inside [tools/regexp.py](../tools/regexp.py), you will find the function `self.getMatcher` to remove from your grouper regular expression strings the group names, transforming `(?P<myname>[a-z])` into `(?:[a-z])`. Easy isn't it ?

##Full grouping function
**Important** In the case of some interesting situation, like the firstLine, our matcher should match the whole first line and return the rest of the text. To allow us to do that, if there is no matcher for a regexp, the nodes maker should return a tuple where [0] is the node, [1] is the text to process for child.