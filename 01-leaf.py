# _*_ coding: utf-8 _*_
# 找到probase中的实体

def leaf():
    hypoList = []
    hypeList = []
    i = 0
    with open('data-concept-instance-relations.txt', 'r', encoding='utf-8')as f:
        for line in f.readlines():
            i += 1
            hype = line.strip().split('\t')[0]
            hypo = line.strip().split('\t')[1]
            hypoList.append(hypo)
            hypeList.append(hype)
            if i == 100000: print(i)

    hypoSet = set(hypoList)
    hypeSet = set(hypeList)
    diffSet = hypoSet - hypeSet

    with open('leaf.txt', 'w', encoding='utf-8')as f:
        for item in diffSet:
            f.write(item + '\n')

if __name__ == '__main__':
    leaf()