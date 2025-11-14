import PyPDF2
import os

class FileCache:
    def __init__(self):
        self.cache = []
        self.n = 0
        
    def new(self):
        name = f"cache/{self.n}.pdf"
        self.cache.append(name)
        self.n += 1
        return name
    
    def clear(self):
        for name in self.cache:
            if os.path.exists(name):
                os.remove(name)
        self.cache = []
        self.n = 0
        
    def merge(self, output_name: str):
        if len(self) == 0:
            return
        
        writer = PyPDF2.PdfWriter()
        for name in self.cache:
            reader = PyPDF2.PdfReader(name)
            for page in reader.pages:
                writer.add_page(page)
        with open(output_name, "wb") as f:
            writer.write(f)
        self.clear()
    
    def __len__(self):
        return len(self.cache)

class File:
    def __init__(self, cache: FileCache, file_path: str, orientation: int, st: None|int=None, ed: None|int=None):
        self.file_path = file_path
        self.orientation = orientation
        self.st = st
        self.ed = ed
        self.cache = cache
        
    def pdf(self):
        reader = PyPDF2.PdfReader(self.file_path)
        writer = PyPDF2.PdfWriter()
        
        total_pages = len(reader.pages)
        start_page = self.st - 1 if self.st is not None else 0
        end_page = self.ed - 1 if self.ed is not None else total_pages - 1
        
        for i in range(start_page, end_page + 1):
            page = reader.pages[i]
            writer.add_page(page.rotate(self.orientation))
                
        filename = self.cache.new()
        with open(filename, "wb") as f:
            writer.write(f)
        
        return filename

class FileRange:
    def __init__(self, cache: FileCache, orientation: int, file_paths: list[str]):
        self.orientation = orientation
        self.file_paths = file_paths
        self.cache = cache
        
    def pdf(self):
        writer = PyPDF2.PdfWriter()
        
        for file_path in self.file_paths:
            reader = PyPDF2.PdfReader(file_path)
            for page in reader.pages:
                if self.orientation == 90:
                    writer.add_page(page.rotate(90))
                elif self.orientation == 180:
                    writer.add_page(page.rotate(180))
                elif self.orientation == -90:
                    writer.add_page(page.rotate(-90))
                else:
                    writer.add_page(page)
                    
        filename = self.cache.new()
        with open(filename, "wb") as f:
            writer.write(f)
        
        return filename
    
if __name__ == "__main__":
    cache = FileCache()
    file1 = File(cache, "files\\test.pdf", 0)
    file2 = File(cache, "files\\test.pdf", 180, st=1, ed=3)
    
    file1.pdf()
    file2.pdf()
    
    cache.merge("files/output.pdf")