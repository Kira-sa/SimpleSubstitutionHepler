import copy


LETTERS = "АБВГД"


key_dictionaries = []  # место для потенциальных ключей


def remove_solved_letters_from_mapping(letter_mapping):
    """ 
    исключаем потенциальные буквы из вариантов если уверены 
    что они однозначно могут принадлежать конкретным шифрам 
    """
    letter_mapping = copy.deepcopy(letter_mapping)
    loop_again = True

    while loop_again:
        loop_again = False

        # список букв, которые имеют только одно соответствие (!!!)
        solved_letters = []
        for cipher_letter in LETTERS:
            if len(letter_mapping[cipher_letter]) == 1:
                solved_letters.append(letter_mapping[cipher_letter][0])
            elif cipher_letter in letter_mapping.values():
                a = 23

        for cipher_letter in LETTERS:
            for s in solved_letters:
                if len(letter_mapping[cipher_letter]) != 1 and s in letter_mapping[cipher_letter]:
                    letter_mapping[cipher_letter].remove(s)
                    if len(letter_mapping[cipher_letter]) == 1:
                        loop_again = True
    
    return letter_mapping


def map_to_key(map):
    key = ['_'] * len(LETTERS)

    for l in LETTERS:
        if len(map[l]) == 1:  # иначе для буквы нет расшифровки
            key_index = LETTERS.find(map[l][0])
            key[key_index] = l
    res = ''.join(key)
    return res


def create_mapping_for_keys(letter_mapping):
    for cipher_letter in LETTERS:
        values = letter_mapping[cipher_letter]
        if len(values) > 1:
            for v in values:
                new_mapping = copy.deepcopy(letter_mapping)
                new_mapping[cipher_letter] = [v]
                new_mapping = remove_solved_letters_from_mapping(new_mapping)

                keys = create_mapping_for_keys(new_mapping)
                key_str = map_to_key(keys)
                if key_str not in key_dictionaries:
                    key_dictionaries.append(key_str)
    return letter_mapping


if __name__=="__main__":
    mapping = {
        'А': ['Б'], 
        'Б': ['В', 'Г'], 
        'В': ['Д'], 
        'Г': ['В', 'Г'], 
        'Д': ['А']
    }
    create_mapping_for_keys(mapping)
    for i in key_dictionaries:
        print(i)

    a = 23
