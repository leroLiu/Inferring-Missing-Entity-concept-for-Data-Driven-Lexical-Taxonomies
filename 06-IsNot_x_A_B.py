# _*_ coding: utf-8 _*_

from pymongo import MongoClient

client = MongoClient('10.131.247.246', 27017)
db = client.probase3
with open('IsNot_dataset.txt', 'r', encoding='utf-8')as f, open('IsNot_x_A_B.txt', 'w', encoding='utf-8')as f1:
    for line in f.readlines():
        B = line.strip().split('\t')[0]
        x = line.strip().split('\t')[1]
        for item in db['probase'].find({'hypo':x}).sort('freq', -1):
            hype = item.get('hype')
            f1.write(x + '\t' + hype + '\t' + B + '\n')
            break