# -*- coding:utf-8 -*-
import os

from flask import jsonify
from flask import redirect
from flask import render_template

from . import lfj

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = BASE_DIR + os.sep + 'files'


@lfj.route('/test/', methods=['GET'])
def test():
    return render_template('lfj/time_zone.html')


@lfj.route('/', methods=['GET'])
def index():
    return redirect('/lfj/zone/')


@lfj.route('/zone/', methods=['GET', 'POST'])
def zone():
    return render_template('lfj/zone.html')


@lfj.route('/time/', methods=['GET', 'POST'])
def time():
    return render_template('lfj/zone.html')


@lfj.route('/time_zone/', methods=['GET', 'POST'])
def time_zone():
    return render_template('lfj/time_zone.html')


@lfj.route('/api/zone_data/')
def ip_api_data():
    'echarts 图表数据接口'
    res = {'zone': ['师宗县', '罗平县', '陆良县', '曲靖市', '马龙县', '富源县', '沾益县', '宣威市', '会泽县'],
           'count': [4, 10, 1, 6, 0, 4, 0, 10, 4]
           # 'count': [4, 10, 1, 6, None, 4, None, 10, 4]
           }

    return jsonify(res)

    # filepath = FILE_PATH + os.sep + 'upload_file.xls'
    # records = {}  # date ,times
    # if os.path.isfile(filepath):
    #     data = xlrd.open_workbook(filepath)
    #     if data:
    #         col_format = ['A', 'B', 'C']  # 指定的列  ip,访问量，时间
    #         table = data.sheet_by_index(0)  # 选取第一个工作区
    #         nrows = table.nrows  # 行数
    #         ncols = table.ncols  # 列数
    #         str_upcase = [i for i in string.uppercase]  # 所有大写字母
    #         i_upcase = range(len(str_upcase))  # 对应的数字
    #         ncols_dir = dict(zip(str_upcase, i_upcase))  # 格式成字典
    #         col_index = [ncols_dir.get(i) for i in col_format]  # 获取指定列所对应的索引
    #         for i in xrange(nrows):
    #             zone = table.cell(i, col_index[0]).value  # ip
    #             times = int(table.cell(i, col_index[1]).value)  # 访问次数
    #             date = table.cell(i, col_index[2]).value  # 时间
    #             date = str(date)[:10]
    #             if records.get(date):
    #                 records[date] += times
    #             else:
    #                 records[date] = times
    # records = [(k, records[k]) for k in sorted(records.keys())]
    # for k, v in records:
    #     res['date'].append(k)
    #     res['pv'].append(v)
    # return jsonify(res)
