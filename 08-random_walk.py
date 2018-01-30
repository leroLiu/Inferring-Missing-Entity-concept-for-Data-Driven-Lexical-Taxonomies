import numpy as np
import json,time


def keyPe():
    with open('data-concept-instance-relations.txt', 'r', encoding='utf-8')as fin:
        probase_keyIsHype = {}
        probase_keyIsHypo = {}
        for line in fin.readlines():
            hype = line.strip().split('\t')[0]
            hypo = line.strip().split('\t')[1]
            if hype in probase_keyIsHype:
                probase_keyIsHype.get(hype).append(hypo)
            else:
                probase_keyIsHype[hype] = [hypo]

            if hypo in probase_keyIsHypo:
                probase_keyIsHypo.get(hypo).append(hype)
            else:
                probase_keyIsHypo[hypo] = [hype]
    return probase_keyIsHype, probase_keyIsHypo



def init(M_Init, AB_father_father_list):
    #*******************************************************************************************************************
    #得到归一化的矩阵M 和 向量X_A 向量X_B
    M_H = M_Init[0:len(AB_father_father_list),0:len(AB_father_father_list)]
    M = M_H.T
    #归一化
    M_sqrt =np.sqrt(M)
    M_col_sum = M.sum(axis = 0)
    M_col_sum_sqrt = np.sqrt(M_col_sum)
    M_normalizetion = M/M_col_sum_sqrt

    X_A = np.zeros(len(AB_father_father_list),dtype= int)
    X_A[0] = 1
    X_B = np.zeros(len(AB_father_father_list),dtype= int)
    X_B[1] = 1
    return M_normalizetion, X_A, X_B

def distribution(M_normalizetion, X_A, X_B):
    #*******************************************************************************************************************
    #求矩阵M_normalizetion*M_normalizetion*X_A      M_normalizetion*M_normalizetion*X_B的概率分布
    M_normalizetion =np.matrix(M_normalizetion)
    X_A =np.matrix(X_A).T
    X_B = np.matrix(X_B).T
    M_A = M_normalizetion * X_A
    M_B = M_normalizetion * X_B
    M_A = M_normalizetion * M_A
    M_B = M_normalizetion * M_B
    return M_A, M_B


def cosi(M_A,M_B):
    # 求M_A和M_B向量的cos值
    up = sum(np.multiply(M_A,M_B))
    M_A_Sum_sqrt = np.sqrt(sum(np.multiply(M_A,M_A)))
    M_B_Sum_sqrt = np.sqrt(sum(np.multiply(M_B,M_B)))
    cos =up/(M_A_Sum_sqrt*M_B_Sum_sqrt)
    return cos

