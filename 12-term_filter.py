#!usr/bin/env python3
# -*- coding:utf-8 -*-

def load():
    with open(r'C:\Users\liujingping\Desktop\周元辅\relation.txt', 'r')as f:
        pro_dic_o = {}
        pro_dic_e = {}
        count = {}
        sete = set()
        seto = set()
        for line in f.readlines():
            # print(line)
            hypo = line.split('\t')[1]
            hype = line.split('\t')[0]
            if hypo in pro_dic_o:
                pro_dic_o.get(hypo).append(hype)
            else:
                pro_dic_o[hypo] = [hype]
                seto.add(hypo)
            if hype in pro_dic_e:
                pro_dic_e.get(hype).append(hypo)
            else:
                pro_dic_e[hype] = [hypo]
                sete.add(hype)
            if hypo in count:
                count[hypo][0] += 1
            else:
                count[hypo] = [1,True]
            if hype in count:
                count[hype][0] += 1
            else:
                count[hype] = [1,True]
    return pro_dic_e,pro_dic_o,count,sete,seto

if __name__ == '__main__':
    thresh = 10
    pro_dic_e, pro_dic_o, count,sete,seto = load()

    with open(r'C:\Users\liujingping\Desktop\周元辅\two.txt','w') as fout:
        for key, value in pro_dic_o.items():
            if value.__len__() == 2:
                fout.write(key + '\t' + str(value) + '\n')

    flag = True
    while(flag):
        flag = False
        for key,value in count.items():
            if value[1] and value[0] < thresh:
                try:
                    for each in pro_dic_e[key]:
                        count[each][0] -= 1
                    sete.remove(key)
                except:
                    pass
                try:
                    for each in pro_dic_o[key]:
                        count[each][0] -= 1
                    seto.remove(key)
                except:
                    pass
                value[1] = False
                flag = True
    print('entity:' + str((seto - sete).__len__()))
    print('concept:' + str(sete.__len__() + seto.__len__() - 2 * (seto - sete).__len__() ))
    entity = seto - sete
    concept = sete | seto - entity
    with open(r'C:\Users\liujingping\Desktop\周元辅\entity.txt','w') as f:
        for each in entity:
            f.write(each + '\n')
    with open(r'C:\Users\liujingping\Desktop\周元辅\concept.txt','w') as f:
        for each in concept:
            f.write(each + '\n')
