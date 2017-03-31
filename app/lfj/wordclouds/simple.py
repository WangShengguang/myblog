#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

import os
from os import path

import matplotlib.pyplot as plt
from wordcloud import WordCloud

d = path.dirname(__file__)

font = os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")

# Read the whole text.
# text = open(path.join(d, 'constitution.txt')).read()
text = open(u"santi.txt").read().decode('gbk')

# Generate a word cloud image
wordcloud = WordCloud(font_path=font).generate(text)

# Display the generated image:
# the matplotlib way:

plt.imshow(wordcloud)
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(font_path=font, max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()
