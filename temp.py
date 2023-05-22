# sample from book
# Simple Substitution Cipher Hacker

import os, re, copy, pprint
import prepare_dictionary


if not os.path.exists('resources/dictionary_1_patterns.py'):
    prepare_dictionary.main()

from resources.dictionary_1_patterns import all_patterns

LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


def read_text():
    with open('resources/text.txt', encoding='utf-8') as file:
        return file.read()


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
    """ объединяем два словаря, добавляем только общие для обоих записи """
    result = get_blank_cipher_letter_mapping()
    for letter in LETTERS:
        if mapA[letter] == []:
            result[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            result[letter] = copy.deepcopy(mapA[letter])
        else:
            for mapped_letter in mapA[letter]:
                if mapped_letter in mapB[letter]:
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

        for cipher_letter in LETTERS:
            for s in solved_letters:
                if len(letter_mapping[cipher_letter]) != 1 and s in letter_mapping[cipher_letter]:
                    letter_mapping[cipher_letter].remove(s)
                    if len(letter_mapping[cipher_letter]) == 1:
                        loop_again = True
    
    return letter_mapping


def hackSimpleSub(text):
    intersect_map = get_blank_cipher_letter_mapping()
    cipher_word_list = 'test'  # TODO: список слов, приведенных к верхнему регистру
    for cipher_word in cipher_word_list:
        new_map = get_blank_cipher_letter_mapping()
        word_pattern = prepare_dictionary.get_word_pattern(cipher_word)
        
        # TODO: проверку переделать с учетом того что мы уже находим подходящие слова
        if word_pattern not in all_patterns:
            continue

        for candidate in all_patterns[word_pattern]:
            new_map = add_letters_to_mapping(new_map, cipher_word, candidate)

        intersected_map = intersect_mappings(intersect_map, new_map)

    return remove_solved_letters_from_mapping(intersected_map)


def decrypt_with_cipher_letter_mapping(cipher_text, letter_mapping):
    key = ['x'] * len(LETTERS)

    for cipher_letter in LETTERS:
        if len(letter_mapping[cipher_letter]) == 1:
            key_index = LETTERS.find(letter_mapping[cipher_letter][0])
            key[key_index] = cipher_letter
        else:
            # TODO: ?!
            cipher_text = cipher_text.replace(cipher_letter.lower(), '_')
            cipher_text = cipher_text.replace(cipher_letter.upper(), '_')
    
    key = ''.join(key)

    return key


def main():
    text = read_text().lower()

    letter_mapping = hackSimpleSub(text)

    print('Mapping')
    pprint.pprint(letter_mapping)
    print()
    print('Оригинальный текст:')
    print(text)
    print()

    solved_text = decrypt_with_cipher_letter_mapping(text, letter_mapping)

    print('Расшифрованный текст:')
    print(solved_text)


if __name__ == "__main__":
    main()

