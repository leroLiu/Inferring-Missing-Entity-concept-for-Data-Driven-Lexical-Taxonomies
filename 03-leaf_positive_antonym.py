#!usr/env/bin python3
#-*- coding:utf-8 -*-

from nltk.corpus import wordnet as wn

with open(r'C:\Users\刀轻城\Desktop\数据记录\leaf_positive_rel.txt', 'r', encoding='utf-8')as fin,open(r'C:\Users\刀轻城\Desktop\数据记录\leaf_positive_antonym.txt', 'w', encoding='utf-8')as fout,open(r'C:\Users\刀轻城\Desktop\数据记录\test.txt', 'w', encoding='utf-8') as test:
    for line in fin.readlines():
        nl = []
        l = line.strip().split('\t')
        if l.__len__() == 3:
            hype,x = l[0],l[1]
            l = wn.synsets(hype)
            for each in l:
                syn = each.lemmas()
                for each_s in syn:
                    al = each_s.antonyms()
                    for each_a in al:
                        nl.append(each_a.name())
            nl = set(nl)
            for each in nl:
                fout.write(each + '\t' + x + '\n')
            test.write(hype + '\t' + x + '\t' + '$$$\n')
            continue
        test.write(hype + '\t' + x + '\t' + '@@@\n')
