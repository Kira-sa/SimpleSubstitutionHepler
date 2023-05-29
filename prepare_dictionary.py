"""
prepare dictionaries if its not
"""

import pprint
import os.path

dictionaries = [
    "resources/dictionary_1.txt",
    "resources/dictionary_2.txt"
]


def get_word_pattern(word: str) -> str:
    """Определение повторяющихся букв в слове. Возвращает шаблон повторяющихся букв"""
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


def get_all_patterns_from_dictionary(dictionary_path):
    all_patterns = {}  # все шаблоны слов из словаря

    with open(dictionary_path, encoding='utf-8') as file:
        word_list = file.read().split('\n')

    for word in word_list:
        pattern = get_word_pattern(word)

        if pattern not in all_patterns:
            all_patterns[pattern] = [word]
        else:
            all_patterns[pattern].append(word)

    with open(name_to_patterns(dictionary_path), 'w', encoding='utf-8') as file:
        file.write('all_patterns = ')
        file.write(pprint.pformat(all_patterns))


def name_to_patterns(d_name):
    return "".join([d_name[:-4], "_patterns.py"])


def prepare_dictionaries():
    for i in dictionaries:
        if not os.path.exists(name_to_patterns(i)):
            print(f"Подготавливаем {i}")
            get_all_patterns_from_dictionary(i)
            print(f"Подготовка {i} завершена")


def main():
    prepare_dictionaries()

# if __name__ == "__main__":
#     main()
