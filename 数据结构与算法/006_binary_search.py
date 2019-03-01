# def binary_search(li,data):
#     n=len(li)
#     mid=n//2
#     if n<=0:
#         return False
#     # else:
#     #     return True
#     if li[mid]==data:
#         return True
#     elif li[mid]>data:
#         return binary_search(li[:mid],data)
#     else:
#         return binary_search(li[mid+1:],data)
#
# a=[1,2,3,4,5,6,7,8,9]
# result=binary_search(a,8)
# print(result)

def binary_search(li,data):
    start=0
    end=len(li)+1

    while start<=end:
        mid = (start + end) // 2
        if li[mid]==data:
            return True
        elif li[mid]>data:
            end=mid-1
        else:
            start=mid+1
    return False


a=[1,2,3,4,5,6,7,8,9]
result=binary_search(a,8)
print(result)

