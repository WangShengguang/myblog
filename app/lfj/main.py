# -*- coding:utf-8 -*-

import os
import string
import sys
from math import ceil

import xlrd
from flask import Flask, request, jsonify, redirect
from flask import render_template
from flask.ext.script import Manager

from db import cur

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
manager = Manager(app)
PER_PAGE = 50
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = BASE_DIR + os.sep + 'files'


@app.route('/')
def vpn_apps():
    "vpn应用展示"
    page = int(request.args.get('page', 1))
    app_name = request.args.get('app_name', '')
    market_id = request.args.get('market_id', '')
    category = request.args.get('category', '')
    sql = 'select name,market_id,category,version,des_url,down_url,deploy_date from vpn_data  where 1=1 '
    if app_name:
        sql += ' and name like "{}%%" '.format(app_name)
    if market_id:
        sql += ' and market_id like "{}%%" '.format(market_id)
    if category:
        sql += ' and category like "{}%%" '.format(category)
    total_page = ceil(len(cur.fetchmany(cur.execute(sql.decode('utf-8')))) / float(PER_PAGE))
    sql += " limit {page},{per_page}".format(page=(page - 1) * PER_PAGE, per_page=PER_PAGE)
    app_infos = cur.fetchmany(cur.execute(sql.decode('utf-8')))
    apps = []
    for app_info in app_infos:
        app = {'name': app_info[0], 'market_id': app_info[1], 'category': app_info[2] if app_info[2] else '',
               'version': app_info[3], 'des_url': app_info[4], 'down_url': app_info[5], 'deploy_date': app_info[6]}
        apps.append(app)
    arg = {'have_pre': False, 'have_next': False, 'cur_page': 1, 'next_page': 2, 'pre_page': 1, 'page': page,
           'app_name': app_name, 'category': category, 'market_id': market_id, 'apps': apps,
           'total_page': int(total_page)}
    if page > 1:
        arg['have_pre'] = True
    if page < arg['total_page']:
        arg['have_next'] = True
    return render_template('vpn_apps.html', **arg)


@app.route('/ip/')
def ip_stat():
    return render_template('ipstat.html')


@app.route('/api/people_data/')
def ip_api_data():
    'echarts 图表数据接口'
    res = {'date': [], 'pv': []}
    filepath = FILE_PATH + os.sep + 'upload_file.xls'
    records = {}  # date ,times
    if os.path.isfile(filepath):
        data = xlrd.open_workbook(filepath)
        if data:
            col_format = ['B', 'C', 'D']  # 指定的列  ip,访问量，时间
            table = data.sheet_by_index(0)  # 选取第一个工作区
            nrows = table.nrows  # 行数
            ncols = table.ncols  # 列数
            str_upcase = [i for i in string.uppercase]  # 所有大写字母
            i_upcase = range(len(str_upcase))  # 对应的数字
            ncols_dir = dict(zip(str_upcase, i_upcase))  # 格式成字典
            col_index = [ncols_dir.get(i) for i in col_format]  # 获取指定列所对应的索引
            for i in xrange(nrows):
                ip = table.cell(i, col_index[0]).value  # ip
                times = int(table.cell(i, col_index[1]).value)  # 访问次数
                date = table.cell(i, col_index[2]).value  # 时间
                date = str(date)[:10]
                if records.get(date):
                    records[date] += times
                else:
                    records[date] = times
    records = [(k, records[k]) for k in sorted(records.keys())]
    for k, v in records:
        res['date'].append(k)
        res['pv'].append(v)
    return jsonify(res)


@app.route('/ip/upload/', methods=['POST', 'GET'])
def ip_upload():
    "将上传文件保存到files文件夹下"
    file = request.files.get('upload_file.xls')
    if not os.path.exists(FILE_PATH):
        os.mkdir(FILE_PATH)
    file.save(FILE_PATH + os.sep + 'upload_file.xls')
    return redirect('/ip/?a=2')


if __name__ == '__main__':
    manager.run()
