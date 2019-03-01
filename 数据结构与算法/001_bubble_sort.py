#冒泡排序
def bubble_sort(li):
    n=len(li)
    for j in range(n-1):
        for i in range(n-1-j):
            #if li[i]<li[i+1]: 降序
            if li[i]>li[i+1]:
                li[i],li[i+1]=li[i+1],li[i]

a=[22,53,12,64,75,21,77,11,32]

bubble_sort(a)
print(a)