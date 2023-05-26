import os, re, copy

import prepare_dictionary
if not os.path.exists('resources/dictionary_1_patterns.py'):
    prepare_dictionary.main()
from resources.dictionary_1_patterns import all_patterns


LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


def get_blank_cipher_letter_mapping():
    return {
        'А': [],
        'Б': [],
        'В': [],
        'Г': [],
        'Д': [],
        'Е': [],
        'Ё': [],
        'Ж': [],
        'З': [],
        'И': [],
        'Й': [],
        'К': [],
        'Л': [],
        'М': [],
        'Н': [],
        'О': [],
        'П': [],
        'Р': [],
        'С': [],
        'Т': [],
        'У': [],
        'Ф': [],
        'Х': [],
        'Ц': [],
        'Ч': [],
        'Ш': [],
        'Щ': [],
        'Ъ': [],
        'Ы': [],
        'Ь': [],
        'Э': [],
        'Ю': [],
        'Я': [],
    }


def add_letters_to_mapping(letter_mapping, cipher_word, candidate):
    letter_mapping = copy.deepcopy(letter_mapping)
    for i in range(len(cipher_word)):
        if candidate[i] not in letter_mapping[cipher_word[i]]:
            letter_mapping[cipher_word[i]].append(candidate[i])
    return letter_mapping


