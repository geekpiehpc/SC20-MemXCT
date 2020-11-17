
import pandas as pd
import json
import numpy as np; 
np.random.seed(0)
import seaborn as sns; 
sns.set(style="whitegrid", color_codes=True)
import matplotlib.pyplot as plt
import os

# data_source='../output/result_logs.json'
data_source='./single.json'
# res_dir='../output'

if __name__ == "__main__":
    annote_dict={}
    with open(data_source) as f:
        data = json.load(f)

    GFLOPS=[]
    BW=[]
    CPUorGPU=[]
    CDS=[]
    for pu in ['cpu','gpu']:
        for ds in ['CDS1','CDS2']:
            tmpmax_gf=0
            tmpmax_mem=0
            for dic in data:
                # if 'fix' in dic['params']['tag']:
                #     continue
                # if 'tune' not in dic['params']['tag']:
                #     continue
                if dic['params']['arch']==pu and dic['params']['DATASET']==ds:
                    if dic['result']['total_flops']>tmpmax_gf:
                        tmpmax_gf=dic['result']['total_flops']
                    if dic['result']['aver_band']>tmpmax_mem:
                        tmpmax_mem=dic['result']['aver_band']
            CPUorGPU.append(pu)
            BW.append(tmpmax_mem)
            GFLOPS.append(tmpmax_gf)
            CDS.append(ds)


    data_df=pd.DataFrame()
    data_df['CDS']=CDS
    data_df['GFLOPS']=GFLOPS
    data_df['BW']=BW
    data_df['CPUorGPU']=CPUorGPU
    print(data_df)

    for i in range(len(CDS)):
        if CDS[i]=='CDS1':
        # if CPUorGPU[i]=='cpu':
            idx=data_df[(data_df['CPUorGPU']=='cpu') & (data_df['CDS']=='CDS1')].index
            # baseline=float(data_df['GFLOPS'][idx])
            # annote_dict[GFLOPS[i]]=GFLOPS[i]/float(data_df['GFLOPS'][idx])
            # annote_dict[BW[i]]=BW[i]/float(data_df['BW'][idx])
        if CDS[i]=='CDS2':
        # if CPUorGPU[i]=='gpu':
            idx=data_df[(data_df['CPUorGPU']=='cpu') & (data_df['CDS']=='CDS2')].index
            # baseline=float(data_df['GFLOPS'][idx])
        annote_dict[GFLOPS[i]]=GFLOPS[i]/float(data_df['GFLOPS'][idx])
        annote_dict[BW[i]]=BW[i]/float(data_df['BW'][idx])
    # print(annote_dict)

    plt.subplot(121)
    # bplot=sns.barplot(x="CPUorGPU", y="GFLOPS", hue="CDS", data=data_df,\
    bplot=sns.barplot(x="CDS", y="GFLOPS", hue="CPUorGPU", data=data_df,\
        # capsize=.05,\
            ci=None\
        # ,legend=False
        )
    plt.legend(loc=7)
    # l = plt.legend()
    # l.set_title('')

    for p in bplot.patches:
        # print(p.get_x(),p.get_width(),p.get_height())
        # print(p.get_x(),p.get_width(),p.get_height())
        bplot.annotate(format(annote_dict[p.get_height()], '.2f')+'x', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'center', 
                       size=10,
                       xytext = (0, -12), 
                       textcoords = 'offset points')
    plt.xlabel('')

    plt.subplot(122)
    bplot=sns.barplot(x="CDS", y="BW", hue="CPUorGPU", data=data_df,\
        # capsize=.05,\
            ci=None\
        # ,legend=False
        )
    plt.ylabel('Memory B/W Utilization (GB/s)')
    plt.legend(loc=7)
    # l = plt.legend()
    # l.set_title('')

    for p in bplot.patches:
        if annote_dict[p.get_height()]==1:
            bplot.annotate(format(annote_dict[p.get_height()], '.2f')+'x', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'center', 
                       size=10,
                       xytext = (0, 2), 
                       textcoords = 'offset points')
        else:
            bplot.annotate(format(annote_dict[p.get_height()], '.2f')+'x', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'center', 
                       size=10,
                       xytext = (0, -12), 
                       textcoords = 'offset points')
    plt.xlabel('')
    plt.tight_layout()
    # plt.savefig(os.path.join(res_dir,'single_comparison.eps'))

    # plt.hist(data,bins=20)
    plt.show()

