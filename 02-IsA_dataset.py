from pymongo import MongoClient

client = MongoClient('10.131.247.246', 27017)
db = client.probase3

def k(x):
    return int(x.strip().split('\t')[2])

i = 0
with open(r'C:\Users\刀轻城\Desktop\数据记录\IsA_dataset.txt', 'w', encoding='utf-8')as fout,open(r'C:\Users\刀轻城\Desktop\数据记录\leaf_positive_rel.txt','r', encoding='utf-8') as fin:
    lines = fin.readlines()
    xs = []
    for each in lines:
        xs.append(each.strip().split('\t')[1])
    lines.sort(key = k,reverse = True)
    for item in lines:
        if i == 14259: break
        x = item.strip().split('\t')[1]
        B = item.strip().split('\t')[0]
        if xs.count(x)> 1:
            i += 1
            fout.write(B + '\t'+ x + '\n')