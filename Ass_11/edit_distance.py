from functools import lru_cache
import sys

solution = {}

@lru_cache(maxsize=2**10)
def edit_distance(string1, string2):
    
    if len(string1) == 0: return len(string2) #如果两个词中的一个为空，则编辑距离为另一个的长度
    if len(string2) == 0: return len(string1)
    
    tail_s1 = string1[-1] #s1的最后一位
    tail_s2 = string2[-1] #s2的最后一位
    
    candidates = [
        (edit_distance(string1[:-1], string2) + 1, 'DEL {}'.format(tail_s1)),  #D_del=D(s1去掉最后一位，s2)+1,指删除s1最后一位
        # string 1 delete tail
        (edit_distance(string1, string2[:-1]) + 1, 'ADD {}'.format(tail_s2)),  #D_add=D(s1, s2去掉最后一位)+1,指给s1增加s2的最后一位
        # string 1 add tail of string2
    ]
    
    if tail_s1 == tail_s2: #如果s1,s2最后一位相同D_sub=D(s1去掉最后一位,s2去掉最后一位)
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 0, '')
    else: #不相同的话D_sub=D(s1去掉最后一位,s2去掉最后一位)+1，s1的最后一位替换为s2的最后一位
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 1, 'SUB {} => {}'.format(tail_s1, tail_s2))

    candidates.append(both_forward)#candidate=[D_del,D_sub,D_add]
    
    min_distance, operation = min(candidates, key=lambda x: x[0]) #min_distance 为最小的edit_distance, operation 为Del，Sub，Add
    
    solution[(string1, string2)] = operation 
    
    return min_distance

def parse_edit(string1,string2):
    if len(string2) == 0:
        return ['DEL {}'.format(string1)]
    if len(string1) == 0:
        return ['ADD {}'.format(string2)]
    operation = solution[(string1,string2)]
    if len(string1) == 1 and len(string2) == 1:
        return [operation]
    ope = operation.split(" ")[0]
    if ope == 'ADD':
        return parse_edit(string1,string2[:-1])+[operation]
    elif ope == 'SUB' or ope == '':
        return parse_edit(string1[:-1],string2[:-1])+[operation]
    else:
        return parse_edit(string1[:-1],string2)+[operation]

if __name__ == "__main__":
    if len(sys.argv) is not 3:
        print("usage: edit_distance.py word1 word2")
        exit()
    string1 = sys.argv[1]
    string2 = sys.argv[2]
    solution = {}
    min_distance = edit_distance(string1,string2)
    path = parse_edit(string1,string2)
    print("the min distance is {}".format(min_distance))
    for steps in path:
        if len(steps) is not 0:
            print(steps)
    exit()
    
