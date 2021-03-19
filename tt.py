import openpyxl

from orthogonal_table import QueryTable

if __name__ == '__main__':
    filepath = './media/新建 Microsoft Excel 工作表.xlsx'

    workbook = openpyxl.load_workbook(filepath)
    worksheet = workbook['Sheet1']

    input_data = []
    for columns in worksheet.columns:
        t_list = []
        for index, cell in enumerate(columns):
            if index == 0:
                t_list.append(cell.value)
                t_list.append([])
            else:
                t_list[1].append(cell.value)
        input_data.append(t_list)
    qt = QueryTable()
    rets = qt.solve(input_data)

    for r in rets:
        print(r)