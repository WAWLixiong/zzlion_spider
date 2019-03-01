def shell_sort(li):
    n=len(li)
    gap=n//2
    while gap>0:
        for j in range(gap,n):
            for i in range(j , 0, -gap):
                if li[i] < li[i - gap]:
                    li[i], li[i - gap] = li[i - gap], li[i]
                else:
                    break
        gap=gap//2

a=[22,53,12,64,75,21,77,11,32]
shell_sort(a)
print(a)