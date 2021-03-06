# -*- coding: utf-8 -*-

# Define here the models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_cfg = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'password',
    'db': 'flask ',
}

# 初始化数据库连接:
test_engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}'.format(**db_cfg))

# 创建DBSession类型:
TestDBSession = sessionmaker(bind=test_engine)
# create database test
