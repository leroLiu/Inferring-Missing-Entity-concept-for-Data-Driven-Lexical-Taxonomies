# _*_ coding: utf-8 _*_

def k(x):
    return int(x.strip().split('\t')[2])

with open('IsA_dataset.txt', 'r', encoding='utf-8')as f, open('Is_x_A_B.txt', 'w', encoding='utf-8')as fout,open('leaf_positive_rel.txt','r', encoding='utf-8') as fin:
    count = fin.readlines()
    count.sort(key = k,reverse = True)
    xs = []
    for each in count:
        xs.append(each.strip().split('\t')[1])
    for line in f.readlines():
        B = line.strip().split('\t')[0]
        x = line.strip().split('\t')[1]
        tar = xs.index(x)
        del count[tar]
        del xs[tar]
        tar = xs.index(x)
        fout.write(x + '\t' + count[tar].strip().split('\t')[0]+ '\t' + B + '\n')
