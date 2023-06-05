import itertools

rus_vowels = ['о', 'е', 'а', 'и', 'у', 'я', 'ы', 'ю', 'э']
rus_consonants = ['н', 'т', 'с', 'р', 'в', 'л', 'к', 'м', 'д', 'п', 'з', 'ь', 'б', 'г', 'ч', 'й', 'х', 'ж', 'ш', 'ц',
                  'щ', 'ф']


def decode_by_key_dictionary(cipher_text, key_dict):
    res = []
    if len(key_dict) == 0:
        print("Перечень расшифрованных букв пуст")
    for i in cipher_text:
        if i in key_dict:
            res += key_dict[i]
        else:
            res += '-'
    return ''.join(res)


def try_permutations(cipher_text, voe, cons, known_letters):
    deciphers = []
    # построить перестановками все варианты ключей
    if len(known_letters) == 0:
        all_keys = get_all_permutations(voe, cons)
    else:
        all_keys = get_all_permutations_by_known(voe, cons, known_letters)
    # построить расшифровки по ключам
    for i in all_keys:
        q = decode_by_key_dictionary(cipher_text, i)
        deciphers.append(q)
    return deciphers


def get_all_perm(letters, rus_letters):
    count = min(len(letters), len(rus_letters))
    possible_letters = rus_letters[:count]
    letters_perm = list(itertools.permutations(possible_letters))
    return letters_perm


def get_all_vowel_perm(vowels, rus_vowels):
    return get_all_perm(vowels, rus_vowels)


def get_all_cons_perm(consonants, rus_consonants):
    return get_all_perm(consonants, rus_consonants)


def get_all_permutations(vowels, consonants):
    # построить перестановки vowels
    possible_vowels_perm = get_all_vowel_perm(vowels, rus_vowels)

    # построить перестановки consonants
    possible_consonants_perm = get_all_cons_perm(consonants, rus_consonants)

    # построить перемноженные ключи vowels * consonants
    result = []
    for i in possible_consonants_perm:
        for j in possible_vowels_perm:
            d = {}
            for key, value in enumerate(vowels):
                d[value] = j[key]
            for key, value in enumerate(consonants):
                d[value] = i[key]
            result.append(d)
    return result


def get_all_permutations_by_known(vowels, consonants, known_l):
    # построить перестановки vowels
    possible_vowels_perm = get_all_vowel_perm(vowels, rus_vowels)

    # построить перестановки consonants
    possible_consonants_perm = get_all_cons_perm(consonants, rus_consonants)

    # построить перемноженные ключи с учетом "известных букв"
    result = []
    for i in possible_consonants_perm:
        for j in possible_vowels_perm:
            d = {}
            for key, value in enumerate(vowels):
                d[value] = j[key]
            for key, value in enumerate(consonants):
                d[value] = i[key]
            isValid = True
            for l in known_l:
                if l in d and known_l[l] != d[l]:
                    isValid = False
            if isValid:
                d.update(known_l)
                result.append(d)
    return result


def get_all_permutations_for_sets(letters_sets) -> list[dict]:
    """ Возвращаем список словарей - ключей """
    result = []
    cipher_letters = letters_sets[:len(letters_sets) // 2]
    decipher_letters = letters_sets[len(letters_sets) // 2:]
    print(cipher_letters)
    print(decipher_letters)
    perm = list(itertools.permutations(decipher_letters))

    for i in perm:
        d = dict(zip(cipher_letters, i))
        result.append(d)
    
    return result


def get_all_permutations_for_sets_with_known(letters_sets, known_letters):
    """ Берем потенциальный список ключей, берем только те ключи 
    где если пересечения ключ-значение с известными парами букв +
    добавляем в ключ известные пары если они отстутствуют """
    pre_results = get_all_permutations_for_sets(letters_sets)
    results = []
    for key, value in enumerate(pre_results):
        isValid = True
        for letter in value:
            if letter in known_letters:
                if known_letters[letter] != value[letter]:
                    isValid = False
                    break
        if isValid:
            v = value.copy()  # почему-то если склеить эти две команды
            v.update(known_letters)  # то результат None (?)
            results.append(v)

    return results


def try_permutations_for_sets(cipher_text, set_string, known_letters):
    """ Вариант перебора всех ключей когда пользователем задаётся множество:
    шифрбуквы - расшифровки, из которых собираются все возможные пары ключей и значений. 
    Возможно присутствие гласных и согласных вперемешку. """
    deciphers = []
    
    if len(known_letters) == 0:
        # пользователем не заданы точно определённые сочетания
        all_keys = get_all_permutations_for_sets(set_string)
    else:
        # пользователем заданы некоторые точно определённые сочетания,
        # учитываем их при переборе
        all_keys = get_all_permutations_for_sets_with_known(set_string, known_letters)
    
    for i in all_keys:
        q = decode_by_key_dictionary(cipher_text, i)
        deciphers.append(q)

    return deciphers
