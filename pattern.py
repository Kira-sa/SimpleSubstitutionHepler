# 1. считать текст из файла
# 2. по искомому слову построить индекс и вычислить длину
# 3. по длине искомого слова пройтись по тексту подстроками, посроить для них индекс и сравнить с искомым
#     1. если обнаружится - запомнить позицию
#     2. если не обнаружится - продолжить, пока не закончится текст
# 4. по звершению обхода
#     1. если слово было обнаружено, произвести замену известных букв и вывести сообщение пользователю
#     2. если слово не было обнаружено - сообщить пользователю что ничего не найдено

import re


from prepare_dictionary import get_word_pattern, prepare_dictionaries


cipher_text = ''
known_word = 'КРИПТОАНАЛИЗ'
known_word_len = len(known_word)
known_word_pattern = ''
includes = []  # место для записии обнаруженных включений


dictionary_patterns = {}
partial_key = {}


def read_text():
    with open('resources/text.txt', encoding='utf-8') as file:
        return file.read()


def get_all_includes(text: str, word: str):
    result = []
    word_len = len(word)
    for i in range(len(text) - word_len + 1):
        sub = text[i: i + word_len]
        sub_pattern = get_word_pattern(sub)
        # print(f'{i}  {sub}: {sub_pattern}')  # вывод всех построенных шаблонов 
        if sub_pattern == known_word_pattern:
            # print("EURICA!")
            result.append(i)
    return result


def get_partial_decode(text, key):
    res = ''
    for i in text:
        if i in key:
            res += key[i].upper()
        else:
            res += i.lower()
    return res


def get_partial_key(encoded_word, known_word):
    res = {}
    for key, val in enumerate(encoded_word):
        res[val.lower()] = known_word[key].lower()
    return res


def text_to_words(text):
    """ пробуем разбить текст на слова, без учета известного слова """
    words = []
    words_d = {}
    start = 0
    word_len = 1

    while True:
        # если доползли до конца, то всё (на потерю последнего слова пока забьём)
        if start + word_len > len(text):
            break
        
        # берём слово
        word_candidate = text[start:start+word_len]
        word_candidate_pattern = get_word_pattern(word_candidate)

        if word_candidate_pattern in dictionary_patterns:
            # шаблон есть, продолжим проверять увеличив слово на 1 символ
            word_len += 1
        else:
            # похоже такого слова нет
            # откатываем назад
            # изменяем индексы
            # пробуем взять слово и записать его в words

            # aa = dictionary_patterns.get(word_candidate_pattern) is None  # проверка что по ключу можно взять значение из словаря
            while True:
                word_len -= 1
                # обновляем слово, пересчитываем
                word_candidate = text[start:start+word_len]
                word_candidate_pattern = get_word_pattern(word_candidate)

                if dictionary_patterns.get(word_candidate_pattern) is None:
                    # ошибка сравнения, откатываем индекс еще назад
                    continue
                
                words_d[word_candidate] = dictionary_patterns[word_candidate_pattern]
                words.append(word_candidate)
                start += word_len
                # успех, выходим
                break
                
    return words


def text_to_words_known(text):
    """ пробуем разбить текст на слова с учетом известного слова """
    words = []
    words_d = {}
    start = 0
    word_len = 1

    l = len(text)
    isLast = False

    while True:
        # если доползли до конца, то проверяем последнее слово
        if start + word_len > len(text):
            if isLast:
                break
            else:
                isLast = True

        # берём слово
        word_candidate = text[start:start+word_len]
        word_candidate_pattern = get_word_pattern(word_candidate)  # определяем паттерн слова
        word_candidate_known_letters, word_map = check_known_letters(word_candidate)  # определяем какие буквы точно должны быть в искомом слове

        if word_candidate_pattern in dictionary_patterns and not isLast:
            # шаблон есть, продолжим проверять увеличив слово на 1 символ
            word_len += 1
        else:
            # похоже такого слова нет
            # откатываем назад
            # изменяем индексы
            # пробуем взять слово и записать его в words

            # aa = dictionary_patterns.get(word_candidate_pattern) is None  # проверка что по ключу можно взять значение из словаря
            while True:
                word_len -= 1
                # обновляем слово, пересчитываем
                word_candidate = text[start:start+word_len]
                word_candidate_pattern = get_word_pattern(word_candidate)
                word_candidate_known_letters, word_map = check_known_letters(word_candidate)

                # ошибка сравнения, откатываем индекс еще назад
                if dictionary_patterns.get(word_candidate_pattern) is None:
                    continue

                # слова из словаря
                d_words = dictionary_patterns[word_candidate_pattern]

                # если в подходящем индексе нет слов с подходящими буквами, откатываем индекс назад
                words_exists = get_word_exists(d_words, word_candidate_known_letters, word_map)
                if len(words_exists) == 0:
                    continue
                
                words_d[word_candidate] = words_exists
                words.append(word_candidate)
                start += word_len
                word_len = 1
                # успех, выходим
                break

    return words, words_d


def get_word_exists(d_words, letters, word_map):
    """ проверяем регуляркой что слово соответствует маске
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
    res = {}
    s = []
    for key, val in enumerate(word):
        if val in partial_key:
            res[key] = partial_key[val]
            s.append(partial_key[val])
        else:
            s.append('.')
    return res, "".join(s)


def use_dictionary_1():
    from resources.dictionary_1_patterns import all_patterns
    return all_patterns


if __name__ == "__main__":
    print("Подготовка словарей...")
    prepare_dictionaries()
    print("Подготовка словарей завершена")

    dictionary_patterns = use_dictionary_1()

    known_word_pattern = get_word_pattern(known_word)
    print(f'{known_word}: {known_word_pattern}')

    cipher_text = read_text().lower()
    includes = get_all_includes(cipher_text, known_word)
    print(f'Включения известного слова: {includes}')

    if len(includes) > 0:
        # собираем частичный ключ по известному слову
        partial_key = get_partial_key(cipher_text[includes[0] : includes[0] + known_word_len], known_word)
        partial_decoded_text = get_partial_decode(cipher_text, partial_key)
    
        print(f'Исходный текст:')
        print(cipher_text)
        print(f'Предположительный текст:')
        print(partial_decoded_text)
    
    else:
        print("Возможных включений известного слова в тексте не обнаружено")

    # words = text_to_words(cipher_text)
    words, words_d = text_to_words_known(cipher_text)
    print(words)
    for i in words_d:
        print(f'{i}: {words_d[i]}')

    # дополнительное:
    # 5. грузим словарь и строим шаблоны для всех слов
    # 6. проходим по шифротексту, скользящим срезом проходим его в поиске слов
    # 7. ?? строим с возможными вариантами замены букв (с учетом известного слова)
    # 8. чистим словарь
    # 9. собираем ключ
    # get_all_patterns_from_dictionary()

    # magic(cipher_text)
    
