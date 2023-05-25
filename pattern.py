# 1. считать текст из файла
# 2. по искомому слову построить индекс и вычислить длину
# 3. по длине искомого слова пройтись по тексту подстроками, посроить для них индекс и сравнить с искомым
#     1. если обнаружится - запомнить позицию
#     2. если не обнаружится - продолжить, пока не закончится текст
# 4. по звершению обхода
#     1. если слово было обнаружено, произвести замену известных букв и вывести сообщение пользователю
#     2. если слово не было обнаружено - сообщить пользователю что ничего не найдено

import os, re, copy

import prepare_dictionary

if not os.path.exists('resources/dictionary_1_patterns.py'):
    prepare_dictionary.main()

from resources.dictionary_1_patterns import all_patterns

LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

cipher_text = ''
known_word = 'КРИПТОАНАЛИЗ'
known_word_len = len(known_word)
includes = []  # место для записии обнаруженных включений
key_dictionaries = []  # место для потенциальных ключей


partial_key = {}  # словарь соответствия шифрованных букв буквам из известного слова


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


def read_text():
    with open('resources/text.txt', encoding='utf-8') as file:
        return file.read()


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


def get_partial_decode(text, key):
    res = ''
    for i in text:
        if i in key:
            res += key[i].upper()
        else:
            res += i.lower()
    return res


def get_partial_key(encoded_word: str, known_word: str) -> dict:
    """ Составляем словарь соответствия зашифрованных букв -> к буквам из известного слова"""
    res = {}
    for key, val in enumerate(encoded_word):
        res[val.lower()] = known_word[key].lower()
    return res


def from_text_to_word(text, start, wordlen):
    word = text[start:start+wordlen]
    pattern = prepare_dictionary.get_word_pattern(word)
    return word, pattern


def text_to_words_known(text):
    """ пробуем разбить текст на слова с учетом известного слова """
    words = []
    words_d = {}
    start = 0
    word_len = 1

    l = len(text)
    isLast = False

    # цикл обхода шифрограммы
    while True:
        # если доползли до конца, то проверяем последнее слово
        if start + word_len > len(text):
            if isLast:
                break
            else:
                isLast = True

        # берём слово
        word_candidate, word_candidate_pattern = from_text_to_word(text, start, word_len)  # определяем паттерн слова

        if word_candidate_pattern in all_patterns and not isLast:
            # шаблон есть, продолжим проверять увеличив слово на 1 символ
            word_len += 1
        else:
            # похоже такого слова нет, уменьшаем слово на 1, 
            # индекс гарантированно должен быть в словаре, 
            # поэтому проверяем соответствие известным буквам
            # aa = all_patterns.get(word_candidate_pattern) is None  # проверка что по ключу можно взять значение из словаря
            
            # цикл обхода предполагаемого слова 
            while True:
                word_len -= 1
                word_candidate, word_candidate_pattern = from_text_to_word(text, start, word_len)
                known_letters, word_map = check_known_letters(word_candidate)

                # слова из словаря, соответствующие шаблону
                d_words = all_patterns[word_candidate_pattern]

                # если в подходящем индексе нет слов с подходящими буквами, уменьшаем длину слова, повторяем
                words_exists = get_word_exists(d_words, word_map)
                if len(words_exists) == 0:
                    continue
                
                # записываем результат
                words_d[word_candidate] = words_exists
                words.append(word_candidate)
                start += word_len
                word_len = 1
                # успех, выходим
                break

    return words, words_d


def get_word_exists(d_words, word_map):
    """ 
    проверяем регуляркой что слова соответствуют маске
    если нашли - возращаем эти слова
    если нет - список пустой
    """
    res = []

    for word in d_words:
        q = re.fullmatch(pattern=word_map, string=word)
        if q is not None:
            res.append(word)

    return res


def check_known_letters(word):
    """ Строим шаблон для регулярки 
        на основании проверяемого слова и 'известных' расшифровок букв
    """
    res = {}
    s = []
    for key, val in enumerate(word):
        if val in partial_key:
            res[key] = partial_key[val]
            s.append(partial_key[val])
        else:
            s.append('.')
    return res, "".join(s)


def create_keys(letter_mapping):
    for cipher_letter in LETTERS:
        values = letter_mapping[cipher_letter]
        if len(values) > 1:
            for v in values:
                new_mapping = copy.deepcopy(letter_mapping)
                new_mapping[cipher_letter] = [v]
                new_mapping = remove_solved_letters_from_mapping(new_mapping)

                keys = create_keys(new_mapping)
                key_str = map_to_key(keys)
                if key_str not in key_dictionaries:
                    key_dictionaries.append(key_str)
    return letter_mapping


def map_to_key(map):
    key = ['_'] * len(LETTERS)

    for l in LETTERS:
        if len(map[l]) == 1:  # иначе для буквы нет расшифровки
            key_index = LETTERS.find(map[l][0])
            key[key_index] = l
    res = ''.join(key)
    return res

if __name__ == "__main__":
    known_word_pattern = prepare_dictionary.get_word_pattern(known_word)
    print(f'{known_word}: {known_word_pattern}')

    cipher_text = read_text().lower()
    includes = get_all_includes(cipher_text, known_word, known_word_pattern)

    if len(includes) == 0:
        print("Возможных включений известного слова в тексте не обнаружено")

    for i in includes:
        """ Обрабатываем текст с учетом подходящих включений известного слова"""
        # Получаем частичную расшифровку, из букв известного слова
        partial_key = get_partial_key(cipher_text[i : i + known_word_len], known_word)

        # Частично декодированный текст с учетом букв из известного слова
        partial_decoded_text = get_partial_decode(cipher_text, partial_key)  
    
        print(f'Исходный текст:')
        print(cipher_text)
        print(f'Предположительный текст:')
        print(partial_decoded_text)

        # words = text_to_words(cipher_text)
        words, words_d = text_to_words_known(cipher_text)

        # вывод списка предполагаемых слов и из потенциальных расшифровок из словаря
        # print(words)
        # for i in words_d:
        #     print(f'{i}: {words_d[i]}')

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

        
        # собираем ключи
        create_keys(letter_mapping)

        with open('resources/keys.txt', 'w', encoding='utf-8') as file:
            for i in key_dictionaries:
                file.write(i)
                file.write('\n')
        
        a = 23
        # расшифровываем сообщение
        # записываем в results
