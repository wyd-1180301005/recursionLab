import numpy as np
import math as ma
from scripts.naiveMedian import naiveMedianClass
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

# 输入一个数组,使用给定的pivot进行划分数组
# 重新排列数组,使得左侧小于等于pivot,右侧大于pivot
# 返回分界中点的位置
def myPartition(arr,st_in,ed_in,pivot):
    
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


class advancedMedianClass():
    cost=0

    # 使用递归的版本(容易理解调试,然而复杂度高)
    # 基于五数取中的第k顺序值计算算法
    # k在[0,len(arr))范围内
    def advancedMedian(self,arr,st,ed,k):


        if(ed-st<=75):
            self.cost+=selectSort(arr,st,ed)
            return arr[st+k]
        
        # 分成长度为5的小数组,num是分出来的小数组的个数
        # 如果最后一个小数组不够五个数,也算是一个小数组 
        # [0 1 2 3 4]  [5 6 7 8 9] [10 11 12]
        num=ma.ceil((ed-st)/5)
        # 将五个数排序,并将其中位数放到队首
        for i in range(0,num):
            st_five=st+i*5
            ed_five=min(st_five+5,ed)
            mid_five=int((st_five+ed_five-1)/2)
            self.cost+=selectSort(arr,st_five,ed_five)

            tmp=arr[st+i]
            arr[st+i]=arr[mid_five]
            arr[mid_five]=tmp
        
        # 找到中位数的中位数
        median=self.advancedMedian(arr,st,st+num,int(num/2))
        part=myPartition(arr,st,ed,median)
        self.cost+=ed-st # partition 过程的代价



        # 现在要判断第k大的元素会出现在哪一个部分内,从而缩减问题规模:
        sub_arr1_len=part-st

        # k在第二部分内:
        if(k >=sub_arr1_len):
            return self.advancedMedian(arr,part,ed,k-sub_arr1_len)
        else:
            return self.advancedMedian(arr,st,part,k)

    # 使用双端队列的版本(算法较为复杂不易理解,但是复杂度低,鲁棒性高)
    # 基于五数取中的第k顺序值计算算法
    # k在[0,len(arr))范围内
    def advancedMedian_QueueImpl(self,arr,st_in,ed_in,k_in):

        q1=deque()
        q2=deque()
        q3=deque()

        st=st_in
        ed=ed_in
        k=k_in

        # 用来记录还有多少个待解决的原始问题
        count_num=0

        theMedian=0
        trace_back=False
        while(True):

            
            # 如果当前问题是一个naive问题,则直接使用naive方法解决该问题
            # 并且递归调用开始出栈,使用theMedian去partition原始问题
            # 当栈中不存在任何原始问题时,即是算法将初始的问题简化为naive问题的时刻,直接返回theMedian就是初始问题的答案
            trace_back=False
            if(ed-st<=75):
                self.cost+=selectSort(arr,st,ed)
                trace_back=True
                theMedian=arr[st+k]
                if(count_num==0):
                    return theMedian
                st=q1.pop()
                ed=q2.pop()
                k=q3.pop()
                count_num-=1


            # 在递归的时候,将原始问题暂存
            if(trace_back==False):
                
                # 分成长度为5的小数组,num是分出来的小数组的个数
                # 如果最后一个小数组不够五个数,也算是一个小数组 
                # [0 1 2 3 4]  [5 6 7 8 9] [10 11 12]
                num=ma.ceil((ed-st)/5)
                # 将五个数排序,并将其中位数放到队首
                for i in range(0,num):
                    st_five=st+i*5
                    ed_five=min(st_five+5,ed)
                    mid_five=int((st_five+ed_five-1)/2)
                    self.cost+=selectSort(arr,st_five,ed_five)

                    tmp=arr[st+i]
                    arr[st+i]=arr[mid_five]
                    arr[mid_five]=tmp


                q1.append(st)
                q2.append(ed)
                q3.append(k)
                count_num+=1

                # 将当前要解决的问题设定为"求解pivot"的子问题
                ed=st+num
                k=int(num/2)
            # pivot求出来了,可以进行partition了
            else:
                part=myPartition(arr,st,ed,theMedian)
                self.cost+=ed-st # partition 过程的代价

                # 现在要判断第k大的元素会出现在哪一个部分内,从而缩减问题规模:
                sub_arr1_len=part-st

                # k在第二部分内:
                if(k >=sub_arr1_len):
                    st=part
                    k=k-sub_arr1_len
                else:
                    ed=part


# 测试median的方法
for i in range(0,100):
    arr=np.random.randint(0,100000,10000)
    arr1=arr.copy()

    m1=advancedMedianClass()
    mid1=m1.advancedMedian_QueueImpl(arr,0,len(arr),int(len(arr)/2))

    m2=naiveMedianClass()
    mid2=m2.naiveMedian(arr1)


    if(mid1!=mid2):
        print("error")