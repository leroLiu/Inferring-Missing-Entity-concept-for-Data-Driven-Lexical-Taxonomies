#!usr/bin/env python3
# -*- coding:utf-8 -*-

from numpy import *
import datetime
import multiprocessing
import sys

def load():
    with open('data-concept-instance-relations.txt', 'r')as f:
        pro_dic_o = {}
        pro_dic_e = {}
        for line in f.readlines():
            # print(line)
            hypo = line.split('\t')[1]
            hype = line.split('\t')[0]
            if hypo in pro_dic_o:
                pro_dic_o.get(hypo).append(hype)
            else:
                pro_dic_o[hypo] = [hype]
            if hype in pro_dic_e:
                pro_dic_e.get(hype).append(hypo)
            else:
                pro_dic_e[hype] = [hypo]
    return pro_dic_e,pro_dic_o

def gene_ver(A, B, modeA,modeB,pro_dic_e,pro_dic_o):
    if modeA == 'hype':
        try:
            A_l = pro_dic_o[A]
        except:
            A_l = []
    else:
        try:
            A_l = pro_dic_e[A]
        except:
            A_l = []
    if modeB == 'hype':
        try:
            B_l = pro_dic_o[B]
        except:
            B_l = []
    else:
        try:
            B_l = pro_dic_e[B]
        except:
            B_l = []
    inter = set(A_l) & set(B_l)
    oa = set(A_l) - set(B_l)
    ob = set(B_l) - set(A_l)
    c1 = [[1] * (len(inter) + len(oa))][0] + [[0] * len(ob)][0]
    c2 = [[1] * len(inter)][0] + [[0] * len(oa)][0] + [[1] * len(ob)][0]
    return array(c1),array(c2)

def cosi(v1, v2):
    dot_product = dot(v1, v2)
    norm1 = linalg.norm(v1)
    norm2 = linalg.norm(v2)
    return dot_product / (norm1 * norm2)

def intersec(v1,v2):
    return dot(v1,v2)

def un(v1,v2):
    k = 0
    for m in range(v1.__len__()):
        if v1[m] == 1 or v2[m] == 1:
            k += 1
    return k

def vabs(v):
    return dot(v,array([[1] * v.__len__()][0]))

def sim(v1,v2,v3,v4):
    if linalg.norm(v1) == 0 or linalg.norm(v2) == 0:
        c1 = 0
    else:
        c1 = cosi(v1,v2)
    if linalg.norm(v3) == 0 or linalg.norm(v4) == 0:
        c2 = 0
    else:
        c2 = cosi(v3,v4)
    return 1 - (1 - c1) * (1 - c2)

def func(msg,pro_dic_e,pro_dic_o, p,i):
    print(msg)
    qwe = 0
    with open('IsA_x_A50_B_similarity.txt', 'a', encoding='utf-8')as fout, open('test_IsA_x_A50_B.txt', 'a', encoding='utf-8')as test:
        for each in p[i]:
            # try:
            # start = datetime.datetime.now()
            if each.strip().split('\t').__len__() == 4:
                x = each.strip().split('\t')[0]
                A = each.strip().split('\t')[1]
                B = each.strip().split('\t')[2]
            else:
                test.write(x + '\t' + A + '\t' + B + '\t@@@\n')
                continue

            v1, v2 = gene_ver(A, B, 'hypo', 'hypo',pro_dic_e,pro_dic_o)
            buf = intersec(v1, v2)
            first = buf / vabs(v1)
            v3, v4 = gene_ver(A, B, 'hype', 'hype',pro_dic_e,pro_dic_o)
            second = sim(v1,v2,v3,v4)

            try:
                A_set = set(pro_dic_e[A])
            except:
                A_set = set()
            try:
                x_set = set(pro_dic_o[x])
            except:
                x_set = set()
            Bi = A_set & x_set
            sum = 0
            if len(Bi) == 0:
                third = 0
            else:
                for each_Bi in Bi:
                    v1, v2 = gene_ver(each_Bi, B, 'hype', 'hype',pro_dic_e,pro_dic_o)
                    v3, v4 = gene_ver(each_Bi, B, 'hypo', 'hypo',pro_dic_e,pro_dic_o)
                    sum += sim(v1, v2, v3, v4)
                third = sum / len(Bi)

            try:
                A_set = set(pro_dic_o[A])
            except:
                A_set = set()
            try:
                x_set = set(pro_dic_o[x])
            except:
                x_set = set()
            Bi = A_set & x_set
            sum = 0
            if len(Bi) == 0:
                forth = 0
            else:
                for each_Bi in Bi:
                    v1, v2 = gene_ver(each_Bi, B, 'hype', 'hype',pro_dic_e,pro_dic_o)
                    v3, v4 = gene_ver(each_Bi, B, 'hypo', 'hypo',pro_dic_e,pro_dic_o)
                    sum += sim(v1, v2, v3, v4)
                forth = sum / len(Bi)
            # end = datetime.datetime.now()
            fout.write(x + '\t' + A + '\t' + B + '\t' + str(first) + '\t' + str(second) + '\t' + str(third) + '\t' + str(
                forth) + '\n')
            qwe += 1
            if qwe%1000 == 0:
                print(qwe + 'done')
            # print(x + '\t' + A + '\t' + B + '\t' + str(first) + '\t' + str(second) + '\t' + str(third) + '\t' + str(forth))
            test.write(x + '\t' + A + '\t' + B + '\t$$$\n')
            # except:
            #     test.write(x + '\t' + A + '\t' + B + '\t@@@\n')
            #     print(A + '\t' + B + '\t' + x)
    print('done' + msg)

if __name__ == '__main__':
    with open('IsA_x_A50_B.txt', 'r', encoding='utf-8')as fin:
        pro = 10    #进程数量
        pro_dic_e = multiprocessing.Manager().dict()  # 主进程与子进程共享这个字典
        pro_dic_o = multiprocessing.Manager().dict()
        pro_dic_e, pro_dic_o = load()
        p = multiprocessing.Manager().list()
        allin = fin.readlines()
        raws = allin.__len__()
        pace = int(raws/pro)
        for i in range(pro):
            if i == 0:
                head = 0
            else:
                head = tail
            tail = head + pace
            if i == 9:
                p.append(allin[head:])
            else:
                p.append(allin[head:tail])
        pool = multiprocessing.Pool(processes=pro)
        for i in range(pro):
            msg = 'hello %d' % (i)
            pool.apply_async(func, (msg,pro_dic_e,pro_dic_o, p,i))
        pool.close()
        pool.join()
        print('Sub-process(es) done.')