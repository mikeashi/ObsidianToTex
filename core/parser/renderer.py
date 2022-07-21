from mistletoe.latex_renderer import LaTeXRenderer
import core.parser.tokens as tokens
from itertools import chain
from core.parser.document import Document
import mistletoe.block_tokenizer as tokenizer
from mistletoe import block_token, span_token


class Renderer(LaTeXRenderer):
    def __init__(self, header=False):
        self.header = header
        self.chapter = False
        super().__init__(*chain(self._tokens_from_module(tokens)))
    
    def render_document(self, token):
        return self.render_inner(token)

    def render_definition(self, token):
        # open tag
        template = '\n\\begin{definition}'
        
        # add title
        if token.title != '':
            template += '[{}]\n'.format(token.title)
            # TODO add lable
        
        # add text
        template += '\n{}\n'.format(self.element_render(self.span_tokens(token.paragraph)))

        # add list
        if token.list != []:
            template += '\n{}\n'.format(self.element_render(self.block_tokens(token.list)))
        # close tag
        template += '\n\\end{definition}\n'
        return template


    def render_oink(self,token):
        # TODO : get the citention id
        return "\cite{{{}}}".format(token.content[1:])

    def render_heading(self, token):
        inner = self.render_inner(token)
        if not self.chapter and self.header:
            self.chapter = True
            return "\\chapter{{{}}}".format(inner)
        if token.level == 1:
            return '\n\\section{{{}}}\n'.format(inner)
        elif token.level == 2:
            return '\n\\subsection{{{}}}\n'.format(inner)
        return '\n\\subsubsection{{{}}}\n'.format(inner)

    def span_tokens(self,text):
        return span_token.tokenize_inner(text)
    
    def block_tokens(self,lines):
        return tokenizer.tokenize(lines, Document.types)

    def element_render(self,tokens):
        return ''.join(map(self.render, tokens))