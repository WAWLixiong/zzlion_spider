#插入排序

# #思想
# if li[0]>li[1]:
#     li[0],li[1]=li[1],li[0]
#
# if li[1]>li[2]:
#     li[1],li[2]=li[2],li[1]
#         if li[0]>li[2]:
#             li[0],li[2]=li[2],li[0]

def insert_sort(li):
    n=len(li)
    for j in range(n-1):
        for i in range(j+1,0,-1):
            if li[i]<li[i-1]:
                li[i],li[i-1]=li[i-1],li[i]
            else:
                break


a=[22,53,12,64,75,21,77,11,32]
insert_sort(a)
print(a)