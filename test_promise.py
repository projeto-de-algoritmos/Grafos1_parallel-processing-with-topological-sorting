import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from top_processing import Evaluate, lazy, count_graph, relational_graph

@lazy
def mergesort(values, l, r):

    if(l<r):
        mid = (l+r)//2

        mergesort(values, l, mid)
        mergesort(values, mid+1, r)
        merge(values, l, mid, r)

    return values

@lazy
def merge(arr: list, l: int, mid: int, r: int):

    n1: int = mid - l + 1
    n2: int = r - mid

    L = arr[l:mid+1]
    R = arr[mid+1:r+1]

    l1: int = 0
    l2: int = 0
    p: int = l

    while l1 < n1 and l2 < n2:

        if L[l1] < R[l2]:
            arr[p] = L[l1]
            l1+=1
        else:
            arr[p] = R[l2]
            l2+=1

        p+=1

    while(l1 < n1):
        arr[p] = L[l1]
        l1+=1
        p+=1

    while(l2 < n2):
        arr[p] = R[l2]
        l2+=1
        p+=1

@lazy
def add(value1, value2):
    return value1 + value2

@lazy
def mult(value1, value2):
    return value1 * value2

if __name__ == '__main__':

    print(add(add(5, 4), mult(10, 4))())

