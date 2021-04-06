if __name__ == '__main__':
    d = {}
    index = 4
    d.setdefault(index, 0)
    d[index] += 1
    print(d)