# _*_ coding: utf-8 _*_

from pymongo import MongoClient

client = MongoClient('10.131.247.246', 27017)
db = client.probase3

with open('leaf_positive_antonym.txt', 'r', encoding='utf-8')as f, open('leaf_positive_antonym_inProbase.txt', 'w', encoding='utf-8')as f2:
    for line in f.readlines():
        B = line.strip().split('\t')[0]
        x = line.strip().split('\t')[1]
        if db['probase'].find({'hype':B}).count() != 0 and db['probase'].find({'hype': B, 'hypo': x}).count() == 0:
            f2.write(line)
