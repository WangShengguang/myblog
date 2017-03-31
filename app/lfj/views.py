# -*- coding:utf-8 -*-
import os

from flask import jsonify
from flask import redirect
from flask import request
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


@lfj.route('/gdp/', methods=['GET', 'POST'])
def gdp():
    return render_template('lfj/gdp.html')


@lfj.route('/time_zone/', methods=['GET', 'POST'])
def time_zone():
    return render_template('lfj/time_zone.html')


@lfj.route('/api/zone_data/')
def ip_api_data():
    'echarts 图表数据接口'
    res = {'zone': ["师宗县", "罗平县", "陆良县", "曲靖市", "马龙县", "富源县", "沾益县", "宣威市", "会泽县"],
           'count': [4, 10, 1, 6, 0, 4, 0, 10, 4]  # 2000
           # 'count': [4, 10, 1, 6, None, 4, None, 10, 4]
           }

    return jsonify(res)


@lfj.route('/api/gdp_data/<arg>')
def gdp_api_data(arg):
    """
    echarts 图表数据接口'
    "人均GDP,平均寿命,人口,国家,年份"
    [9430, 75.9, 1340968737, "陆良县", 2010]
    """
    sum_gdps = [52, 78, 95, 270, 23, 112, 96, 148, 95]  # 亿元
    ave_gdps = [1.4, 1.4, 1.5, 3.9, 1.2, 1.5, 2.3, 1.1, 1.1]  # 万
    gdps = ave_gdps if 'ave' in arg else sum_gdps
    zones = [u"师宗县", u"罗平县", u"陆良县", u"曲靖市", u"马龙县", u"富源县", u"沾益县", u"宣威市", u"会泽县"]
    peoples = [38, 55, 62, 68, 20, 74, 41, 142, 94]  # 万人
    counts = [7, 24, 3, 9, 0, 11, 0, 37, 0]  # 2010
    oneyear = []
    for gdp, age_ave, people, zone in zip(gdps, counts, peoples, zones):
        oneyear.append([gdp, age_ave, people, zone, 2010])
    res = {'counties': zones, 'timeline': [2010], 'series': [oneyear]}
    return jsonify(res)
