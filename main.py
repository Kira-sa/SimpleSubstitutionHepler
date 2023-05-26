# dictionary_2 - отсортированный словарь без Ё
# dictionary_1 - отсортированный словарь слова с ё в конце

import collections
import argparse
from pathlib import Path
import sys

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
    """Выводит вычисленные частоты в файл statistics.txt"""
    with open('statistics_3.txt', mode='w', encoding='utf-8') as file:
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
    print(f"Частотный анализ выполняется")
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
    print(try_decode(text))

def del_rare_bi_or_trigrams(bt_grams: list) -> list:
    """Удаляет из списка биграмм/триграмм редко встречающиеся биграммы/триграммы"""
    used_bt_grams = []
    for el in bt_grams:
        if el[1] != 1:
            used_bt_grams.append(el)
    return used_bt_grams


def complement_vowels(bgrms: list, l_fr: list):
    """Дополняет список гласных букв на основе списка известных согласных букв"""
    for letter in consonants:
        for el in bgrms:
            if letter in el[0]:
                # print(el)
                b = el[0]
                if b[0] == letter and b[1] not in vowels:
                    vowels.append(b[1])
                elif b[1] == letter and b[0] not in vowels:
                    vowels.append(b[0])
    sort_by_usage(vowels, l_fr)


def complement_consonants(bgrms: list, l_fr: list):
    """Дополняет список согласных букв на основе списка известных гласных букв"""
    for letter in vowels:
        for el in bgrms:
            if letter in el[0]:
                b = el[0]
                if b[0] == letter and b[1] not in consonants:
                    consonants.append(b[1])
                elif b[1] == letter and b[0] not in consonants:
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


def chosen_plaintext_attack(word: str):
    print(f"В тексте есть слово {word}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Имя файла с зашифрованным текстом', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    file_name = Path.cwd() / 'resources' / ('%d.txt' % args.file)
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
              f"1 - Выполнить частотный анализ\n"
              f"2 - Ввести наиболее вероятное слово\n"
              f"3 - Завершить программу\n")
        running = True
        while running:
            try:
                answer = int(input())
            except ValueError:
                print(f"Кажется, это не число\n")
                exit()
            if answer == 1:
                frequency_analysis(list(letter_frequencies.items()), list(bigrams.items()), list(trigrams.items()),
                                   cipher_text)
                exit()
            elif answer == 2:
                print("Введите слово: ")
                word = input().lower()
                chosen_plaintext_attack(word)
                exit()
            elif answer == 3:
                exit()
            else:
                print("Такой команды я не знаю")
