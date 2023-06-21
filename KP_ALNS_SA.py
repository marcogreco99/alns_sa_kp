import random
from random import randint, shuffle
import math


def getWeightKnapsack(X):
    w = 0
    for t in X:
        w += t[0]
    return w

def getValueKnapsack(X):
    v = 0
    for t in X:
        v += t[1]
    return v

def checkAvailable(w,c):
    global treasures
    for t in treasures:
        if t[0]+w<=c:
            return True
    return False

def getTreasureOk(w,c):
    global treasures
    for t in treasures:
        if t[0]+w<=c:
            return t
    return



def destroy(op_destr):
    global Xcurrent, treasures
    l = Xcurrent.copy()
    match op_destr:
        case 0: # peso max
            if(len(Xcurrent)==0): return l
            max = l[0]
            for t in l:
                if t[0] > max[0]:
                    max = t
                elif t[0] == max[0]:
                    if t[1] < max[1]:
                        max = t

            l.remove(max)
            treasures.append(max)
            return l

        case 1: # valore minimo
            if(len(Xcurrent)==0): return l
            min = l[0]
            for t in l:
                if t[1] < min[1]:
                    min = t
                elif t[1] == min[1]:
                    if t[0] > min[0]:
                        min = t

            l.remove(min)
            treasures.append(min)
            return l

        case 2:
            if(len(Xcurrent)==0): return l
            max = l[0]
            for t in l:
                if t[0]/t[1] > max[0]/max[1]:
                    max = t
                elif t[0]/t[1] == max[0]/max[1]:
                    if t[0] > max[0]:
                        max = t

            l.remove(max)
            treasures.append(max)
            return l

        case 3:
            if (len(Xcurrent)==0): return l
            if len(l)-1 >= 2: n = randint(2, len(l)-1)
            else: n = 1
            todelete=random.sample(range(0,len(l)),n)
            for i in sorted(todelete, reverse = True):
                treasures.append(l[i])
            for fd in sorted(todelete, reverse = True):
                del l[fd]
            return l


        case _:
            return l

def repair(op_rep, X):
    global treasures, c
    l = X.copy()
    match op_rep:
        case 0: # peso min
            if len(treasures)==0 or checkAvailable(getWeightKnapsack(l),c) == False: return l
            min = getTreasureOk(getWeightKnapsack(l),c)
            for t in treasures:
                if t[0] < min[0] and getWeightKnapsack(l)+t[0] <= c :
                    min = t
                elif t[0] == min[0] and getWeightKnapsack(l)+t[0] <= c :
                    if t[1] > min[1]:
                        min = t

            l.append(min)
            treasures.remove(min)
            return l

        case 1: # valore max

            if len(treasures)==0 or checkAvailable(getWeightKnapsack(l),c) == False: return l
            max = getTreasureOk(getWeightKnapsack(l),c)
            for t in treasures:
                if t[1] > max[1] and getWeightKnapsack(l)+t[0] <= c :
                    max = t
                elif t[1]==max[1] and getWeightKnapsack(l)+t[0] <= c :
                    if t[0] < max[0]:
                        max = t

            l.append(max)
            treasures.remove(max)
            return l

        case 2:

            if len(treasures)==0 or checkAvailable(getWeightKnapsack(l),c) == False: return l
            min = getTreasureOk(getWeightKnapsack(l),c)
            for t in treasures:
                if t[0]/t[1] < min[0]/min[1] and getWeightKnapsack(l)+t[0] <= c:
                    min = t
                elif t[0]/t[1] == min[0]/min[1] and getWeightKnapsack(l)+t[0] <= c:
                    if t[0] < min[0]:
                        min = t

            l.append(min)
            treasures.remove(min)
            return l

        case 3:

            if len(treasures)==0 or checkAvailable(getWeightKnapsack(l),c) == False: return l
            if len(treasures)-1 >= 2: n = randint(2, len(treasures)-1)
            else: n = 1
            for i in range(n):
                if(checkAvailable(getWeightKnapsack(l),c) == False):
                    return l
                else:

                    shuffle(treasures)
                    t = getTreasureOk(getWeightKnapsack(l),c)
                    l.append(t)
                    treasures.remove(t)
            return l

        case _:
            return l


