# analyze.py
# Credit to Kostia Howard '24 for working logic in hard-hard vowel detection.

def analyze_non_contiguous(text):
    hard_vowels = set(['а', 'о', 'у', 'ы', 'э', 'и'])
    ignore_char = set([' ', '.', ',', '\n', '\\', '(', ')',
                      '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

    combo_freq = {}
    combo_line_num = {}
    char_count = 0
    prev = ''  # Takes previous if hard vowel, else empty

    highlighted_result = ""
    non_contig = 0
    for line_num, line in enumerate(text.splitlines()):
        add_line = ''
        for curr in line:
            add_line += curr
            char_count += 1

            if curr in hard_vowels or str(curr).lower() in hard_vowels:
                # if prev char is also a hard vowel
                if prev != '':
                    non_contig += 1
                    combo = prev + curr
                    combo_freq[combo] = combo_freq.get(combo, 0) + 1

                    if combo not in combo_line_num:
                        combo_line_num[combo] = []
                    combo_line_num[combo].append(line_num + 1)

                    # Remove characters until beginning of pattern
                    add_back = ''
                    while len(add_line) and (add_line[-1] in ignore_char or
                                             str(add_line[-1]).lower() in hard_vowels):
                        add_back += add_line[-1]
                        add_line = add_line[:-1]

                    # Keep sliding backwards onto previous line, if necessary
                    if len(add_line) == 0:
                        while (highlighted_result[-1] in ignore_char or
                        str(highlighted_result[-1]).lower() in hard_vowels):
                            add_back += highlighted_result[-1]
                            highlighted_result =highlighted_result[:-1]

                    # Add back the already scanned letters, now surrounded by yellow highlight
                    add_line += (
                        f'<span style="background-color: #FFFF00">{add_back[::-1]}</span>')

                prev = curr
            elif curr in ignore_char and prev != '':
                continue
            else:
                prev = ''

        highlighted_result += add_line + '\n'

    return highlighted_result, combo_freq, combo_line_num


def analyze_contiguous(text):
    hard_vowels = set(['а', 'о', 'у', 'ы', 'э', 'и'])
    combo_freq = {}
    combo_line_num = {}
    char_count = 0
    prev = ''  # Takes previous if hard vowel, else empty

    highlighted_result = ""
    non_contig = 0
    for line_num, line in enumerate(text.splitlines()):
        add_line = ''
        for curr in line:
            add_line += curr
            char_count += 1

            if curr in hard_vowels or str(curr).lower() in hard_vowels:
                # if prev char is also a hard vowel
                if prev != '' and len(add_line) != 1:
                    non_contig += 1
                    combo = prev + curr
                    combo_freq[combo] = combo_freq.get(combo, 0) + 1

                    if combo not in combo_line_num:
                        combo_line_num[combo] = []
                    combo_line_num[combo].append(line_num + 1)
                    add_line = add_line[:-2] + (
                        f'<span style="background-color: #FFFF00">{combo}</span>')

                prev = curr

            else:
                prev = ''

        highlighted_result += add_line + '\n'

    return highlighted_result, combo_freq, combo_line_num
