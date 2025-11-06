PDF_LABELS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def label2idx(label: str) -> int:
    return PDF_LABELS.index(label)