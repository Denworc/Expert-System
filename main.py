import os
import sys


class Colors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    GREEN = '\033[1;32;40m'
    Yellow = '\033[1;33;40m'
    END = '\033[0m'


def get_rules(goal, rules_buff):
    res = []
    for rule in rules_buff:
        buff = rule.split('=>', 1)[1]
        if goal in buff:
            res.append(rule)
    return res


def get_facts(rule):
    res = []
    for fact in rule.split('=>', 1)[0].split():
        if fact in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            res.append(fact)
    return res


def solve_rule(param, solve_buff):
    for key, val in solve_buff.items():
        param = param.replace(key, str(val))
    param = param.replace("+", "and")
    param = param.replace("|", "or")
    try:
        return eval(param)
    except:
        print("Oops, there seems to be a problem with your input file, try to fix it.")
        sys.exit()


def solve_fact(stack, context, fact_buff, rules_buff, solve_buff):
    if not stack:
        return True
    goal = stack.pop(0)
    if goal in fact_buff:
        return solve_fact(stack, context, fact_buff, rules_buff, solve_buff)
    context.insert(0, goal)
    rules = get_rules(goal, rules_buff)
    for rule in rules:
        facts = get_facts(rule)
        for fact in facts:
            if fact not in context:
                stack.insert(0, fact)
                res = solve_fact(stack, context, fact_buff, rules_buff, solve_buff)
                solve_buff[fact] = res
        res = solve_rule(rule.split('=>', 1)[0], solve_buff)
        if res:
            print(Colors.Yellow + rule.split('=>', 1)[0] + "from rule", rule, "is True, so", goal,
                  "is True" + Colors.END)
            return True
        else:
            print(Colors.Yellow + rule.split('=>', 1)[0] + "from rule", rule, "is False, so", goal,
                  "is False" + Colors.END)
    return False


def get_res(fact, fact_buff, rules_buff):
    stack = []
    stack.append(fact)
    context = []
    solve_buff = {}
    res = solve_fact(stack, context, fact_buff, rules_buff, solve_buff)
    if res:
        print(Colors.GREEN + fact, ":", str(res) + Colors.END)
    else:
        print(Colors.RED + fact, ":", str(res) + Colors.END)


def parse_file(l):
    clean = []
    fact_buff = {}
    rules_buff = []
    input_buff = []
    find_buff = []
    find_list = []
    for line in l:
        line = line.replace("!", "not ")
        line = line.replace("(", " ( ")
        line = line.replace(")", " ) ")
        new = line.split('#', 1)[0]
        new = ' '.join(new.split())
        if new:
            clean.append(new)
    for line in clean:
        if line[0] == '=':
            for fact in line[1:]:
                if fact in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    fact_buff[fact] = "True"
            input_buff.append(fact_buff)
            fact_buff = {}
        elif '=>' in line:
            if line not in rules_buff:
                rules_buff.append(line)
        elif line[0] == '?':
            for fact in line[1:]:
                if fact in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    find_list.append(fact)
            find_buff.append(find_list)
            find_list = []
    for f in input_buff:
        for ask in find_buff:
            print("-" * 80)
            if f:
                for key, val in f.items():
                    print(Colors.BLUE + key, ":", str(val) + Colors.END)
            else:
                print(Colors.BLUE + "All False" + Colors.END)
            for some in ask:
                print(Colors.BLUE + some, "= ?" + Colors.END)
            for elem in ask:
                get_res(elem, f, rules_buff)


def get_file():
    if os.path.exists(sys.argv[1]):
        f = open(sys.argv[1], 'r')
        if os.path.getsize(sys.argv[1]) > 0:
            l = [line.strip() for line in f]
        else:
            f.close()
            sys.exit()
        f.close()
        parse_file(l)
    else:
        print("File not found, try again")
        sys.exit()


def main():
    if len(sys.argv) == 2:
        get_file()
    else:
        print("The program should receive one argument.")


if __name__ == '__main__':
    main()
