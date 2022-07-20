import os
import enum
import shutil
from .Note import Note


class Modes(enum.Enum):
    FILE = 1
    DIRECTORY = 2


class Converter:
    def __init__(self, inputPath, outputPath="output", ignored=["Draft"]) -> None:
        if not os.path.exists(inputPath):
            raise Exception("Input path does not exist")
        if os.path.isfile(inputPath):
            self.mode = Modes.FILE
        else:
            self.mode = Modes.DIRECTORY
        self.cleanOutputFolder(outputPath)
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.parts = []
        self.ignored = ignored

    def cleanOutputFolder(self, outputPath) -> None:
        if os.path.exists(outputPath):
            shutil.rmtree(outputPath)
        os.mkdir(outputPath)
        os.mkdir(outputPath + "/parts")
        # copy template folder
        shutil.copytree('assets/template', outputPath,dirs_exist_ok=True)


    def convert(self) -> None:
        self.load()
        texParts = []
        for part in self.parts:
            name, notes = part
            self.writePart(name, notes)
            texParts.append(name + ".tex")
        
        # build content file
        output = ""
        with open(os.path.join(self.outputPath, "parts/content.tex"), "w+") as f:
            for texPart in texParts:
                output = output + "\\input{parts/" + texPart + "}\n"
                output = output + "\n"

        with open(os.path.join(self.outputPath, "main.tex"), "r") as f:
            content = f.read()
            content = content.replace("[CONTENT]", output)
            with open(os.path.join(self.outputPath, "main.tex"), "w+") as f:
                f.write(content)
        
                
            
    def writePart(self, name, notes) -> None:
        with open(os.path.join(self.outputPath, "parts", name + ".tex"), "w+") as f:
            for note in notes:
                f.write(note.tex)
                f.write("\n")
                f.write("\n")

            

    def load(self) -> None:
        if self.mode == Modes.FILE:
            self.loadFile()
        elif self.mode == Modes.DIRECTORY:
            self.loadFolders()

    def loadFile(self) -> None:
        raise Exception("Not implemented")

    def loadFolders(self) -> None:
        folders = sorted(os.listdir(self.inputPath))
        for folder in folders:
            name = self.getName(folder)
            self.parts.append((name, self.loadFolder(folder)))

    def loadFolder(self, folder) -> None:
        files = sorted(os.listdir(os.path.join(self.inputPath, folder)))
        notes = []
        for file in files:
            if any(word in file for word in self.ignored):
                continue
            notes.append(Note(os.path.join(self.inputPath, folder, file)))
        return notes

    def getName(self, folder, name=None) -> str:
        if name is None:
            name = folder.split(" ")[1]
        if name in self.getNames():
            return self.getName(folder, name+"_")
        else:
            return name

    def getNames(self) -> list:
        names = []
        for part in self.parts:
            name, notes = part
            names.append(name)
        return names
