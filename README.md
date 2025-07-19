# Narex

If you have ever used regular expressions, then you know how difficult they can be. Some people, when confronted with a problem, think _“I know, I’ll use regular expressions.”_ Now they have two problems [[1]](https://regex.info/blog/2006-09-15/247).

Challenges of using regular expressions:
- Expressions easily become unreadable, as they are extremely dense.
- No standardization or cross-flavor compatibility. Depending on the flavor, it can vary significantly. Supported features and syntax often differ.
- Unnatural pattern memorization. Humans quickly forget the syntax, as it is not intuitive.
- The learning curve is steep, especially for non-tech users. Even though many non-tech users need data processing, regular expressions remain out of reach for them.

The ultimate goal is to produce a DSL that uses natural language and enables cross-flavor compatibility.

The main use case is for the user to define the desired flavor (Perl, Python, etc.) and write a regular expression using natural language. The output will be raw regular expression, which can be directly used within the specified flavor.

This DSL can be widely used by people from different backgrounds, as it uses natural language. Tricky regular expressions are abstracted, and a universal tool for cross-flavor support is provided. Learning this DSL frees you from ever having to remember regular expression syntax again.

The biggest issues are the vast number of flavors, subtle differences, and partially supported advanced features. Due to the complexity of implementing a DSL that handles advanced features and multiple engine flavors, support will be added gradually.

## References:
[1] [Source of the famous “Now you have two problems” quote](https://regex.info/blog/2006-09-15/247) _(Author: Jeffrey Friedl, Accessed: _July 19, 2025_)_