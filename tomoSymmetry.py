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
    for refRow in refData:
        if(refRow[2] == '0.000000'): #只需要找一半
            break
        for reversedRow in reversedRefData:
            if(refRow[2][1:] == reversedRow[2]):
                # -x的坐标和value,x的坐标和value,以及差值,调试用
                dataInfo.append([refRow[2],float(refRow[4]),reversedRow[2],float(reversedRow[4]),float(refRow[4]) - float(reversedRow[4])])
                # value用来求最大值
                value.append(float(refRow[4]))
                value.append(float(reversedRow[4]))
                # 差值的list
                deltaSym.append(float(refRow[4]) - float(reversedRow[4]))
                break
  
    valueMax = max(value)       
    deltaSymMax = max(deltaSym)    

    # 对称性值（即差值最大值，然后归一化）
    symmetryIndex = deltaSymMax/valueMax
    # 每个点的对称性值
    symmetryData = np.array(deltaSym)
    symmetryData = np.divide(symmetryData,valueMax)
 

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


    print(x_inter_index,value_inter_index,len(value_inter_index))

    return 

# python入口
def main():

    with open(refFile, 'r') as f:
        reader = csv.reader(f)
        
        referenceData=[]
        for row in reader:
            lenRow = len(row)
            
            if(lenRow > 5):
                if(row[3] == '15.000000'):     # 只需要水下15的数据
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
                   
    symmetryMeaData = calculate_Measured_profile_symmetry(measuredData)
      


if __name__ == "__main__":
    main()