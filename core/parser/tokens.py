import re
import mistletoe.span_token as span_token
import mistletoe.block_token as block_token
from mistletoe.block_token import List as List



__all__ = ['Oink','Definition']



class Oink(span_token.SpanToken):
    pattern = re.compile(r'\[\s?@?(\w*)\s?\]')
    parse_inner = False
    parse_group = 1

class Definition(block_token.BlockToken):
    pattern = re.compile(r'(Definition)|(definition):')
    _open_info = None
    
    def __init__(self, match):
        self.title,self.paragraph,self.list = match
        

    @classmethod
    def start(cls, line):
        match_obj = cls.pattern.match(line)
        if not match_obj:
            return False
        return True
    
    @classmethod
    def read(cls,lines):
        # first line contains Definition:
        line = next(lines)
        # remove definition:
        line = line[len('Definition:'):]
        # remove leading and trailing whitespace
        line = line.strip()
        title = ''
        # check if there is a title
        if line.startswith('('):
            # get title
            title = line[1:line.index(')')]
            # remove title from line
            line = line[line.index(')')+1:]
            # remove leading and trailing whitespace
            line = line.strip()
        
        line_buffer = [line]
        list = []
        for line in lines:
            if line == '\n':
                break
            if line.startswith('\t'):
                list.append(line[1:])
                continue
            line_buffer.append(line)


        return title,"".join(line_buffer),list