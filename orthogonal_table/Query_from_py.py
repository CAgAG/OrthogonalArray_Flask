from orthogonal_table.allpairspy import AllPairs


class QueryTable:
    def solve(self, data: list):
        """
        :param data:
                    [
                        ['浏览器', ["Windows", "Linux", "MAC"]],
                        ['操作平台', ["Firefox", "Opera", "IE"]],
                        ['语言', ["Chinese", "English", "spanish"]],
                        ['不正经', ["1", "2", '3']]
                    ]
        :return:
        """
        ret = []
        parameters = []
        keys = []
        for i in data:
            keys.append(i[0])
            parameters.append(i[1])

        for eles in AllPairs(parameters):
            t_dict = {}
            for index, ele in enumerate(eles):
                t_dict.setdefault(keys[index], ele)
            ret.append(t_dict)
        return ret


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
        ['d', ["d0", "d1"]],

    ]

    qt = QueryTable()
    s = qt.solve(data1)
    for i in s:
        print(i)

    print('================')
    s = qt.solve(data2)
    for i in s:
        print(i)
