

class QueryTable:
    def __init__(self, data_path='./orthogonal_table/data/ts723_Designs.txt'):
        all_table = {}
        with open(data_path, 'r') as f:
            all_lines = f.readlines()
            length = len(all_lines)
            index = 0
            while True:
                if index == length:
                    break
                file_list = all_lines[index]
                if '\n' == file_list:
                    index += 1
                    continue
                if '^' in file_list:
                    mk, n = file_list.strip().split('     ')
                    all_table[mk] = []
                    for _ in range(int(n.replace('n=', ''))):
                        index += 1
                        all_table[mk].append(all_lines[index].strip())
                index += 1
        self.query_table = all_table

    def gen_query(self, data: list):
        """
        data = [
                ['浏览器', ["Windows", "Linux", "MAC"]],
                ['操作平台', ["Firefox", "Opera", "IE"]],
                ['语言', ["Chinese", "English", "spanish"]],
                ['不正经', ["1", "2"]]
            ]
        """
        table = {}
        for line in data:
            # 水平
            m = len(line[1])
            table.setdefault(m, 0)
            # 因素
            table[m] += 1

        query_str = []
        for k, v in table.items():
            query_str.append(f'{k}^{v}')
        return query_str

    def get_query_key(self, qs: list):
        # 配合 gen_query 使用
        # qt.get_query_key(['64^1', '2^64'])
        """
        :param qs:
        :return: 失败： None
        """

        q_length = len(qs)
        for k in self.query_table.keys():
            k_list = k.split(' ')
            if len(k_list) != q_length:
                continue

            flag = True
            for q in qs:
                if q not in k_list:
                    flag = False
                    break

            if flag:
                return k

    def split_table(self, query_key: str):
        """
        :param query_key: '3^20 6^1 21^1'
        :return: 二维索引列表
        """
        data = self.query_table[query_key]
        keys = query_key.split(' ')

        tables = []
        for d in data:
            start = 0
            ss = []
            # 混合正交表
            for key in keys:
                m = len(key.split('^')[0])
                k = int(key.split('^')[-1])
                # ss.append(d[start: start + m * k].strip())
                s_str = d[start: start + m * k]
                for s in range(len(s_str) // m):
                    ss.append(int(s_str[s * m: s * m + m].strip()))
                start += m * k

            tables.append(ss)

        return tables

    def solve(self, data: list):
        """
        :param data: 数据
        :return: 成功返回列表, 失败返回None
        """
        gen_key = self.gen_query(data)
        query_key = self.get_query_key(gen_key)
        print('query_key: ', query_key)
        if query_key is None:
            return None
        ret = []
        data = self.reshape_data(query_key, data)

        for index_list in self.split_table(query_key):

            r = {}
            for index, v_index in enumerate(index_list):
                # data[index][1][v_index]
                header = data[index][0]
                content = data[index][1][v_index]

                r.setdefault(header, 'None')
                r[header] = content
            ret.append(r)

        return ret

    def reshape_data(self, shape: str, data_list: list) -> list:
        """
        :param shape: query_key -> self.get_query_key(gen_key)
        :param data_list: data
        :return: reshape data
        """
        new_data = []
        shape_list = shape.strip().split(' ')
        data_dict = {}
        for data in data_list:
            c = data_dict.setdefault(f'{len(data[1])}', [])
            c.append(data)

        for sp in shape_list:
            num = sp.split('^')[0]
            new_data.extend(data_dict[num])
        return new_data


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
    """
    {'浏览器': 'Windows', '操作平台': 'Firefox', '语言': 'Chinese', '不正经': '1'}
    {'浏览器': 'Windows', '操作平台': 'Opera', '语言': 'spanish', '不正经': '2'}
    {'浏览器': 'Windows', '操作平台': 'IE', '语言': 'English', '不正经': '3'}
    {'浏览器': 'Linux', '操作平台': 'Firefox', '语言': 'spanish', '不正经': '3'}
    {'浏览器': 'Linux', '操作平台': 'Opera', '语言': 'English', '不正经': '1'}
    {'浏览器': 'Linux', '操作平台': 'IE', '语言': 'Chinese', '不正经': '2'}
    {'浏览器': 'MAC', '操作平台': 'Firefox', '语言': 'English', '不正经': '2'}
    {'浏览器': 'MAC', '操作平台': 'Opera', '语言': 'Chinese', '不正经': '3'}
    {'浏览器': 'MAC', '操作平台': 'IE', '语言': 'spanish', '不正经': '1'}
    """

    print('================')
    s = qt.solve(data2)
    for i in s:
        print(i)
    """
    {'a': 'a0', 'b': 'b0', 'c': 'c0', 'd': 'd0', 'e': 'e0'}
    {'a': 'a0', 'b': 'b0', 'c': 'c1', 'd': 'd1', 'e': 'e1'}
    {'a': 'a0', 'b': 'b0', 'c': 'c1', 'd': 'd1', 'e': 'e2'}
    {'a': 'a0', 'b': 'b1', 'c': 'c0', 'd': 'd0', 'e': 'e2'}
    {'a': 'a0', 'b': 'b1', 'c': 'c0', 'd': 'd1', 'e': 'e0'}
    {'a': 'a0', 'b': 'b1', 'c': 'c1', 'd': 'd0', 'e': 'e1'}
    {'a': 'a1', 'b': 'b0', 'c': 'c0', 'd': 'd0', 'e': 'e1'}
    {'a': 'a1', 'b': 'b0', 'c': 'c0', 'd': 'd1', 'e': 'e2'}
    {'a': 'a1', 'b': 'b0', 'c': 'c1', 'd': 'd0', 'e': 'e0'}
    {'a': 'a1', 'b': 'b1', 'c': 'c0', 'd': 'd1', 'e': 'e1'}
    {'a': 'a1', 'b': 'b1', 'c': 'c1', 'd': 'd0', 'e': 'e2'}
    {'a': 'a1', 'b': 'b1', 'c': 'c1', 'd': 'd1', 'e': 'e0'}
    """

    print(qt.gen_query(data3))