def initial_solution():
    global treasures, c
    knapsack = []
    check = [0, 0, 0, 0]
    while(getWeightKnapsack(knapsack) != c and sum(check)!=len(treasures)):
        value = randint(0, len(treasures)-1)
        if check[value]!=1 and treasures[value][0]+getWeightKnapsack(knapsack) <= c:
            knapsack.insert(0,treasures[value])
        check[value]=1
    for t in (knapsack): treasures.remove(t)
    return knapsack

#INIZIALIZZAZIONE
allTreasures = [[1,20], [4, 100], [3, 30], [7, 500]]
treasures = [[1,20], [4, 100], [3, 30], [7, 500]]
P_d = [0.25,0.25,0.25,0.25] #probabilità per ogni operatore di distruzione
P_i = [0.25,0.25,0.25,0.25] #probabilità per ogni operatore di riparazione
T = 100 #temperatura
h = 0.05 #cooling rate
c = 8 #capacità dello zaino
inc = 0.05
flag = True
D = [0, 1, 2, 3]
I = [0, 1, 2, 3]
Xinit = []
Xcurrent = []
Xbest = []

Xinit = initial_solution()
print('Xinit:'+str(Xinit))
Xbest = Xinit.copy()
Xcurrent = Xbest.copy()

while(True):
    #Seleziono un operatore d in D con probabilità P_d[i]
    d = random.choices(
             D,
             P_d,
             k=1
    )[0]

    Xnew = destroy(d)

    #Seleziono un operatore i in I con probabilità P_i[k]
    i = random.choices(
        I,
        P_i,
        k=1
    )[0]

    Xnew2 = repair(i,Xnew)

    if (getValueKnapsack(Xnew2) > getValueKnapsack(Xcurrent)):
        Xcurrent = Xnew2.copy()

        for pd in range(len(P_d)):
            if pd != d and P_d[pd]-inc < 0 or P_d[d]+inc > 1 :
                flag = False

        for pi in range(len(P_i)):
            if pi != i and P_i[pi]-inc < 0 or P_i[i]+inc > 1:
                flag = False

        #if flag == False: inc = 0.01

        if flag:
            P_d[d]+=inc
            P_d[d] = round(P_d[d],1)
            for pd in range(len(P_d)):
                if pd != d:
                    P_d[pd]-=inc
                    P_d[pd]=round(P_d[pd],1)

            P_i[i]+=inc
            P_i[i] = round(P_i[i],1)
            for pi in range(len(P_i)):
                if pi != i:
                    P_i[pi]-=inc
                    P_i[pi]=round(P_i[pi],1)
    else:
        n = pow(math.e, -(getValueKnapsack(Xcurrent) - getValueKnapsack(Xnew2))  / T)
        e = random.random()
        if e < n:
            Xcurrent=Xnew2.copy()

            for pd in range(len(P_d)):
                if pd != d and P_d[pd]-inc < 0 or P_d[d]+inc > 1:
                    flag = False

            for pi in range(len(P_i)):
                if pi != i and P_i[pi]-inc < 0 or P_i[i]+inc > 1:
                    flag = False

            if flag:
                P_d[d]+=inc
                P_d[d] = round(P_d[d],1)
                for pd in range(len(P_d)):
                    if pd != d:
                        P_d[pd]-=inc
                        P_d[pd] = round(P_d[pd],1)

                P_i[i]+=inc
                P_i[i] = round(P_i[i],1)
                for pi in range(len(P_i)):
                    if pi != i:
                        P_i[pi]-=inc
                        P_i[pi] = round(P_i[pi],1)
        else:
            treasures = allTreasures.copy()
            for t in Xcurrent: treasures.remove(t)
    if (getValueKnapsack(Xcurrent) > getValueKnapsack(Xbest)):
        Xbest=Xcurrent.copy()

    T = h * T

    print('Xbest:'+str(Xbest))






Risultati del modello (tren/test):
Perdita: -1,83 / -1,75
Precisione binaria: 0,89 / 0,89
Violazione dello spazio: 0,05 / 0,06
Sovraprezzo: 0,12 / 0,14