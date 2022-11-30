import numpy as np
from balocco.database.tables import Entry


def levenshtein(s, t):
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows, cols), dtype=int)
    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 1
            distance[row][col] = min(distance[row - 1][col] + 1,
                                     distance[row][col - 1] + 1,
                                     distance[row - 1][col - 1] + cost)
    return ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))


def search(words: list, query: str, precision: float = 0.5) -> list:
    results = {}
    for w in words:
        distance = levenshtein(w.term, query)
        if distance >= precision:
            results[w] = precision
    return list({k: v for k, v in sorted(results.items(), key=lambda item: item[1])}.keys())
