# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

from connect import test_engine, TestDBSession
import random

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Ips(Base):
    # 表的名字:
    __tablename__ = 'ips_static'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    ip = Column(String(125), unique=True)
    count = Column(Integer(), default=0)
    date = Column(DateTime, default=datetime.utcnow())


Base.metadata.create_all(test_engine)  # 创建表

if __name__ == '__main__':
    # '生成假数据，辅助开发'
    test_conn = test_engine.connect()
    session = TestDBSession()
    for i in range(200):
        a = str(random.randint(0, 256))
        date = '-'.join(['2017', '3', str(random.randint(1, 31))]) + ' 00:00:00'
        one_record = Ips(ip='.'.join([a, a, a, a]), count=random.randint(0, 1000), date=date)
        session.add(one_record)
        try:
            session.commit()
        except:
            session.rollback()
    pass
