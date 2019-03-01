def merge_sort(li):
    n=len(li)
    mid=n//2
    if  n==1:
        return li
    #拆分列表
    left_list=li[:mid]
    right_list=li[mid:]

    #排序
    left_sort=merge_sort(left_list)
    right_sort=merge_sort(right_list)

    #合并序列
    left_index=0
    right_index=0
    merge_list=[]

    while left_index<len(left_sort) and right_index<len(right_sort):
        if left_sort[left_index]<=right_sort[right_index]:
            merge_list.append(left_sort[left_index])
            left_index+=1
        else:
            merge_list.append(right_sort[right_index])
            right_index+=1

    merge_list.extend(left_sort[left_index:])
    merge_list.extend(right_sort[right_index:])
    return merge_list

a=[22,53,12,64,75,21,77,11,32]
n=len(a)
sorted_list=merge_sort(a)
print(sorted_list)