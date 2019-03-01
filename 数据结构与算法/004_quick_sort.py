
#快速排序法
def quick_sort(li,start,end):
    mid=li[start]
    left=start
    right=end
    if start>=end:
        return
    while left< right:
        while left<right and li[right]>=mid:
            right-=1
        li[left]=li[right]
        while left<right and li[right]<mid:
            left+=1
            li[right]=li[left]
    li[left]=mid
    quick_sort(li,start,left-1)
    quick_sort(li,left+1,end)

a=[22,53,12,64,75,21,77,11,32]
n=len(a)
quick_sort(a,0,n-1)
print(a)