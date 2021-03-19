from orthogonal_table import Query_from_file
from orthogonal_table import Query_from_py


class QueryTable:
    def __init__(self):
        self.q_file = Query_from_file.QueryTable()
        self.q_py = Query_from_py.QueryTable()

    def solve(self, data: list):
        f_ret = self.q_file.solve(data)
        if f_ret is None:
            print('from py:')
            return self.q_py.solve(data)
        else:
            print('from file:')
            return f_ret


if __name__ == '__main__':
    # 3^4
    data1 = [
        ['浏览器', ["Windows", "Linux", "MAC"]],
        ['操作平台', ["Firefox", "Opera", "IE"]],
        ['语言', ["Chinese", "English", "spanish"]],
        ['不正经', ["1", "2", '3']]
    ]

    # 2^4 3^1
    data2 = [
        ['e', ["e0", "e1", "e2"]],
        ['a', ["a0", "a1"]],
        ['b', ["b0", "b1"]],
        ['c', ["c0", "c1"]],
        ['d', ["d0", "d1"]]
    ]

    # 2^3 4^1 6^1
    data3 = [
        ['e', ["e0", "e1", "e2", 'e3', 'e4', 'e5']],
        ['a', ["a0", "a1", 'a2', 'a3']],
        ['b', ["b0", "b1"]],
        ['c', ["c0", "c1"]],
        ['d', ["d0", "d1"]]
    ]

    qt = QueryTable()
    s = qt.solve(data1)
    for i in s:
        print(i)

    print('================')
    s = qt.solve(data2)
    for i in s:
        print(i)

    print('================')
    s = qt.solve(data3)
    for i in s:
        print(i)
