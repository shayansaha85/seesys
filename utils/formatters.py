def bytes_to_human(n):
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i * 10)
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return f"{value:.2f}{s}"
    return f"{n}B"
