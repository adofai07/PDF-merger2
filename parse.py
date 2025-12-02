import re

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
    "DELETE_RANGE": re.compile(r'\!\([a-zA-Z0-9]\-[a-zA-Z0-9]\)'),
    "SHOW": re.compile(r'\@'),
}

syntax_ext = {
    "MOD_CW": r'(\+)',
    "MOD_CCW": r'(\-)',
    "MOD_180": r'(\=)',
    "FILE": r'([a-zA-Z0-9])',
    "RANGE": r'\((.)-(.)\)',
    "FILE_PART_ST": r'([a-zA-Z0-9])\[(\d+)-\]',
    "FILE_PART_ED": r'([a-zA-Z0-9])\[-(\d+)\]',
    "FILE_PART_STED": r'([a-zA-Z0-9])\[(\d+)-(\d+)\]',
    "OUTPUT": r'\{([a-zA-Z0-9]+)\}',
    "DELETE": r'\!([a-zA-Z0-9])',
    "DELETE_RANGE": r'\!\(([a-zA-Z0-9])\-([a-zA-Z0-9])\)',
    "SHOW": r'(\@)',
}

def parse_token(tok: tuple[str, str]) -> tuple:
    name, val = tok
        
    for k, v in syntax_ext.items():
        if name == k:
            m = re.match(v, val)
            if not m:
                raise ValueError(f"Token '{val}' does not match pattern for '{name}'")
            return (name, *m.groups())
        
def parse(s: str) -> list:
    s = s.replace(" ", "")
    patterns = list(syntax.items())
    n = len(s)
    results = []

    def backtrack(i: int, path: list):
        if i == n:
            results.append(path.copy())
            return
        for name, pat in patterns:
            m = pat.match(s, i)
            if not m:
                continue
            if m.start() != i:
                continue
            tok = m.group(0)
            path.append((name, tok))
            backtrack(i + len(tok), path)
            path.pop()

    backtrack(0, [])
    return results


if __name__ == "__main__":
    parse_result = parse("+a-b(0-c)=c[-67]D1{merged}")
    
    for token in parse_result[0]:
        print(parse_token(token))