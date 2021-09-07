# -*- coding: UTF-8 -*-
import csv
import numpy as np
from scipy import interpolate
import pylab as pl

## 文件目录
refFile = 'testdata/Radixact_WTGold_J7mm_Transverse_June2017.csv'
measuredFile = 'testdata/Tran_J07_20210818_Pro.csv'

# 计算金标的对称性函数
def calculate_Ref_profile_symmetry(refData):
    reversedRefData=refData[::-1]  #得到其逆序的列表，方便对比提高效率
    dataInfo = []
    value = []
    deltaSym = []

    # 先计算金标函数如何归一的，是100最大值归一还是1的最大值归一
    for refRow in refData:
        value.append(float(refRow[4]))

    valueMax=max(value)

    for refRow in refData:
        if(float(refRow[2]) == 0): #只需要找一半
            break
        if(float(refRow[4]) < (valueMax*0.2)): #只找20%以上的
            continue
        for reversedRow in reversedRefData:
            if(refRow[2][1:] == reversedRow[2]):
                # -x的坐标和value,x的坐标和value,以及差值,调试用
                dataInfo.append([refRow[2],float(refRow[4]),reversedRow[2],float(reversedRow[4]),float(refRow[4]) - float(reversedRow[4])])
                # 差值的list
                indexData = float(refRow[4])/float(reversedRow[4])
                if indexData<1:
                    indexData = 1/indexData
                deltaSym.append(indexData)
                break
  
    symmetryIndex = max(deltaSym)    

    # 每个点的对称性值
    symmetryData = np.array(deltaSym)

    return symmetryIndex, symmetryData

# 计算测量数据的对称性函数
def calculate_Measured_profile_symmetry(measuredData):
    x_index = []
    value_index = []
    # 得到横纵坐标，然后进行插值
    for row in measuredData:
        x_index.append(row[0])
        value_index.append(row[1])  

    # 字符串转换位float
    x_np = np.array(x_index)
    value_np = np.array(value_index)
    x_np = x_np.astype(float)
    value_np = value_np.astype(float)

    # 插值 三次样条插值，更平滑
    interpolateF=interpolate.interp1d(x_np,value_np,kind='cubic')

    # 插值得到和金标数据一样的数据点 -250到250,步长为1
    x_inter_index=np.arange(-250,251,1)
    value_inter_index = interpolateF(x_inter_index)

    # 按坐标对比插值,[-250,250]对应value的下标是[0,500]
    symmetricIndexData = []
    for xx_interp in x_inter_index:
        if(value_inter_index[xx_interp+250] < (max(value_inter_index)*0.2)): #只找20%以上的
            continue
        if xx_interp == 0:
            break
        indexData = value_inter_index[xx_interp+250]/value_inter_index[250-xx_interp]
        if indexData<1:
            indexData = 1/indexData
        symmetricIndexData.append(indexData)
    
    symmetricIndex = max(symmetricIndexData)

    return  symmetricIndex, symmetricIndexData

# python入口
def main():

    with open(refFile, 'r') as f:
        reader = csv.reader(f)
        
        referenceData=[]
        for row in reader:
            lenRow = len(row)
            
            if(lenRow > 5):
                if(row[3][0:2] == '15' and float(row[3]) == 15):     # 只需要水下15的数据
                    referenceData.append(row)

    symmetryGSIndex, symmetryGSData = calculate_Ref_profile_symmetry(referenceData)

    with open(measuredFile, 'r') as f:
        reader = csv.reader(f)
        
        measuredData=[]
        rowNum = 0
        for row in reader:
            rowNum += 1
            if(rowNum > 7):              
                measuredData.append(row)
                   
    symmetryMeaIndex, symmetryMeaData = calculate_Measured_profile_symmetry(measuredData)

    print (refFile,'金标的对称性参数==',symmetryGSIndex)
    print (measuredFile,'测量数据对称性参数==',symmetryMeaIndex)

    # 计算时候是从边缘到0点，绘图时候要取反
    symmetryGSData = symmetryGSData[::-1]
    GS_index = np.arange(0,len(symmetryGSData),1)

    symmetryMeaData = symmetryMeaData[::-1]
    Mea_index = np.arange(0,len(symmetryMeaData),1)

    pl.plot(GS_index,symmetryGSData,label='GS')
    pl.plot(Mea_index,symmetryMeaData,label='Measured')  
    pl.legend(loc="lower right")  
    pl.show()

if __name__ == "__main__":
    main()