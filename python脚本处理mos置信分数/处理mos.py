import json
import numpy as np
from scipy.linalg import solve
from scipy.stats import t
# 计算mos分数
def calc_mos(data, i):
    '''
    计算MOS，data为MxN的列表，M个句子，N个试听人，内容为每个试听的得分
    :param data:
    :return:
    '''
    data = data.astype(np.float64)
    # 计算MOS分数的均值（志愿者人数，句子数）
    mu = np.mean(data)
    # 计算每个句子分数的方差（志愿者人数，句子数）
    var_uw = (np.std(data, axis=1) ** 2).mean()
    # 计算每个试听人的句子分数的方差（志愿者人数，句子数）
    var_su = (np.std(data, axis=0) ** 2).mean()
    mos_data = data.flatten()
    mos_data = mos_data[~np.isnan(mos_data)]
    # 计算整体评分数据的方差，即样本与总体之间的方差。
    var_swu = mos_data.std() ** 2

    x = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 1]])
    y = np.array([var_uw, var_su, var_swu])
    [var_s, var_w, var_u] = solve(x, y)
    M = min(data.shape)
    N = min(data.shape)
    var_mu = var_s / M + var_w / N + var_u / (M * N)
    df = min(M, N) - 1  # 可以不减1
    t_interval = t.ppf(0.95, df, loc=0, scale=1)  # t分布的95%置信区间临界值
    interval = t_interval * np.sqrt(var_mu)
    print('第{}个模型的MOS的95%置信区间为：{} +—{}'.format(i + 1,round(float(mu), 3), round(interval, 3)))
    return 'MOS的95%置信区间为：{} +—{}'.format(round(float(mu), 3), round(interval, 3))


# 存储打分人姓名
names = ['xxx1', 'xxx2']

# 保存最终计算时的格式
mos_list_n = []
mos_list_score2 = []

# 读取每个人的打分情况
for name in names: # 遍历每个人的名字

    # 读取 JSON 文件，指定编码格式为 utf-8
    with open('分数文件/' + name + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 每个人 (句子， 模型)
    score1 = np.array(data['score1'])
    score2 = np.array(data['score2'])

    mos_list_n.append(score1)
    mos_list_score2.append(score2)


# 目前结构： （人， 句子， 模型）
mos_list_n = np.stack(mos_list_n)
mos_list_score2 = np.stack(mos_list_score2)

# 转置为 (模型，人，句子)的维度
mos_list_n = np.transpose(mos_list_n, (2, 0, 1))  # 将第1个维度与第2个维度交换位置
mos_list_score2 = np.transpose(mos_list_score2, (2, 0, 1))  # 将第1个维度与第2个维度交换位置


# 计算mos分数
print("----------------------------------------n-dmos----------------------------------------")
for i in range(mos_list_n.shape[0]):
    calc_mos(mos_list_n[i], i)
print("----------------------------------------dmos2----------------------------------------")
for i in range(mos_list_score2.shape[0]):
    calc_mos(mos_list_score2[i], i)