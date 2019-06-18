import argparse
from collections import defaultdict

def parse(rule):
    rule = rule.strip('\n')
    temp = rule.split(':')
    key = temp[0].strip(' ')
    t = temp[1].split('|')
    grammar = [r.strip(' ').split(' ') for r in t]
    return key, grammar

def parseRule(rule):
    rule = rule.strip('\n').split(':')

    key = rule[0].strip()
    temp = [l.replace(' ', '') for l in rule[1].split('|')]
    value = []
    for t in temp:
        v = []
        if t == 'epsilon':
            v.append('epsilon')
        else:
            for i in range(len(t)):
                k = t[i]
                if k!="'":
                    for j in range(i+1, len(t)):
                        if t[j]=="'":
                            k+="'"
                        else:
                            break
                    v.append(k)
            
        value.append(v)

    # print(key, '->', value)
    return key, value


def first(grammar):
    first_dict = defaultdict(set)

    updated = True
    while updated:
        updated = False
        for key, value in grammar.items():
            for v in value:
                k=v[0]
                temp = set()
                if v == 'epsilon':
                    temp.add(v)
                elif k not in grammar.keys(): # terminal
                    temp.add(v[0])
                else:
                    for i in range(len(v)):
                        k = v[i]
                        temp = temp | first_dict[k]

                        # terminal 
                        if k not in grammar.keys():
                            temp.add(k)
                            temp.discard('epsilon')
                            break

                        if 'epsilon' not in first_dict[k]:
                            temp.discard('epsilon')
                            break

                
                if (first_dict[key] | temp) != first_dict[key]:
                    updated = True
                    first_dict[key] = first_dict[key] | temp

    # to remove empty sets
    first_dict = {k: v for k, v in first_dict.items() if len(v) > 0}
    return first_dict


def follow(grammar, first_dict, first_key):
    follow_dict = defaultdict(set)
    follow_dict[first_key].add('$')

    updated = True
    while updated:
        updated = False
        for key, value in grammar.items():
            for v in value:
                if v != 'epsilon':
                    for i in range(len(v)):
                        temp = set()
                        k = v[i]
                        if k in grammar.keys() and i == len(v)-1:
                            temp = follow_dict[key]
                        elif k in grammar.keys() and v[i+1] not in grammar.keys():
                            temp.add(v[i+1])
                        elif k in grammar.keys() and v[i+1] in grammar.keys() and 'epsilon' not in first_dict[v[i+1]]:
                            temp = first_dict[v[i+1]]
                        elif k in grammar.keys() and v[i+1] in grammar.keys() and 'epsilon' in first_dict[v[i+1]]:
                            for z in range(i+1, len(v)):
                                kk = v[z]

                                if z == len(v)-1 and kk not in grammar.keys():
                                    temp.add(kk)
                                    break
                                else:
                                    temp = temp | first_dict[kk]
                                if z == len(v)-1 and kk in grammar.keys() and 'epsilon' in first_dict[v[z]]:
                                    temp = temp | follow_dict[key]

                                if 'epsilon' not in first_dict[kk]:
                                    break
                                
                            temp.discard('epsilon')
                        if k in grammar.keys() and  (follow_dict[k]|temp) != follow_dict[k]:
                            updated = True
                            follow_dict[k] = follow_dict[k]|temp

    follow_dict = {k: v for k, v in follow_dict.items() if len(v) > 0}
    return follow_dict


def output(keys, first_dict, follow_dict):
    out = ''
    for key in keys:
        out+=key+' :'
        for v in first_dict[key]:
            out+=' '+v
        out+=' :'
        if key not in follow_dict:
            out+=' '
        else:
            for v in follow_dict[key]:
                out+=' '+v
        out+='\n'
    
    return out


if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input to test strings in on DFA", nargs="?", metavar="input_file")
    
    args = parser.parse_args()

    print(args.file)

    # get the file object
    output_file = open("task_5_1_result.txt", "w+")


    with open(args.file, "r") as file:
        rules = file.readlines()
        
        grammar = {}
        first_key = ''
        for rule in rules:
            key, value = parse(rule)
            if first_key == '':
                first_key = key
            grammar[key] = value
        
        first_dict = first(grammar)
        follow_dict = follow(grammar, first_dict, first_key)

        output_file.write(output(grammar.keys(), first_dict, follow_dict))



