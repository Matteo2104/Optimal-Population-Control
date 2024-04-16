def occurrence(V, el):
    count = 0
    for v in V:
        if v == el:
            count += 1
    return count