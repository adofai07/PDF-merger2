# PDF-merger 2

This is my improved version of the previous PDF merger. Copy several pdf files (or zip files containing pdf files) in the `files` directory and run `main.py`. The syntax is as follows:

```py
syntax = {
    "MOD_CW": re.compile(r'\+'),
    "MOD_CCW": re.compile(r'\-'),
    "MOD_180": re.compile(r'\='),
    "FILE": re.compile(r'[a-zA-Z0-9]'),
    "RANGE": re.compile(r'\([a-zA-Z0-9]\-[a-zA-Z0-9]\)'),
    "FILE_PART_ST": re.compile(r'[a-zA-Z0-9]\[\d+-\]'),
    "FILE_PART_ED": re.compile(r'[a-zA-Z0-9]\[-\d+\]'),
    "FILE_PART_STED": re.compile(r'[a-zA-Z0-9]\[\d+-\d+\]'),
    "OUTPUT": re.compile(r'\{[a-zA-Z0-9]+\}'),
    "DELETE": re.compile(r'\![a-zA-Z0-9]'),
    "SHOW": re.compile(r'\@'),
}
```

### `MOD_CW`, `MOD_CCW`, `MOD_180`

They are simply `+`, `-`, and `=` respectively. They rotate the next thing clockwise, counter-clockwise, and 180 degrees.

### `FILE`

It is a single file identifier, which is a single alphanumeric character. For example, `a` refers to the file labeled `[a]` when you run `main.py`.

### `RANGE`

It is a range of files. For example, `(7-b)` refers to files labeled `[7]`, `[8]`, `[9]`, `[a]`, and `[b]`.

### `FILE_PART_ST`, `FILE_PART_ED`, `FILE_PART_STED`

They refer to parts of a file. For example, `c[3-]` refers to file `[c]` from page 3 to the end, `d[-5]` refers to file `[d]` from the start to page 5, and `e[2-6]` refers to file `[e]` from page 2 to page 6.

### `OUTPUT`

It specifies the output file name. For example, `{final}` means the output file will be named `final.pdf`.

### `DELETE`

It specifies a file to be deleted from the `files` directory while merging. For example, `!b` means the file labeled `[b]` will be deleted while merging. Note that the command runs from left to right, so if you have `!bb`, the file will be deleted before being added to the merged output, resulting in an error.

### `SHOW`

It is simply `@`. When this token is encountered, the program will open the final output in your default PDF viewer after merging.

### Using modifiers and ranges

You can combine modifiers and ranges. For example, `+(a-c)` means files `[a]`, `[b]`, and `[c]` will be rotated clockwise before being added to the merged output.  `-6[2-4]` means file `[6]` from page 2 to page 4 will be rotated counter-clockwise before being added to the merged output.

### Example

If you have files `example1.pdf`, `example2.pdf`, and `example3.pdf` in the `files` directory, the program will show:

```txt
[0]: example1.pdf
[1]: example2.pdf
[2]: example3.pdf
```

You can enter the string `+0[6-7](1-2)!2{merged}@` to rotate pages 6 to 7 of `example1.pdf` clockwise, add `example2.pdf` and `example3.pdf` as they are, delete `example3.pdf`, and output the merged file as `merged.pdf`. The final output `merged.pdf` will then open in your default PDF viewer.