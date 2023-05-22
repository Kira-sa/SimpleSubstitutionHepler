# 1. считать текст из файла
# 2. по искомому слову построить индекс и вычислить длину
# 3. по длине искомого слова пройтись по тексту подстроками, посроить для них индекс и сравнить с искомым
#     1. если обнаружится - запомнить позицию
#     2. если не обнаружится - продолжить, пока не закончится текст
# 4. по звершению обхода
#     1. если слово было обнаружено, произвести замену известных букв и вывести сообщение пользователю
#     2. если слово не было обнаружено - сообщить пользователю что ничего не найдено

import pprint


cipher_text = ''
known_word = 'КРИПТОАНАЛИЗ'
known_word_len = len(known_word)
known_word_pattern = ''
includes = []  # место для записии обнаруженных включений


all_patterns = {}  # все шаблоны слов из словаря


def read_text():
    with open('resources/text.txt', encoding='utf-8') as file:
        return file.read()


def get_word_pattern(word: str):
    """
    Определение повторяющихся букв в слове
    :param word: слово
    :return: шаблон повторяющихся букв
    """
    word = word.upper()
    next_number = 0
    letters = {}
    word_pattern = []

    for letter in word:
        if letter not in letters:
            letters[letter] = str(next_number)
            next_number += 1
        word_pattern.append(letters[letter])
    return '.'.join(word_pattern)


def get_all_patterns_from_dictionary():
    # all_patterns.clear ?
    word_list = []

    with open('resources/dictionary_1.txt', encoding='utf-8') as file:
        word_list = file.read().split('\n')

    for word in word_list:
        pattern = get_word_pattern(word)

        if pattern not in all_patterns:
            all_patterns[pattern] = [word]
        else:
            all_patterns[pattern].append(word)

    with open('resources/dictionary_1_patterns.py', 'w') as file:
        file.write('all_patterns = ')
        file.write(pprint.pformat(all_patterns))


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


def magic(text):

    buf = ''
    buf_len = 2
    for key in range(len(text) - buf_len):
        # берем предполагаемое слово и строим шаблон
        buf = text[key : key + buf_len]
        buf_pattern = get_word_pattern(buf)
        # ищем совпадения по шаблону со словарём
        pass
        # если совпадения есть, пробуем увеличить слово
        # если совпадений нет, уменьшаем слово - запомниаем совпавшие слова по шаблону
    pass



if __name__ == "__main__":
    print("start")
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

    
    # дополнительное:
    # 5. грузим словарь и строим шаблоны для всех слов
    # 6. проходим по шифротексту, скользящим срезом проходим его в поиске слов
    # 7. ?? строим с возможными вариантами замены букв (с учетом известного слова)
    # 8. чистим словарь
    # 9. собираем ключ
    # get_all_patterns_from_dictionary()

    # magic(cipher_text)
    
