import enum
import os
from core.parser.document import Document
from core.parser.renderer import Renderer

class Type(enum.Enum):
    HEADER=True
    BODY=False

class Note:
    def __init__(self, path) -> None:
        self.path = path
        if not os.path.exists(path):
            raise Exception("Path does not exist")
        self.name = os.path.basename(path)
        if self.name.startswith("000"):
            self.type = Type.HEADER
        else:
            self.type = Type.BODY
        self.load()
        self.convert()
    
    def load(self) -> None:
        with open(self.path, "r") as f:
            self.markdown = f.read()

    def convert(self) -> str:
        self.tex = Renderer(self.type == Type.HEADER).render(Document(self.markdown))
        

    def __repr__(self) -> str:
        return f"{self.name}, {self.type}"