def intersect_mappings(mapA, mapB):
    # """ объединяем два словаря, добавляем только общие для обоих записи """
    """ объединяем два словаря"""
    result = get_blank_cipher_letter_mapping()
    for letter in LETTERS:
        if mapA[letter] == []:
            result[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            result[letter] = copy.deepcopy(mapA[letter])
        else:
            # for mapped_letter in mapA[letter]:
            #     if mapped_letter in mapB[letter]:
            #         result[letter].append(mapped_letter)
            for mapped_letter in mapA[letter]:
                result[letter].append(mapped_letter)
    return result


def read_text(file_path):
    with open(file_path, encoding='utf-8') as file:
        return file.read().upper()


def get_all_includes(text: str, word: str, word_pattern: str):
    """ Собираем все уникальные подстроки, соответствующие шаблону известного слова"""
    l = []
    word_len = len(word)
    for i in range(len(text) - word_len + 1):
        sub = text[i: i + word_len]
        sub_pattern = prepare_dictionary.get_word_pattern(sub)
        # print(f'{i}  {sub}: {sub_pattern}')  # вывод всех построенных шаблонов 
        if sub_pattern == word_pattern:
            l.append(i)

    q = {}
    if len(l)>0:
        print(f"Обнаруженные комбинации букв, соответствующие шаблону заданного слова '{word}'")

    for i in l:
        w = text[i:i+len(word)]
        print(f"{i+1}: {w}")

        if w not in q.values():
            q[i] = text[i:i+len(word)]
    return q.keys()


def get_word_from_text(text: str, start: int, wordlen: int):
    word = text[start:start+wordlen]
    pattern = prepare_dictionary.get_word_pattern(word)
    return word, pattern


def get_re_by_partial_key(word: str, partial_key: dict):
    """ Строим шаблон для регулярки на основании проверяемого 
    слова и 'известных' расшифровок букв"""
    res = {}
    s = []
    for key, val in enumerate(word):
        if val in partial_key:
            res[key] = partial_key[val]
            s.append(partial_key[val])
        else:
            s.append('.')
    return res, ''.join(s)


def get_word_exists(words: list[str], word_re: str):
    """ Выбираем из списка слов те, которые соответствуют регулярке """
    res = []
    for word in words:
        w = word.upper()
        q = re.fullmatch(pattern=word_re, string=w)
        if q is not None:
            res.append(word)
    return res


def text_to_words(text: str, partial_key: dict):
    words = []
    words_d = {}
    start = 0
    word_len = 1

    isLast = False

    while True:
        if start + word_len > len(text):
            break
        
        # на всякий случай
        if word_len == 0:
            break
        
        word_candidate, word_candidate_pattern = get_word_from_text(text, start, word_len)

        if word_candidate_pattern in all_patterns and not isLast:
            word_len += 1
        else:
            while True:
                word_len -= 1
                word_candidate, word_candidate_pattern = get_word_from_text(text, start, word_len)
                known_letters, word_re = get_re_by_partial_key(word_candidate, partial_key)

                # слова из словаря, соответствующие
                dictionary_words = all_patterns[word_candidate_pattern]

                # выбираем из словарных слов те, у которых на определённых местах
                # соответствующие буквы

                words_exists = get_word_exists(dictionary_words, word_re)
                if len(words_exists) == 0:
                    continue

                # записываем результат, смещаем поиск 
                words_d[word_candidate] = words_exists
                words.append(word_candidate)
                start += word_len
                word_len = 1
                break
    return words, words_d


def get_partial_key(encoded_word: str, known_word: str):
    res = {}
    for key, val in enumerate(encoded_word):
        res[val] = known_word[key]
    return res


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


def some_decode_magic(cipher_text, letter_map):
    res = []
    for l in cipher_text:
        if len(letter_map[l]) == 1:
            res.append(letter_map[l][0])
        else:
            res.append('-')
    return ''.join(res)


def map_to_key(map):
    key = ['_'] * len(LETTERS)

    for l in LETTERS:
        if len(map[l]) == 1:  # иначе для буквы нет расшифровки
            key_index = LETTERS.find(map[l][0])
            key[key_index] = l
    res = ''.join(key)
    return res


def create_keys(letter_mapping):
    key_dictionaries = []

    def create_keys_worker(letter_mapping):
        for cipher_letter in LETTERS:
            values = letter_mapping[cipher_letter]
            if len(values) > 1:
                for v in values:
                    new_mapping = copy.deepcopy(letter_mapping)
                    new_mapping[cipher_letter] = [v]
                    new_mapping = remove_solved_letters_from_mapping(new_mapping)

                    keys = create_keys_worker(new_mapping)
                    key_str = map_to_key(keys)
                    if key_str not in key_dictionaries:
                        key_dictionaries.append(key_str)
        return letter_mapping
    
    create_keys_worker(letter_mapping)
    return key_dictionaries


def solve_by_known_word(cipher_text_path: str, known_word: str, folder_for_results: str) -> None:
    cipher_text = read_text(cipher_text_path)
    known_word_pattern = prepare_dictionary.get_word_pattern(known_word)
    print(f"{known_word}: {known_word_pattern}")

    includes = get_all_includes(cipher_text, known_word, known_word_pattern)

    if len(includes) == 0:
        print(f"Возможных включений слова {known_word} в тексте не обнаружено")
    
    for i in includes:
        """ Обрабатываем текст с учетом подходящих включений известного слова"""
        # предполагаемая шифровка известного слова
        known_word_encoded = cipher_text[i : i + len(known_word)]
        # словарь соответствий зашифрованных букв к расшифрованным
        partial_key = get_partial_key(known_word_encoded, known_word)
        words, words_d = text_to_words(cipher_text, partial_key)

        # основной словарь соответствий
        intersect_map = get_blank_cipher_letter_mapping()

        # строим словарь
        for word in words_d:
            new_map = get_blank_cipher_letter_mapping()

            for candidate in words_d[word]:
                new_map = add_letters_to_mapping(new_map, word.upper(), candidate.upper())
            
            intersect_map = intersect_mappings(intersect_map, new_map)

        # чистим словарь
        letter_mapping = remove_solved_letters_from_mapping(intersect_map)

        # Показываем тест, расшифрованный однозначно определёнными буквами
        some_result = some_decode_magic(cipher_text, letter_mapping)
        print(some_result)

        keys = create_keys(letter_mapping)

        with open(f'{folder_for_results}keys_{i}.txt', 'w', encoding='utf-8') as file:
            for i in keys:
                file.write(i)
                file.write('\n')


if __name__=="__main__":
    known_word = "КРИПТОАНАЛИЗ"
    cipher_text_path = "resources/text.txt"
    folder_for_results = "results/"

    solve_by_known_word(cipher_text_path, known_word, folder_for_results)