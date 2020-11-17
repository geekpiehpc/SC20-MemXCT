import json 
import seaborn
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts
import seaborn as sns
import pandas as pd

data_source='../output/strong_multinode.json'
res_dir='../output'

def Draw_ADS(CDS,NP,ax,dataset):
    # print(CDS)
    ax.set_adjustable("datalim")
    ax.grid(True,which="both", linestyle='--')
    CDSdf=pd.DataFrame({'recon':CDS[3],'Ap':CDS[0],'C':CDS[1],'R':CDS[2],'x':NP})
    sns.lineplot(x='x',y='recon',data=CDSdf,label='Total',ax=ax)
    sns.scatterplot(x='x',y='recon',data=CDSdf,ax=ax)

    sns.lineplot(x='x',y='Ap',data=CDSdf,label='${A_p}$',ax=ax)
    sns.scatterplot(x='x',y='Ap',data=CDSdf,ax=ax)

    sns.lineplot(x='x',y='C',data=CDSdf,label='C',ax=ax)
    sns.scatterplot(x='x',y='C',data=CDSdf,ax=ax)

    sns.lineplot(x='x',y='R',data=CDSdf,label='R',ax=ax)
    sns.scatterplot(x='x',y='R',data=CDSdf,ax=ax)

    ax.legend()
    ax.set_xticks(NP)
    ax.set_yscale("log")
    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Solution Time(s)')
    ax.set_title(dataset+' strong scaling')

with open(data_source) as f:
    data = json.load(f)

CDS1=[[] for i in range(4)]
CDS2=[[] for i in range(4)]
CDS3=[[] for i in range(4)]
NP1=[]
NP2=[]
NP3=[]

data.reverse()
for dic in data:
    if dic['params']['DATASET']=='CDS1' and dic['params']['SPATSIZE']==32 and dic['params']['PROJBLOCK']==32:
        NP1.append(dic['params']['NP']//60)
        # Ap
        CDS1[0].append(dic['times']['proj_calc']+dic['times']['back_calc'])
        # C
        CDS1[1].append(dic['times']['proj_alltoall']+dic['times']['back_alltoall'])
        # R
        CDS1[2].append(dic['times']['proj_reduce']+dic['times']['back_reduce'])
        # reconstruction time(total)
        CDS1[3].append(dic['times']['recon'])

    elif dic['params']['DATASET']=='CDS2' and dic['params']['SPATSIZE']==32 and dic['params']['PROJBLOCK']==32:
        NP2.append(dic['params']['NP']//60)
        CDS2[0].append(dic['times']['proj_calc']+dic['times']['back_calc'])
        CDS2[1].append(dic['times']['proj_alltoall']+dic['times']['back_alltoall'])
        CDS2[2].append(dic['times']['proj_reduce']+dic['times']['back_reduce'])
        CDS2[3].append(dic['times']['recon'])
    elif dic['params']['DATASET']=='CDS3' and dic['params']['SPATSIZE']==64 and dic['params']['PROJBLOCK']==256:
        NP3.append(dic['params']['NP']//60)
        CDS3[0].append(dic['times']['proj_calc']+dic['times']['back_calc'])
        CDS3[1].append(dic['times']['proj_alltoall']+dic['times']['back_alltoall'])
        CDS3[2].append(dic['times']['proj_reduce']+dic['times']['back_reduce'])
        CDS3[3].append(dic['times']['recon'])


# fig = plt.figure()

fig, axes = plt.subplots(1,3)
ax1=axes[0]
ax2=axes[1]
ax3=axes[2]
Draw_ADS(CDS1,NP1,ax1,dataset='CDS1')
Draw_ADS(CDS2,NP2,ax2,dataset='CDS2')
Draw_ADS(CDS3,NP3,ax3,dataset='CDS3')
ax3.legend_.remove() 
ax2.legend_.remove() 

plt.draw()
plt.tight_layout()
plt.savefig(os.path.join(res_dir,'strong_scaling_multi_node.eps'),bbox_inches='tight')
plt.show()