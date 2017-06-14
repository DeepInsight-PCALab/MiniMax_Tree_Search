#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function

# for grid value:
# 0 means nothing
# 1 means black
# 2 means white
# ###############
# A typical grids like:
# 0 1 0
# 0 2 0
# 1 0 2

# for state value:
# 0  means ties
# 1  means black wins
# -1 means black loses
# -2 means to be determined

def State_To_Vector(s):
    res = []
    for i in xrange(3 * 3):
        res.append(s % 3)
        s /= 3
    return res

def Vector_To_State(v):
    v = list(reversed(v))
    res = 0
    for x in v:
        res = res * 3 + x
    return res

def Check_Equal(v):
    assert(len(v) == 3)
    for i in range(1, len(v)):
        if v[0] != v[i]:
            return False
    return True

def Get_Score(who_win):
    if who_win == 1:
        return 1
    if who_win == 2:
        return -1
    return 0

def Judge_Terminal_State(s):
    v = State_To_Vector(s)
    # print('Judge_Terminal_State = ', v)
    # check v row by row
    for r in range(0, 9, 3):
        if Check_Equal(v[r: r + 3]) and v[r] != 0:
            return True, Get_Score(v[r])
    # check v column by column
    for c in range(0, 3):
        if Check_Equal(v[c: c + 9: 3]) and v[c] != 0:
            return True, Get_Score(v[c])
    # check v by diganol
    if Check_Equal([v[0], v[4], v[8]]) and v[4] != 0:
        return True, Get_Score(v[4])
    if Check_Equal([v[2], v[4], v[6]]) and v[4] != 0:
        return True, Get_Score(v[4])
    # ties game
    if 0 not in v:
        return True, 0
    return False, -1

def Judge_Who_To_Play(s):
    v = State_To_Vector(s)
    dt = {2: 0, 1: 0, 0: 0}
    for x in v:
        dt[x] += 1
    if dt[2] == dt[1]:
        return 1
    return 2

dp = {}
def Dfs(fa):
    if fa in dp:
        return dp[fa]
    is_terminal, score = Judge_Terminal_State(fa)
    #if is_terminal:
    #    print('is_terminal = ', State_To_Vector(fa), 'score = ', score)
    if is_terminal:
        dp[fa] = score
        return dp[fa]
    who_to_play  = Judge_Who_To_Play(fa) # 1 or 2
    vector       = State_To_Vector(fa)
    jinzhi       = 1
    value_vector = []
    for i, v in enumerate(vector):
        if v == 0:
            son = fa + jinzhi * who_to_play
            value_vector.append(Dfs(son))
        jinzhi *= 3

    assert(len(value_vector) > 0)
    if who_to_play == 1: # choose max
        dp[fa] = max(value_vector)

    if who_to_play == 2: # choose min
        dp[fa] = min(value_vector)

    return dp[fa]


for x in range(0, 10000):
    assert(x == Vector_To_State(State_To_Vector(x)))
value = Dfs(0)

def print_grid_value(g, v):
    t = 0
    for i in range(3):
        print('%3d %3d %3d' %(g[t], g[t + 1], g[t + 2]))
        t += 3
    print('value = %d'%v)
    print('---------------------')

def print_next(v):
    fa = Vector_To_State(v)
    who_to_play = Judge_Who_To_Play(fa)
    print(who_to_play)
    jinzhi       = 1
    for i, v in enumerate(v):
        if v == 0:
            son = fa + jinzhi * who_to_play
            tv  = State_To_Vector(son)
            #print('son = ', son, 'tv = ', tv)
            print_grid_value(tv, dp[son])
        jinzhi *= 3


print_next([0, 0, 0, 0, 0, 0, 0, 0, 0])            
# it is for the next states of 
# 0 0 0
# 0 0 0
# 0 0 0

#print_next([1, 2, 1, 0, 1, 0, 0, 2, 2])
#print_next([0, 0, 0, 0, 1, 0, 0, 0, 0])


