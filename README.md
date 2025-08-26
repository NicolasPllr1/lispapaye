# LISP interpreter

This LISP interpreter was started as a mini-project to get into the
[Recurse Center](https://www.recurse.com/).

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
