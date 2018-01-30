#!usr/bin/env python3
# -*- coding:utf-8 -*-

i = 0
with open(r'D:\ljp\data-concept-instance-relations.txt', 'r') as fin,open(r'C:\Users\liujingping\Desktop\周元辅\relation.txt','w') as fout:
    for line in fin.readlines():
        # print(line)
        fre = line.split('\t')[2]
        if int(fre) < 4:
            break
        i += 1
        fout.write(line)
print('relation:' + str(i))