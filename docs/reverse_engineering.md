# Reverse engineering analysis
Within this document, an analysis about the further improvement of Narex in the context of reverse engineering will be conducted.

The main idea is about leveraging Narex by converting random regular expressions into more readable expressions, ideally converging toward natural language.

For instance, if we have the following regular expression:
``` sh
[A-Za-z]{1,}\s{0,}[A-Za-z]{1,}
```
We might convert it into something like:
``` sh
letter 1 or more times 
whitespace 0 or more times
letter 1 or more times
```
As we can see, it is definitely more readable than the original raw regular expression.

The main pros of this idea besides readability are:
- Possibility of easier debugging of messy regex.
- Decoding rare and context-dependent regex operators.

Further text will focus on analyzing doability of this idea.

What if we have a more complex regex? For instance, something like this:
``` sh
^[A-Za-z]{1,}(?:\.[A-Za-z]{1,}){0,}@[A-Za-z]{1,}(\.[A-Za-z]{1,}){1,}$
```
We might convert it into something like this:
``` sh
starts
letter repeat 1 or more times 
uncaptured group {. letter repeat 1 or more times} repeat 0 or more times
@
letter repeat 1 or more times 
group {. letter repeat 1 or more times} repeat 1 or more times
ends
```

The source of this example intentionally wasn't shared earlier, just to show how difficult it is to understand what a regex means without context. It is an email example from [here](/examples/email/).

Therefore, the main cons of this idea are:
- We have definitely increased readability, but except for a better understanding of concrete operators, we still can't easily grasp the original idea of the user. If we use an analogy, we are now closer to assembler than to machine code, but still far from Python. The main problem is losing the "why", as clause names are converted into regex.
- If we focus on a specific engine, for instance Python, we must support all possible operators defined by its specification. Otherwise, the tool won't work. In contrast, Narex supports a minimal set of rules which is enough to explain any mental model of the user. Also, the user must use defined rules, while in reverse engineering any input is allowed. This factor leads to high implementation complexity. A hybrid approach would be to focus on commonly used operators at the beginning.
- Grammar might be a bit more complex because of the nature of variations. For instance, if we want to get `alphanumeric`, then corresponding regex patterns are `[a-zA-Z0-9_]`, `[A-Za-z0-9_]`, and so on, leading to 24 combinations, and it is just for one rule. Also, many similar rules use brackets, like `either` (`[abc]`) or `optional` (`[ab|ba|ca]`). The parser might have many processing hurdles. 
- Currently, concrete rule explanations are provided by the vast majority of tools, but accurate semantics are not provided by any [[1]](https://regex101.com/)[[2]](https://regexr.com/). The only way to provide original semantics is by using AI agents, however, they are inaccurate [[3]](https://www.gitloop.com/tool/regex-explainer). At the moment of this analysis, a better idea for converting raw regex into natural language has not been found.

All in all, this feature could be useful, but it involves many implementation hurdles with limited value for the end user compared to the required effort.

The analysis above reflects the author's current view. We are open to further suggestions and opinions. If anyone is interested in the challenge, they are welcome to contribute and help implement regex reverse engineering.

## References:
[1] [regex101: build, test, and debug regex](https://regex101.com/) _(Author: Firas Dib, Accessed: _May 9, 2026_)_

[2] [RegExr: Learn, Build, & Test RegEx](https://regexr.com/) _(Author: gskinner.com, Accessed: _May 9, 2026_)_

[3] [Regex Explainer With AI](https://www.gitloop.com/tool/regex-explainer) _(Author: Denzelle W., Accessed: _May 9, 2026_)_
