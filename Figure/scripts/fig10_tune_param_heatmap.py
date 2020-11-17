import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import json
import os
import pandas as pd
from matplotlib import gridspec
#         'PROJBLOCK',
#         'PROJBUFF',
#         'total_flops',
data_source='../output/result_logs.json'
res_dir='../output'

def draw_heatmap(data):
    ADS=[[] for i in range(3)]
    for dic in data:
        if 'tune' not in dic['params']['tag']:
            continue
        ADS[0].append(dic['params']['PROJBUFF'])
        ADS[1].append(dic['params']['PROJBLOCK'])
        ADS[2].append(dic['result']['total_flops'])
            
    print(len(ADS[0]))

    buffer=list(set(ADS[0]))
    buffer.sort()
    block=list(set(ADS[1]))
    block.sort()
    block.reverse()
    # print(len(buffer),len(block))
    print('buffer',buffer)
    print('block',block)
    # exit()

    heatmap_data=[[0]*len(buffer) for i in range(len(block))]
    for i in range(len(ADS[0])):
        xidx=buffer.index(ADS[0][i])
        yidx=block.index(ADS[1][i])
        heatmap_data[yidx][xidx]=ADS[2][i]

    heatmap_data=pd.DataFrame(heatmap_data)
    heatmap_data.columns=[buffer]
    heatmap_data.index=block
    return heatmap_data,block

if __name__ == "__main__":
    with open(data_source) as f:
        data = json.load(f)
    
    heatmap_data2,block2=draw_heatmap([dic for dic in data if dic['params']['arch']=='cpu' \
        and dic['params']['SPATSIZE']==32])

    heatmap_data1,block1=draw_heatmap([dic for dic in data if dic['params']['arch']=='gpu'\
        and dic['result']['total_flops']!=0
             ])

    sns.heatmap(heatmap_data1,cmap="hot",square=True)
    plt.xlabel('Buffer Size (KB)')
    plt.ylabel('Partition Size (KB)')
    plt.ylim([len(block1), 0])
    plt.title('1 SMT/Core')
    plt.show()

    # f, ax = plt.subplots(figsize=(9, 6))
    fig = plt.figure()
    spec = gridspec.GridSpec(ncols=2, nrows=1,
                         width_ratios=[1, 2])
    ax1 = fig.add_subplot(spec[0])
    ax2 = fig.add_subplot(spec[1])

    cpuax = sns.heatmap(heatmap_data1,cmap="hot",square=True,ax=ax1)
    cpuax.set_xlabel('Buffer Size (KB)')
    cpuax.set_ylabel('Partition Size (KB)')
    cpuax.set_ylim([len(block1), 0])
    cpuax.set_title('1 SMT/Core')

    gpuax = sns.heatmap(heatmap_data2,cmap="hot",square=True,ax=ax2)
    gpuax.set_xlabel('Buffer Size (KB)')
    gpuax.set_ylabel('Partition Size (KB)')
    gpuax.set_ylim([len(block2), 0])
    gpuax.set_title('P100 Performance')
    plt.tight_layout()
    plt.show()