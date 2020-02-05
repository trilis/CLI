import re
from src import enviroment


def find_quotes(string):
    ans = []
    suffix = string
    offset = 0
    while True:
        dq = re.search("\"[^\"]*\"", suffix)
        sq = re.search("\'[^\']*\'", suffix)
        if dq is None and sq is None:
            return ans
        elif dq is None or sq is not None and dq.start() > sq.start():
            qs, qe = sq.start(), sq.end()
            ans.append((qs + offset, qe - 1 + offset, "s"))
            offset += qe
            suffix = suffix[qe:]
        elif sq is None or dq is not None and dq.start() < sq.start():
            qs, qe = dq.start(), dq.end()
            ans.append((qs + offset, qe - 1 + offset, "d"))
            offset += qe
            suffix = suffix[qe:]


def tokenize(string, token, double_quotes_respect=True):
    token_inds = [s.start() for s in re.finditer(token, string)]
    quotes = find_quotes(string)

    def in_quotes(i):
        return any([s < i < e and (type == "s" or double_quotes_respect) for s, e, type in quotes])

    split_inds = [-1] + [i for i in token_inds if not in_quotes(i)] + [len(string)]
    return [string[split_inds[i] + 1:split_inds[i + 1]] for i in range(len(split_inds) - 1)]


def insert_vars(string):
    parts = tokenize(string, "\$\w+", double_quotes_respect=False)
    answer = parts[0]
    for part in parts[1:]:
        name_end = re.search("^\w+", part).end()
        answer += enviroment.get_value(part[:name_end]) + part[name_end:]
    return answer


def peel(word):
    quotes = find_quotes(word)
    quotes_inds = []
    for q in quotes:
        quotes_inds += [q[0], q[1]]
    return "".join([word[i] for i in range(len(word)) if i not in quotes_inds])


def parse(string):
    commands = tokenize(string, "\|")
    commands = [insert_vars(c) for c in commands]
    commands_parts = [[peel(w) for w in tokenize(c, "\s") if w != ""] for c in commands]
    return commands_parts
