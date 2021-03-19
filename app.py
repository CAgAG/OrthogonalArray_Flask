import os
import openpyxl

from flask import Flask, render_template, request, jsonify, session, url_for, redirect

from orthogonal_table import QueryTable

app = Flask(__name__)

# session 密钥
app.config['SECRET_KEY'] = '123456'


@app.route('/')
def index():
    session['filepath'] = ''
    return render_template('exp_index.html')


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')
        filename = file.filename
        file.save(f'./media/{filename}')
        session['filepath'] = f'./media/{filename}'
    except Exception:
        return {
            'code': 1,
            'msg': '上传失败',
            'data': {}
        }
    ctx = {
        "code": 0
        , "msg": "上传成功"
        , "data": {
            'filename': filename
        }
    }
    return jsonify(ctx)


@app.route('/show', methods=['GET'])
def show():
    filepath = session.get('filepath', '')
    if (filepath == '') or (not os.path.exists(filepath)):
        return redirect(url_for('index'))

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

    os.remove(filepath)

    ctx = {
        'data': rets
    }
    return render_template('show_exp.html', **ctx)


if __name__ == '__main__':
    app.run()
