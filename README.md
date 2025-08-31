# LISP interpreter

This LISP interpreter was started as a mini-project to get into the
[Recurse Center](https://www.recurse.com/).

## Quick try

Using [uv](https://docs.astral.sh/uv/):

```bash
uv sync  # create virtual env. at .venv/ and install project dependencies (described in pyproject.toml)
source .venv/bin/activate # activate your virtual env.
python main.py # runs the parser over all snippets in lisp_snippets/
```

Running `python main.py` will run the scanner + parser over all examples in
`./lisp_snippets/`. You can also target a single file, for example:
`python main.py lisp_snippets/symbol.lisp`.

## Lisp code snippets

I will take examples from
[Paul Graham's ANSI Common Lisp](https://www.paulgraham.com/acl.html).
[Chapter 2](https://sep.turbifycdn.com/ty/cdn/paulgraham/acl2.txt?t=1688221954&)
is available for free on his website.

## Plan

### 1. Scanning

The first step is scanning lisp snippets with common syntax.

Having skimmed chapter 1 and 2 from Paul Graham's book, I'm thinking of:

- basic arithmetic operators (+, -, /)

- lisp specific list operator/functions (quote, cons)

- specific values (nil, t)

And also strings.

This does not cover every bits of syntax mentioned in chapter 2, but I think I
will keep it there. Although I think scanning will not be hard. More allowed
tokens simply means more if/else cases to write. But I would like my scanning
capabilities to match my parsing capabilities, so I may limit
[the scanner](#2-parsing) 'power' on purpose. We will see!

### 2. Parsing

This where we lift the flat list of tokens into a tree - the 'AST'.

Nodes in the tree represent either:

- operators, over what their children in the tree represents.
- 'atomic' values (like a literal string or a number). These are the leaves in
  the AST.

I would like to parse the basic pieces of syntax I outlined in the
[scanning section](#1-scanning).

### 3. Interpreting

This will be done pair-programming!

Ideas:

- Assume the lisp program is a single expression: the goal is to evaluate it
- We need to define what are the _possible return values_: numbers, true/nil,
  strings, symbols, lists (~any Lisp program (!), through quoting) And translate
  them to python-land.
- A list is interpreted either as data (a list of data) or as code (a function)
- Keep Lisp _evaluation rule_ in mind when interpreting lists:
  1. evaluate args from left to right, recursively
  2. the args' values are passed to the function named by the operator (which is
     the list first element)

Note: when interpreting a list, it it's not quoted, then it must be a function
-> the first element must be an operator or point/refer to a function

## Resources

- Original 1960 paper by John McCarthy: \[Recursive Functions of Symbolic
  Expressions and Their Computation by Machine, Part
  I\]((https://www-formal.stanford.edu/jmc/recursive.pdf)

- Paul Graham's work

  - [ANSI Common Lisp](https://www.paulgraham.com/acl.html) (1995)
  - [The root of Lisp](https://paulgraham.com/rootsoflisp.html) (may 2001)
  - [What made Lisp different](https://paulgraham.com/diff.html) (dec 2001)
  - [Bel](https://paulgraham.com/bel.html) (oct 2019)

- Wikipedia

  - [Lisp](<https://en.wikipedia.org/wiki/Lisp_(programming_language)>)
  - [S-expression](https://en.wikipedia.org/wiki/S-expression)
  - [Interpreter#History](<https://en.wikipedia.org/wiki/Interpreter_(computing)#History>)