def cal_node(temp_A, temp_B, child_father, child_father_keys):

    M_Init = np.zeros((30000, 30000), dtype=int)
    temp_A_father = child_father[temp_A]  # A的所有父亲
    AB_father_father_list = []
    AB_father_father_list.append(temp_A)  # 添加A，并修改M_Init对应位置权重
    M_Init[len(AB_father_father_list) - 1][len(AB_father_father_list) - 1] = 1
    AB_father_father_list.append(temp_B)  # 添加B，并修改M_Init对应位置权重
    M_Init[len(AB_father_father_list) - 1][len(AB_father_father_list) - 1] = 1
    A_father_number = 0
    B_father_number = 0

    # *******************************************************************************************************************
    # 处理A的所有父亲结点，以及A的父亲的父亲结点。添加到AB_father_father_list中去，并修改M对应位置的权重
    for every_temp_A_father in temp_A_father:
        if A_father_number < 50:  # 只取A前十个父亲结点
            A_father_number += 1
            # A的所有父亲添加到AB_father_father_list里面去，并修改矩阵M中对应的权重
            if every_temp_A_father not in AB_father_father_list:
                AB_father_father_list.append(every_temp_A_father)
                M_Init[len(AB_father_father_list) - 1][len(AB_father_father_list) - 1] = 1
                M_Init[0][len(AB_father_father_list) - 1] = 1
            else:
                M_Init[0][AB_father_father_list.index(every_temp_A_father)] = 1  # 矩阵M中M[0][所在索引]权重变为1

            if every_temp_A_father not in child_father_keys:
                continue
            temp_A_father_father = child_father[every_temp_A_father]  # A父亲的父亲
            A_father_father_number = 0
            for every_A_father_father in temp_A_father_father:
                if A_father_father_number < 50:
                    A_father_father_number += 1
                    if every_A_father_father not in AB_father_father_list:  # A父亲的父亲加入矩阵中，并修改M对应权重
                        AB_father_father_list.append(every_A_father_father)
                        M_Init[len(AB_father_father_list) - 1][len(AB_father_father_list) - 1] = 1
                        M_Init[AB_father_father_list.index(every_temp_A_father)][len(AB_father_father_list) - 1] = 1
                    else:
                        M_Init[AB_father_father_list.index(every_temp_A_father)][
                            AB_father_father_list.index(every_A_father_father)] = 1
                else:
                    break
        else:
            break
    # *******************************************************************************************************************
    # 处理B的所有父亲结点，以及B的父亲的父亲结点。添加到AB_father_father_list中去，并修改M对应位置的权重

    temp_B_father = child_father[temp_B]  # B的所有父亲
    for every_temp_B_father in temp_B_father:
        if B_father_number < 50:  # 只取B前十个父亲结点
            B_father_number += 1
            # B的所有父亲添加到AB_father_father_list里面去，并修改矩阵M中对应的权重
            if every_temp_B_father not in AB_father_father_list:
                AB_father_father_list.append(every_temp_B_father)
                M_Init[len(AB_father_father_list) - 1][len(AB_father_father_list) - 1] = 1
                M_Init[1][len(AB_father_father_list) - 1] = 1
            else:
                M_Init[1][AB_father_father_list.index(every_temp_B_father)] = 1  # 矩阵M中M[0][所在索引]权重变为1

            if every_temp_B_father not in child_father_keys:
                continue
            temp_B_father_father = child_father[every_temp_B_father]  # B父亲的父亲
            B_father_father_number = 0
            for every_B_father_father in temp_B_father_father:
                if (B_father_father_number < 50):
                    B_father_father_number += 1
                    if every_B_father_father not in AB_father_father_list:
                        AB_father_father_list.append(every_B_father_father)
                        M_Init[len(AB_father_father_list) - 1][len(AB_father_father_list) - 1] = 1
                        M_Init[AB_father_father_list.index(every_temp_B_father)][len(AB_father_father_list) - 1] = 1
                    else:
                        M_Init[AB_father_father_list.index(every_temp_B_father)][
                            AB_father_father_list.index(every_B_father_father)] = 1
                else:
                    break
        else:
            break
    return M_Init, AB_father_father_list


if __name__ == '__main__':
    father_child, child_father = keyPe()
    child_father_keys = child_father.keys()
    father_child_keys = father_child.keys()
    with open('IsA_A_B.txt', 'r', encoding='utf-8')as f1:
        IsNotAB_data = f1.read()
    IsNotAB_data_value = IsNotAB_data.split('\n')
    i = 0
    with open('Is_randomwlak(50).txt', 'w', encoding='utf-8')as fw:
        for IsNotAB_data_line in IsNotAB_data_value:
            # start = time.clock()
            i += 1
            if i % 1000 == 0:print(i)
            temp_AB_value = IsNotAB_data_line.split('\t')
            if len(temp_AB_value) < 2:
                continue
            temp_A = temp_AB_value[0]
            temp_B = temp_AB_value[1]

            if temp_A not in child_father_keys or temp_B not in child_father_keys:
                cos1 = 0
            else:
                M_Init, AB_father_father_list = cal_node(temp_A, temp_B, child_father, child_father_keys)
                M_normalizetion, X_A, X_B = init(M_Init, AB_father_father_list)
                M_A_hype, M_B_hype = distribution(M_normalizetion, X_A, X_B)
                cos1 = cosi(M_A_hype, M_B_hype)

            # print('*************************')
            # print(temp_A, ' and ', temp_B, ' cos is: ', cos1)

            if temp_A not in father_child_keys or temp_B not in father_child_keys:
                cos2 = 0
            else:
                M_Init, AB_father_father_list = cal_node(temp_A, temp_B, father_child, father_child_keys)
                M_normalizetion, X_A, X_B = init(M_Init, AB_father_father_list)
                M_A_hypo, M_B_hypo = distribution(M_normalizetion, X_A, X_B)
                cos2 = cosi(M_A_hypo, M_B_hypo)

            # print(temp_A, ' and ', temp_B, ' cos is: ', cos2)

            cos3 = (cos1 + cos2) / 2
            # print(temp_A, ' and ', temp_B, ' cos is: ', cos3)
            # end = time.clock()
            # print(end - start)
            # print(IsNotAB_data_line.strip(), ' ', cos3[0])
            # print('*************************')
            fw.write(IsNotAB_data_line.strip() + '\t' + str(np.array(cos3)[0][0]) + '\n')