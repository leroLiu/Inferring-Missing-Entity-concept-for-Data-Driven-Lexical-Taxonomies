'''
若两个entity的hypernyms都与概念的子节点个数都为0，则肯定不存在isA的关系
'''
import time,random
import multiprocessing

def keyPe():
    with open('data-concept-instance-relations.txt', 'r', encoding='utf-8')as fin:
        probase = {}
        i = 0
        for line in fin.readlines():
            hype = line.strip().split('\t')[0]
            hypo = line.strip().split('\t')[1]
            if hype in probase:
                probase[hype].append(hypo)
            else:
                probase[hype] = [hypo]

            i += 1
            if i % 100000 == 0:print(i)
    return probase

def mutex(probase, concept,entity_hype, i):
    print("jigncheng:", i)
    j = 0
    with open('new_relation.txt', 'a', encoding='utf-8') as f2:
        for line1 in entity_hype[i]:
            line1 = line1.split('\t')
            for item in concept:
                if len(set(probase[line1[1]]) & set(probase[item])) >= 1 or len(set(probase[line1[2]]) & set(probase[item])) >= 1:
                    f2.write(line1[0] + '\t' + item + '\n')
                    f2.flush()
            j += 1
            print('进程',i, ': ', '第', j, '个', '-->')


if __name__ == '__main__':
    probase = multiprocessing.Manager().dict()
    probase = keyPe()
    for key in probase.keys():
        if len(probase[key]) > 100:
            probase[key] = random.sample(probase[key],100)
    concept = multiprocessing.Manager().list()
    with open('concept.txt', 'r', encoding='utf-8')as f:
        for line in f.readlines():
            concept.append(line.strip())
    entity_hype = multiprocessing.Manager().list()
    with open('entity_hypernyms.txt', 'r', encoding='utf-8')as f1:
        for line1 in f1.readlines():
            entity_hype.append(line1.strip())
    pro = 10
    n = int(len(entity_hype) / 10)
    entity_hype = [entity_hype[i:i + n] for i in range(0, len(entity_hype), n)]                 #entity_hype是要分割的list，n是每份多少个
    for i in range(pro):
        print(len(entity_hype[i]))
    pool = multiprocessing.Pool(processes=pro)
    for i in range(pro):
        pool.apply_async(mutex, (probase, concept, entity_hype, i))
    pool.close()
    pool.join()
    print('Sub-process(es) done.')
    # mutex(probase, concept, entity_hype, 0)