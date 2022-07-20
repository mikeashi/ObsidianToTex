from mistletoe.block_token import BlockToken, BlockCode, Heading, Quote,CodeFence, ThematicBreak,List,Table,Footnote,Paragraph
from mistletoe import span_token
import mistletoe.block_tokenizer as tokenizer
from core.parser.tokens import Oink, Definition

class Document(BlockToken):
    #types = [Heading, Quote, CodeFence, ThematicBreak,List, Table, Footnote, Paragraph]
    types = [Definition, List, Heading, CodeFence, Paragraph]
    
    def __init__(self, lines):
        if isinstance(lines, str):
            lines = lines.splitlines(keepends=True)
        lines = [line if line.endswith('\n') else '{}\n'.format(line) for line in lines]
        self.footnotes = {}
        global _root_node
        _root_node = self
        span_token._root_node = self
        self.children = tokenizer.tokenize(lines, self.types)
        span_token._root_node = None
        _root_node = None