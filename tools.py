def box_string(text: str) -> str:
    """Boxes a multi-line string.

    Args:
        text: The string to be boxed. Can be multi-line.

    Returns:
        A new string with a box drawn around the original text.
    """
    lines = text.strip().split('\n')
    if not lines or all(not line for line in lines):
        return "┌──┐\n│  │\n└──┘"

    max_len = max(len(line) for line in lines)
    
    top = '┌' + '─' * (max_len + 2) + '┐'
    bottom = '└' + '─' * (max_len + 2) + '┘'
    
    boxed_lines = [top]
    for line in lines:
        padded_line = line.ljust(max_len)
        boxed_lines.append(f'│ {padded_line} │')
    boxed_lines.append(bottom)
    
    return '\n'.join(boxed_lines)

def time_format(seconds: float) -> str:
    """Formats time in seconds to a string of format MM:SS.

    Args:
        seconds: Time in seconds.
    Returns:
        A string representing the time in MM:SS format.
    """
    seconds = int(seconds)
    
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02}:{secs:02}"