# -*- coding:utf-8 -*-
import os

import jieba
import matplotlib.pyplot as plt
from jieba.analyse import extract_tags
from scipy.misc import imread
from wordcloud import WordCloud

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def GeneratePicture(txtname='大邓爬下来的辱母杀人评论文本', max_words=50, Picname='于欢.png'):
    path = os.getcwd()
    txtfile = path + '/' + txtname + '.txt'
    content = open(txtfile, 'r', encoding='utf-8').read()  # 评论内容
    # 根据tf-idf值找出文件中的关键词
    tags = extract_tags(content, topK=max_words)
    # 分析得到关键词的词频
    word_freq_dict = dict()
    word_list = jieba.lcut(content)
    for tag in tags:
        freq = word_list.count(tag)
        word_freq_dict[tag] = freq
    # 设置背景图片
    if Picname:
        background = path + '/' + Picname
        back_coloring = imread(background)
        font_file = path + '/' + '微软雅黑.ttf'
        wc = WordCloud(font_path=font_file,  # 设置字体
                       background_color="black",  # 背景颜色
                       max_words=max_words,  # 词云显示的最大词数
                       max_font_size=100,  # 字体最大值
                       mask=back_coloring,  # 背景图
                       random_state=42)
    else:
        font_file = path + '/' + '微软雅黑.ttf'
        wc = WordCloud(font_path=font_file,  # 设置字体
                       background_color="black",  # 背景颜色
                       max_words=max_words,  # 词云显示的最大词数
                       max_font_size=100,  # 字体最大值
                       random_state=42)
    wc.generate_from_frequencies(word_freq_dict)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()  # 绘制词云
    # 保存图片
    pic_file = path + '/' + txtname + '%d.png' % max_words
    wc.to_file(pic_file)
