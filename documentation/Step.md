#Step

To simplify the addition of new node discovery service (which from a regular expression creates a new node), a Step object is available. You can find it in the folder `tools/steps.py`.

The Steps come in the process when `senses` have been drawn. **Steps will be performed on the content matched as a sense definition.** Let's have a look at is structure... 

##Structure of Step()
The Step object takes up to five parameters which are :
- `name` : The whole project is using dictionary. A good practice is to keep everything with the same name. So for example, if I wanted to get a new Step to identify Greek, you would name your step `greek` and remind of this string.
- `matrix` : The matrix is a dictionary where you can find sub-dictionary with your `name` as index. In this sub-dictionary, you'll often find a `matcher` and a `grouper`. See [below](#A-little-more) for more information.
- `fn` : This is a function that your Step will call when there is a match. *Remind not to put the parenthesis at the end of your function name !* It will create the nodes for you and return the parent node. See the documentation about [Node Generator Function](#Node maker)
- `normalizer` : a `tools.normalization.Normalizer` instance, potentatially used in your `fn`
- `child` : The next step you want to perform. If None, the step will take care of the rest of unmatched strings as texts

##Node generator function

##A little more about the regexp ?
In the situation where what your are trying to match can contain subnodes, such as a bibliography, you will want to avoid having subgroups when you do a `re.match()`. To avoid this kind of situation, we use two 

Those two types of regular expression are used for different things: 
- the `matcher` will be used to return or split a global element matching your regular expression; 
- the `grouper` will be used to find - if needed - subgroups. 

The good thing with this ? In the RegExp class inside `tools/regexp.py`, you will find the function `self.getMatcher` to remove from your grouper regular expression strings the group names, transforming `(?P<myname>[a-z])` into `(?:[a-z])`. Easy isn't it ?