# dictionary_2 - отсортированный словарь без Ё
# dictionary_1 - отсортированный словарь слова с ё в конце

import collections
import argparse
from pathlib import Path
import sys
from simple_substitution_solver import solve_by_known_word, solve_by_partial_key, LETTERS
import permutations

rus_frequencies = {}
rus_vowels = ['о', 'е', 'а', 'и', 'у', 'я', 'ы', 'ю', 'э']
rus_consonants = ['н', 'т', 'с', 'р', 'в', 'л', 'к', 'м', 'д', 'п', 'з', 'ь', 'б', 'г', 'ч', 'й', 'х', 'ж', 'ш', 'ц',
                  'щ', 'ф']
vowels = []
consonants = []


def get_rus_frequencies() -> None:
    """Считывает из файла частоты для букв русского языка"""
    with open('resources/rus_letter_frequency.txt', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        pair = line.split()
        rus_frequencies[pair[0]] = float(pair[1])


def get_text(file_name: Path) -> str:
    """Считывает из файла шифротекст"""
    with open(file_name, encoding='utf-8') as file:
        return file.read()


def count_letter_frequencies(text: str) -> dict:
    """Вычисляет частоты букв в шифротексте"""
    frequencies = {}
    for letter in text:
        frequencies[letter.lower()] = text.count(letter)
    sorted_frequencies = sorted(frequencies.items(), key=lambda x: -x[1])
    return dict(sorted_frequencies)


def count_bigrams(text: str) -> dict:
    """Вычисляет частоты биграмм в шифротексте"""
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    bigrams_counts = collections.Counter(bigrams)
    sorted_bigrams = sorted(bigrams_counts.items(), key=lambda x: -x[1])
    return dict(sorted_bigrams)


def count_trigrams(text: str) -> dict:
    """Вычисляет частоты триграмм в шифротексте"""
    trigrams = [text[i:i + 3] for i in range(len(text) - 2)]
    trigrams_counts = collections.Counter(trigrams)
    sorted_trigrams = sorted(trigrams_counts.items(), key=lambda x: -x[1])
    return dict(sorted_trigrams)


def write_statistics(letter_fr: dict, bigrams: dict, trigrams: dict) -> None:
    """Выводит вычисленные частоты в файл statistics_1.txt"""
    with open('statistics_2.txt', mode='w', encoding='utf-8') as file:
        file.write('Частоты букв в шифротексте:\n')
        for key, value in letter_fr.items():
            file.write(f'{key} {value}\n')
        file.write('\nЧастоты биграмм в шифротексте:\n')
        for key, value in bigrams.items():
            file.write(f'{key} {value}\n')
        file.write('\nЧастоты триграмм в шифротексте:\n')
        for key, value in trigrams.items():
            file.write(f'{key} {value}\n')


def frequency_analysis(letter_fr: list, bigrams: list, trigrams: list, text: str):
    vowels.clear()
    consonants.clear()
    max_freq_letter = letter_fr[0][0]
    vowels.append(max_freq_letter)
    used_bigrams = del_rare_bi_or_trigrams(bigrams)
    for el in used_bigrams:
        if max_freq_letter in el[0]:
            # print(el)
            b = el[0]
            if b[0] == max_freq_letter and b[1] not in consonants:
                consonants.append(b[1])
            elif b[1] == max_freq_letter and b[0] not in consonants:
                consonants.append(b[0])
    sort_by_usage(consonants, letter_fr)
    complement_vowels(used_bigrams, letter_fr)
    complement_consonants(used_bigrams, letter_fr)

    print(f'Гласные буквы: {vowels}')
    print(f'Согласные буквы: {consonants}')
    # print(try_decode(text))


def del_rare_bi_or_trigrams(bt_grams: list) -> list:
    """Удаляет из списка биграмм/триграмм редко встречающиеся биграммы/триграммы"""
    used_bt_grams = []
    for el in bt_grams:
        if el[1] != 1:
            used_bt_grams.append(el)
    return used_bt_grams


def complement_vowels(bgrms: list, l_fr: list) -> None:
    """Дополняет список гласных букв на основе списка известных согласных букв"""
    for letter in consonants:
        for el in bgrms:
            if letter in el[0]:
                # print(el)
                b = el[0]
                if b[0] == letter and b[1] not in vowels and b[1] not in consonants:
                    vowels.append(b[1])
                elif b[1] == letter and b[0] not in vowels and b[0] not in consonants:
                    vowels.append(b[0])
    sort_by_usage(vowels, l_fr)


def complement_consonants(bgrms: list, l_fr: list):
    """Дополняет список согласных букв на основе списка известных гласных букв"""
    for letter in vowels:
        for el in bgrms:
            if letter in el[0]:
                b = el[0]
                if b[0] == letter and b[1] not in consonants and b[1] not in vowels:
                    consonants.append(b[1])
                elif b[1] == letter and b[0] not in consonants and b[0] not in vowels:
                    consonants.append(b[0])
    sort_by_usage(consonants, l_fr)


def sort_by_usage(letters: list, l_fr: list):
    """Сортирует список букв по убыванию их частоты в шифротексте"""
    fr = []
    for l in letters:
        for el in l_fr:
            if el[0] == l:
                fr.append(el[1])
    for i in range(len(fr) - 1):
        for j in range(len(fr) - i - 1):
            for i in range(len(letters) - 1):
                for j in range(len(letters) - i - 1):
                    if fr[j] < fr[j + 1]:
                        letters[j], letters[j + 1] = letters[j + 1], letters[j]
                        fr[j], fr[j + 1] = fr[j + 1], fr[j]


def try_decode(text: str) -> str:
    """Расшифровывает, но очень плохо"""
    res = []
    for l in text:
        if l in vowels:
            id = vowels.index(l)
            res.append(rus_vowels[id])
        elif l in consonants:
            id = consonants.index(l)
            res.append(rus_consonants[id])
        else:
            res.append('-')
    return ''.join(res)


def chosen_plaintext_attack(text: str, known_word: str):
    folder_for_results = "results/"
    solve_by_known_word(text, known_word.lower(), folder_for_results)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Имя файла с зашифрованным текстом', type=str)
    return parser.parse_args()


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


def print_help():
    print("Доступные команды:\n "
          "анализ - для проведения частотного анализа текста\n "
          "печать - для вывода возможной расшифровки с перебором по словарю\n "
          "словарь - для вывода введенных пользователем пар букв\n "
          "расшифровка - для вывода расшифровки с применением указанных пар букв\n "
          "перестановки - для подбора перестановок с учётом введенных пользователем пар букв\n "
          "выход - для завершения программы")
    print("Введите команду или пару букв 'шифр расшифровка'")


def by_hands_processing(cipher_text):
    key_dictionary = {}
    folder_for_results = "results/"
    print_help()
    while True:
        command = input("Введите команду: ")
        if command == "печать":
            if len(key_dictionary) > 1:
                print(cipher_text)
                solve_by_partial_key(cipher_text, key_dictionary, folder_for_results)
                # print("Введите слово: ")
                # word = input()
                # count = 0
                # for i in range(len(word) - 1):
                #     if word[i] not in rus_vowels and word[i] not in rus_consonants:
                #         count += 1
                # if count != 0:
                #     print("Слово должно состоять из букв русского алфавита")
                # else:
                #     solve_by_known_word(cipher_text, word.lower(), folder_for_results)
            else:
                print("Выводить в печать нечего")
                continue
        elif command == "расшифровка":
            print(cipher_text)
            print(decode_by_key_dictionary(cipher_text, key_dictionary))
        elif command == "словарь":
            print(key_dictionary)
        elif command == "анализ":
            letter_frequencies = count_letter_frequencies(cipher_text)
            bigrams = count_bigrams(cipher_text)
            trigrams = count_trigrams(cipher_text)
            frequency_analysis(list(letter_frequencies.items()), list(bigrams.items()), list(trigrams.items()),
                               cipher_text)
        elif command == "перестановки":
            letter_frequencies = count_letter_frequencies(cipher_text)
            bigrams = count_bigrams(cipher_text)
            trigrams = count_trigrams(cipher_text)
            frequency_analysis(list(letter_frequencies.items()), list(bigrams.items()), list(trigrams.items()),
                               cipher_text)
            deciphers = permutations.try_permutations(cipher_text, vowels, consonants, key_dictionary)

            with open('results/deciphers.txt', 'w', encoding='utf-8') as f:
                for i in deciphers:
                    f.write(i)
                    f.write('\n')

            pos = 0
            step = 10
            for key, val in enumerate(deciphers):
                print(val)
                pos += 1
                if pos % step == 0:
                    comm = input("Нажмите enter, чтобы продолжить вывод, любую команду чтобы прервать: ")
                    if len(comm) != 0:
                        break
            print_help()
        elif command == "выход":
            return
        elif len(command) == 3:
            # принята пара букв через пробел, запоминаем
            try:
                key, value = command.split(' ')
                key_dictionary[key] = value
            except:
                print("Команда не распознана")
        elif len(command) == 1 and command in LETTERS:
            # убираем букву из словаря соответствий
            if command in key_dictionary.keys():
                key_dictionary.pop(command)
        else:
            print("Команда не распознана")


if __name__ == '__main__':
    args = parse_args()
    # aa = "text_2"
    # file_name = Path.cwd() / 'resources' / ('%s.txt' % aa)

    file_name = Path.cwd() / 'resources' / ('%s.txt' % args.file)
    if not file_name.exists() or not file_name.is_file():
        print("Файл не найден", file=sys.stderr)
        sys.exit(1)
    else:
        cipher_text = get_text(file_name)
        letter_frequencies = count_letter_frequencies(cipher_text)
        bigrams = count_bigrams(cipher_text)
        trigrams = count_trigrams(cipher_text)
        write_statistics(letter_frequencies, bigrams, trigrams)
        print(f"Файл {file_name} успешно считан.")
        print(f"Выберите действие:\n"
              f"1 - Ввести наиболее вероятное слово\n"
              f"2 - Выполнить частотный анализ\n"
              f"3 - Выполнить ручной подбор\n"
              f"4 - Завершить программу")
        running = True
        while running:
            try:
                answer = int(input())
            except ValueError:
                print(f"Кажется, это не число")
                continue
            if answer == 1:
                print("Введите слово: ")
                word = input()
                count = 0
                for i in range(len(word) - 1):
                    if word[i] not in rus_vowels and word[i] not in rus_consonants:
                        count += 1
                if count != 0:
                    print("Слово должно состоять из букв русского алфавита")
                    exit()
                else:
                    chosen_plaintext_attack(cipher_text, word)
                    exit()
            elif answer == 2:
                frequency_analysis(list(letter_frequencies.items()), list(bigrams.items()), list(trigrams.items()),
                                   cipher_text)
                exit()
            elif answer == 3:
                by_hands_processing(cipher_text)
                exit()
            elif answer == 4:
                exit()
            else:
                print("Такой команды я не знаю")
