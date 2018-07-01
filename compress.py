def to_bin(num):
    return bin(num)[2:]

def zero_prefix_len(bin):
    return len(bin.split('1')[0])

def encode_unary(nums):
    encoded = ''
    for num in nums:
        for _ in range(num - 1):
            encoded += '0'
        encoded += '1'
    return encoded

def encode_gamma(nums):
    final = ''
    for num in nums:
        binary = to_bin(num)
        pre = encode_unary([len(binary)])[:-1]
        final += pre + binary
    return final

def encode_delta(nums):
    final = ''
    for num in nums:
        gamma = encode_gamma([num])
        z_num = zero_prefix_len(gamma)
        remainder = gamma[z_num + 1 :]
        prefix = encode_gamma([z_num + 1])
        final += prefix + remainder
    return final

def encode_vByte(nums):
    final = ''
    for num in nums:
        #reverse binary bits so they can be processed lsb -> msb
        rev_bin = to_bin(num)[::-1]
        sets_of_7 = len(rev_bin) // 7 if len(rev_bin) % 7 == 0 else len(rev_bin) // 7 + 1
        flags = ['1'] * sets_of_7
        flags[-1] = '0'
        sets = []
        joiner = ''
        for i in range(sets_of_7):
            s = ''
            if len(rev_bin) < i * 7 + 8:
                zeroes_needed = i * 7 + 7 - len(rev_bin)
                #leverage encode_unary to get a specific number of 0s
                zeroes = encode_unary([zeroes_needed + 1])[:-1]
                #add zeroes for encoding purposes and then reverse
                s = (rev_bin[(i * 7): (i * 7 + 7)] + zeroes)[::-1]
            else:
                s = rev_bin[(i * 7):(i * 7 + 7)][::-1]
            sets.append(flags[i])
            sets.append(s)
        final += joiner.join(sets)
    return final


def encode_f_o_r(nums):
    #returns [min_num, max_bin_digits, code]
    min_num = min(nums)
    gap = map(lambda x: x - min_num, nums)
    bin_gap = list(map(lambda dec: to_bin(dec), gap))
    max_bin_digits = max(map(lambda bin: len(bin), bin_gap))
    bin_correct_len = map(lambda bin: encode_unary([max_bin_digits - len(bin) + 1])[:-1] + bin, bin_gap)
    joiner = ''
    return [min_num, max_bin_digits, joiner.join(bin_correct_len)]


def print_code(functions, numbers, titles):
    for i in range(len(functions)):
        print(titles[i] + ": ")
        print('')
        for test in numbers:
            print('{}: {}'.format(test, functions[i]([test])))
        print("Final compression:")
        print(functions[i](numbers))
        print('')
        print('')


test_set = [20000]
titles = ['Unary', 'Gamma', 'Delta', 'vByte', 'Frame of Reference']
functions = [encode_unary, encode_gamma, encode_delta, encode_vByte, encode_f_o_r]

print_code(functions, test_set, titles)