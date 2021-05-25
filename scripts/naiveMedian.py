import numpy as np
import math as ma
from collections import deque

# 简单的选择排序算法
def selectSort(arr,st_in,ed_in):
    for i in range(st_in,ed_in):
        min=i
        for j in range(i+1,ed_in):
            if(arr[j]<arr[min]):
                min=j
        tmp=arr[min]
        arr[min]=arr[i]
        arr[i]=tmp
    return int((ma.pow(ed_in-st_in,2)-(ed_in-st_in))/2)

# 输入一个数组,随机选取其中一个pivot
# 重新排列数组,使得左侧小于等于pivot,右侧大于pivot
# 返回分界中点
def myPartition(arr,st_in,ed_in):
    pivot=arr[np.random.randint(st_in,ed_in)]
    
    st=st_in
    ed=ed_in-1

    while(True):
        while(st<ed_in and arr[st]<=pivot):
            st+=1
        while(ed>=0 and arr[ed]>pivot):
            ed-=1

        if(st>ed):
            break

        tmp=arr[st]
        arr[st]=arr[ed]
        arr[ed]=tmp

        st+=1
        ed-=1

    return st

# quickSort方法,使用partition进行数组分割
# 因为python的递归次数限制,将递归转化为迭代求解,使用双端队列暂存partition信息
# 返回qsort的算法代价----算法执行的比较次数,也就是每次执行partition的数组的长度
def myQsort(arr):

    st=0
    ed=len(arr)

    q1=deque()
    q2=deque()

    q1.append(st)
    q2.append(ed)

    cost_count=0
    num_count=1
    while(num_count>0):
        st=q1.popleft()
        ed=q2.popleft()
        num_count-=1
        
        if(ed-st<2):
            continue
        elif(ed-st<=10):
            cost_count+=selectSort(arr,st,ed)
        else:
            mid=myPartition(arr,st,ed)
            cost_count+=(ed-st)
            q1.append(st)
            q2.append(mid)
            q1.append(mid)
            q2.append(ed)
            num_count+=2
    
    return cost_count

class naiveMedianClass():

    cost=0
    # 排序后,选取中位数的简单算法
    def naiveMedian(self,arr):

        self.cost=myQsort(arr)
        len_arr=len(arr)
        return arr[int(len_arr/2)]

# # test partition
# for i in range(0,100):
#     arr0=np.random.randint(0,1000,30000)
#     mid=myPartition(arr0,0,len(arr0))
#     if(mid==0 or mid>=len(arr0)):
#         continue
#     x=max(arr0[0:mid])
#     y=min(arr0[mid:])
#     if(x>=y):
#         print("error")


# # test qsort correctness
# for i in range(0,100):
#     arr0=np.random.randint(0,100000,3000)
#     n=myQsort(arr0)

#     last=arr0[0]
#     for j in range(1,len(arr0)):
#         if(arr0[j]<last):
#             print("error")
#             break
#         last=arr0[j]

# # test qsort speed
# arr=np.random.randint(0,100000,30000)
# arr1=arr.copy()

# a=selectSort(arr,0,len(arr))
# print(a)
# b=myQsort(arr1)
# print(b)
# print(a/b)