index_max = 100


def create_inverted_index():
    inverted_index = {}
    for i in range(0, index_max):
        lemma_file = open('lemmas/{}.txt'.format(i))
        for line in lemma_file:
            (lemma, tokens) = line.split(':')
            if lemma not in inverted_index:
                inverted_index[lemma] = []
            inverted_index[lemma].append(i)

    return inverted_index


def save_index(inverted_index):
    index_file = open('inverted_index.txt', 'w')
    for lemma in inverted_index.keys():
        index_file.write('{}: {}\n'.format(lemma, ' '.join(list(map(str, inverted_index[lemma])))))


index = create_inverted_index()
save_index(index)


def prepare(a):
    if isinstance(a, str):
        a = index[a]
    return a


def and_operand(a, b):
    a = prepare(a)
    b = prepare(b)

    return list(filter(lambda elem: elem in b, a))


def or_operand(a, b):
    a = prepare(a)
    b = prepare(b)

    s = set(a)
    s.update(b)

    return list(s)


def not_operand(a):
    a = prepare(a)

    return list(filter(lambda doc: doc not in a, range(0, index_max)))


def find_argument(s):
    chars = list(s)
    stack = []
    start_index = 0
    if "(" in s:
        start_index = s.index('(')
    for i in range(start_index, len(chars)):
        char = chars[i]
        if char == ')':
            stack.pop()
        elif char == '(':
            stack.append(i)

        if len(stack) == 0:
            return s[start_index + 1:i]


def process_argument(s: str):
    if "AND" not in s and "OR" not in s and "NOT" not in s:
        return index[s]
    if "NOT" in s:
        start_index = s.index('(')
        substr = s[start_index:]
        arg = find_argument(substr)
        return not_operand(process_argument(arg))
    if "AND" in s:
        parts = s.split("AND")
        left_arg = find_argument(parts[0])
        right_arg = find_argument(parts[1])
        return and_operand(
            process_argument(left_arg),
            process_argument(right_arg)
        )
    if "OR" in s:
        parts = s.split("OR")
        left_arg = find_argument(parts[0])
        right_arg = find_argument(parts[1])
        return or_operand(
            process_argument(left_arg),
            process_argument(right_arg)
        )


# print(index)
# print(index['сеть'])
# print(index['предоставление'])
# print(process_argument('(сеть) OR (предоставление)'))
# print(not_operand(or_operand('сеть', 'предоставление')))
# print(process_argument('NOT((сеть) OR (предоставление))'))

search = input('Введите запрос:')
print(process_argument(search))
