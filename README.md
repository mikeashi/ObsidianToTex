# ObsidianToTex
Project to convert obsidian notes to Latex format

**This is a personal project and it is not intended to be universal solution**

I am trying to automate the process of converting obsidian notes to Latex format.

The project will grow if my needs change.

# Markdown parsers

There are several python parsers for markdown saddly none of them provide a formal lexer/parser rules.

The project [https://github.com/miyuchina/mistletoe](mistletoe) is the parser I choose to use since it is easy to extend and most importantly it is easy to modify.

# Current status

The converter is still in development but it is able to do the following:

- Convert headers to Latex.
- Convert lists to Latex.
- Convert math blocks to Latex.
- Convert code blocks to Latex.
- Convert definitions to Latex.


# Notes Structure
Currently the converter supports the following notes structure:
```
-- Root Folder  
|
|-- 001 First Section
    |-- 000.md
    |-- 001 Some title.md
    |-- 002 Some title.md
    |-- 003 Some title.md
|-- ... Section
|-- ... Section
|-- ... Section
|-- xxx Last Section
```
The first header tag in the 000.md file will define a new chapter.

# Latex template
You have to insert your template under `assets/template.`
The template foldere should contain a `main.tex` file
inside this file a ```[CONTENT]``` tag should be present, where the output will be inserted.
