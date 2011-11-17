import random
import copy
import math

def int2baseTwo(x):
    '''convert a integer into a binary list in reverse order'''
    binList = []
    while x != 0:
        binList.append(x % 2)
        x = x // 2          #each iteration divided by 2 and keep the remainder
    return binList

def randLocationR(n):
    '''return a random location hanoi puzzle.'''
    retList = []
    for i in range(n):
        retList.append(random.randint(0, 2))
    return retList

def rollcall2List(R):
    '''return a hanoi puzzle in list of list format.'''
    maxNum = len(R)
    L = [[], [], []]
    for loc in R:
        L[loc].insert(0, maxNum)
        maxNum -= 1
    return L
    
def isLegalMove(L, a, b):
    '''determine if a move from post a to b is legal.'''
    if L[a] == []:
        return False
    elif L[b] == []:
        return True
    else:
        return (L[a][0] < L[b][0])

def makeMove(L, a, b):
    '''move the top disc from post a to post b if this move is legal.'''
    if isLegalMove(L, a, b):
        L[b].insert(0, L[a].pop(0))

def printList(L):
    '''print the hanoi list.'''
    printL = copy.deepcopy(L)
    maxIndex = max(len(L[0]),len(L[1]),len(L[2]))
    minIndex = min(len(L[0]),len(L[1]),len(L[2]))
    medIndex = len(L[0]) + len(L[1]) + len(L[2]) - maxIndex - minIndex
    print('     [Post 1] [Post 2] [Post 3]')
    for i in range(maxIndex - medIndex):
        for j in range(3):
            if len(L[j]) >= maxIndex:
                print(str(printL[j].pop(0)).rjust(9), end = '')
            else:
                print(' ' * 9, end = '')
        print()
    for i in range(maxIndex - medIndex, maxIndex - minIndex):
        for j in range(3):
            if len(L[j]) >= medIndex:
                print(str(printL[j].pop(0)).rjust(9), end = '')
            else:
                print(' ' * 9, end = '')
        print()
    for i in range(maxIndex - minIndex, maxIndex):
        for j in range(3):
            if len(L[j]) >= minIndex:
                print(str(printL[j].pop(0)).rjust(9), end = '')
            else:
                print(' ' * 9, end = '')
        print()

def list2Rollcall(L):
    '''return a rollcall of hanoi from the list representation.'''
    maxNum = 0
    retList = []
    for post in L:
        maxNum += len(post)
    LCopy = copy.deepcopy(L)
    for i in range(maxNum):
        for index in range(len(L)):
            post = LCopy[index]
            if post != [] and post[0] == i + 1:
               post.pop(0)
               retList.insert(0, index)
               continue
    return retList

def rollcall2SA(R):
    '''convert hanoi puzzle rollcall format to Sierpinski Address format.'''
    length = len(R)
    s = []
    if length % 2 != 0:     #n is odd
        p = [0, 1, 2]
    else:
        p = [2, 1, 0]
    for i in range(length):
        for j in range(3):
            if p[j] == R[i]:        #find the location of R[i] in p
                s.append(j)
        k = s[i]
        swap1 = (k + 1) % 3
        swap2 = (k + 2) % 3     #swap the rest values except k
        temp = p[swap1]
        p[swap1] = p[swap2]
        p[swap2] = temp
    return s

def SA2rollcall(SA):
    '''convert hanoi puzzle SA format to rollcall format.'''
    return rollcall2SA(SA)

def SA2TA(SA):
    '''convert hanoi puzzle SA format to Tenary Address format.'''
    if SA == []:
        return []
    TA = [0] * 3
    length = len(SA)
    for i in range(length):
        for j in range(3):
            TA[j] += pow(2, length - i - 1) 
        TA[SA[i]] -= pow(2, length - i - 1)
    return TA
        
def TA2SA(TA):
    '''convert hanoi puzzle TA format to SA format.'''
    if TA == []:
        return []
    maxLen = 0
    TABaseTwo = []
    testList = []
    SA = []
    temp = 0
    for num in TA:
        temp = int2baseTwo(num)
        TABaseTwo.append(temp)
        if len(temp) > maxLen:
            maxLen = len(temp)
    for i in range(3):              #insert 0 in short lists
        for j in range(maxLen - len(TABaseTwo[i])):
            TABaseTwo[i].append(0)
    for j in range(maxLen):         #translate bitwisely
        if (TABaseTwo[0][j] == 0 and TABaseTwo[1][j] == 1 
                and TABaseTwo[2][j] == 1):
            SA.insert(0, 0)
        elif (TABaseTwo[0][j] == 1 and TABaseTwo[1][j] == 0 
                and TABaseTwo[2][j] == 1):
            SA.insert(0, 1)
        elif (TABaseTwo[0][j] == 1 and TABaseTwo[1][j] == 1 
                and TABaseTwo[2][j] == 0):
            SA.insert(0, 2)
        else:
            print("Illegal Tenary address!")
            return None
    return SA

def reduceTA(A, B):
    '''remove the largest disc in common to simply the puzzle.'''
    if A == B:
        for i in range(3):
            A.pop()
            B.pop()
        return None
    SA_A = TA2SA(A)
    SA_B = TA2SA(B)
    while SA_A[0] == SA_B[0]:       #remove the first indices in common
        SA_A.pop(0)
        SA_B.pop(0)
    TA_A_New = SA2TA(SA_A)
    TA_B_New = SA2TA(SA_B)
    for i in range(3):
        A[i] = TA_A_New[i]
        B[i] = TA_B_New[i]
    return None

def distTA(A_in, B_in):
    '''calculate the TA distance between A and B.'''
    if A_in == B_in:
        return 0
    A_copy = copy.deepcopy(A_in)
    B_copy = copy.deepcopy(B_in)
    reduceTA(A_copy, B_copy)      #simplify puzzle
    SA_A = TA2SA(A_copy)
    SA_B = TA2SA(B_copy)

    base = pow(2, int(math.log(A_copy[SA_B[0]], 2)))
    #calculate the distance towards each other's corner
    dist1 = A_copy[SA_B[0]] + B_copy[SA_A[0]]- 2 * base + 1 
    #calculate the distance passing the left corner
    dist2 = A_copy[3 - SA_A[0]- SA_B[0]] + \
            B_copy[3 - SA_A[0]- SA_B[0]] - base + 1
    return min(dist1, dist2)


def main():
    '''The hanoi game puzzle!'''
    n = input("Please select the size of the Hanoi puzzle: ")
    rollcall = randLocationR(eval(n))
    printList(rollcall2List(rollcall))
    exp = int(math.pow(2, eval(n)))
    targetRollcall = [2] * eval(n)
    distance = distTA(SA2TA(rollcall2SA(rollcall)),
                      SA2TA(rollcall2SA(targetRollcall)))
    print("The TA distance is ", distance)
    if distance == 0:
        print("You are so lucky! It is solved already!")
    resp = ""
    L = rollcall2List(rollcall)
    while distance != 0:
        resp = input("Which disc do you want to move: ")
        if resp == "quit":
            print("Bye!")
            return None
        resp2 = input("Which post do you want to move to: ")
        if resp2 == "quit":
            print("Bye!")
            return None
        if not isLegalMove(L, eval(resp) - 1, eval(resp2) - 1):
            print("Illegal move!")
            continue
        makeMove(L, eval(resp) - 1, eval(resp2) - 1)
        printList(L)
        distance = distTA(SA2TA(rollcall2SA(list2Rollcall(L))),
                          SA2TA(rollcall2SA(targetRollcall)))
        print("The TA distance is ", distance)
    print("Congratulations!")
    return None
