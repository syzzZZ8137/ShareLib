# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 16:13:34 2018

@author: Jax_GuoSen
"""
from MonthStat import * 
from PentagonStat import * 
import os
import numpy as np
import matplotlib.pyplot as plt


data1 = PentagonStat('20180614')
data2 = MothStat('2012')



os.chdir("D:\\工作\\期货市场量化研报\\雷达图")
#=======自己设置开始============
#标签
labels = np.array(['持仓量比','涨跌幅','振幅','成交额比','成交量比'])
dataLenth = 5

for i in range(len(data1)):
    
    #数据
    data = np.array([data1.loc[i,'Zoi_ratio'],data1.loc[i,'Zpct_chg_abs'],data1.loc[i,'Zswing'],data1.loc[i,'Zturnvolume_ratio'],data1.loc[i,'Zvol_ratio']])
    #========自己设置结束============
    
    angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False)
    data = np.concatenate((data, [data[0]])) # 闭合
    angles = np.concatenate((angles, [angles[0]])) # 闭合
    
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)# polar参数！！
    
    if data1.loc[i,'Z_color'] == 0:
        ax.plot(angles, data, 'go-', linewidth=3)# 画线
        ax.fill(angles, data, facecolor='g', alpha=0.25)# 填充
    elif data1.loc[i,'Z_color'] == 1:
        ax.plot(angles, data, 'ro-', linewidth=3)# 画线
        ax.fill(angles, data, facecolor='r', alpha=0.25)# 填充
    else:
        pass
        
    ax.set_thetagrids(angles * 180/np.pi, labels, fontproperties="SimHei")
    ax.set_title(data1.loc[i,'code'], va='bottom', fontproperties="SimHei")
    ax.set_rlim(0,10)
    ax.grid(True,linewidth=2)
    #plt.show()
    plt.savefig('%d.jpg'%i,format='jpg',bbox_inches='tight',dpi=300)



n_bins = 10
x = np.random.randn(1000, 3)

fig, axes = plt.subplots(nrows=2, ncols=2)
ax0, ax1, ax2, ax3 = axes.flatten()

colors = ['red', 'tan', 'lime']
ax0.hist(x, n_bins, normed=1, histtype='bar', color=colors, label=colors)
ax0.legend(prop={'size': 10})
ax0.set_title('bars with legend')

ax1.hist(x, n_bins, normed=1, histtype='bar', stacked=True)
ax1.set_title('stacked bar')

ax2.hist(x, n_bins, histtype='step', stacked=True, fill=False)
ax2.set_title('stack step (unfilled)')

# Make a multiple-histogram of data-sets with different length.
x_multi = [np.random.randn(n) for n in [10000, 5000, 2000]]
ax3.hist(x_multi, n_bins, histtype='bar')
ax3.set_title('different sample sizes')

fig.tight_layout()
plt.show()



var = pd.DataFrame(np.array([[-0.5,-5,0.5,2],[-1,-3,1,4]]))#,columns=list('ab'))

var.plot(kind='bar', stacked=True,grid=True)

plt.show()