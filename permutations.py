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


def try_permutations(cipher_text, voe, cons):
    deciphers = []
    # построить перестановками все варианты ключей
    all_keys = get_all_permutations(voe, cons)
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
                result.append(d)
    return result


if __name__ == "__main__":
    vowels = ['з', 'и', 'э', 'д']
    consonants = ['г', 'с', 'л', 'т', 'п', 'у', 'м', 'ф']
    known_letters = {'з': 'о', 'и': 'а', 'г': 'н'}
    # result_key = get_all_permutations(vowels, consonants)
    res = get_all_permutations_by_known(vowels, consonants, known_letters)
    a = 23