from parse import parse, parse_token
from pdf import FileCache, File, FileRange
from idx import label2idx, PDF_LABELS
from tools import box_string, time_format
import glob
import os
import time
import zipfile

def main():
    zip_files = glob.glob("files/*.zip")
    for zip_file in zip_files:
        print(f"Extracting {zip_file}...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall("files")
        os.remove(zip_file)
        
    for i in glob.glob("files/*"):
        if not i.endswith(".pdf"):
            os.remove(i)
        
    files = glob.glob("files/*.pdf")
    cache = FileCache()
    
    print(f"Found {len(files)} PDF files.")
    print("-" * os.get_terminal_size().columns)
    
    if len(files) == 0:
        print("No PDF files found in 'files/' directory.")
        return
    
    if len(files) > len(PDF_LABELS):
        print(f"Too many files! Maximum supported is {len(PDF_LABELS)}.")
        return
    
    for i in range(len(files)):
        print(f"[{PDF_LABELS[i]}] {files[i].split(chr(92))[1]}")
        
    user_input = parse(input("Enter command: "))
    start_time = time.time()
    
    if len(user_input) == 0:
        print("No valid tokens parsed.")
        return
    
    if len(user_input) >= 2:
        print("The command is ambiguous. Please specify which interpretation to use.")
        
        for i in range(len(user_input)):
            print(f"Interpretation {i+1}:")
            for token in user_input[i]:
                print(f"    {parse_token(token)}")
                
        choice = int(input(f"Select interpretation (1-{len(user_input)}): "))
        user_input = user_input[choice - 1]
        
    if len(user_input) == 1:
        user_input = user_input[0]
    
    n = len(user_input)
    l = len(str(n))
    
    ori = 0
    output = "output"
    show_output = False
    
    for i in range(n):
        print(box_string(f"[{i+1:>{l}}] ({time_format(time.time() - start_time)})\nClass: {user_input[i][0]}\nToken: {user_input[i][1]}"))
        
        token = parse_token(user_input[i])
        
        if token[0] == "MOD_CW":
            ori = 90
        
        elif token[0] == "MOD_CCW":
            ori = -90
            
        elif token[0] == "MOD_180":
            ori = 180
            
        elif token[0] == "FILE":
            file_char = token[1]
            file_path = files[label2idx(file_char)]
            File(cache, file_path, ori).pdf()
            
        elif token[0] == "RANGE":
            start_char = token[1]
            end_char = token[2]
            file_paths = []
            for j in range(label2idx(start_char), label2idx(end_char) + 1):
                file_paths.append(files[j])
            FileRange(cache, ori, file_paths).pdf()
            
        elif token[0] == "FILE_PART":
            file_char = token[1]
            page_num = int(token[2])
            file_path = files[label2idx(file_char)]
            File(cache, file_path, ori, st=page_num, ed=page_num).pdf()
            
        elif token[0] == "FILE_PART_ST":
            file_char = token[1]
            start_page = int(token[2])
            file_path = files[label2idx(file_char)]
            File(cache, file_path, ori, st=start_page).pdf()
        
        elif token[0] == "FILE_PART_ED":
            file_char = token[1]
            end_page = int(token[2])
            file_path = files[label2idx(file_char)]
            File(cache, file_path, ori, ed=end_page).pdf()
            
        elif token[0] == "FILE_PART_STED":
            file_char = token[1]
            start_page = int(token[2])
            end_page = int(token[3])
            file_path = files[label2idx(file_char)]
            File(cache, file_path, ori, st=start_page, ed=end_page).pdf()
            
        elif token[0] == "OUTPUT":
            output = token[1]
            
        elif token[0] == "DELETE":
            file_char = token[1]
            file_path = files[label2idx(file_char)]
            os.remove(file_path)
            
        elif token[0] == "DELETE_RANGE":
            start_char = token[1]
            end_char = token[2]
            for j in range(label2idx(start_char), label2idx(end_char) + 1):
                file_path = files[j]
                os.remove(file_path)
            
        elif token[0] == "SHOW":
            show_output = True
            
    # if len(cache) == 0:
    #     print("No files to merge.")
    #     return
            
    if output == "":
        print("No output filename specified. Using default 'output.pdf'.")
        output = "output"
    
    output_file = f"files/{output}.pdf"
        
    print(f"Merging files into 'files/{output}.pdf'")
    cache.merge(output_file)
    
    print("Clearing cache")
    cache.clear()
    
    if show_output:
        os.startfile(os.path.normpath(output_file))
    
    
if __name__ == "__main__":
    main()