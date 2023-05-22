# dictionary_2 - отсортированный словарь без Ё
# dictionary_1 - отсортированный словарь слова с ё в конце

import collections

rus_frequencies = {}


def get_rus_frequencies() -> None:
    """Считывает из файла частоты для букв русского языка"""
    with open('resources/rus_letter_frequency.txt', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        pair = line.split()
        rus_frequencies[pair[0].lower()] = float(pair[1])


def get_text() -> str:
    """Считывает из файла шифротекст"""
    with open('resources/text.txt', encoding='utf-8') as file:
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
    with open('statistics.txt', mode='w', encoding='utf-8') as file:
        file.write('Частоты букв в шифротексте:\n')
        for key, value in letter_fr.items():
            file.write(f'{key} {value}\n')
        file.write('\nЧастоты биграмм в шифротексте:\n')
        for key, value in bigrams.items():
            file.write(f'{key} {value}\n')
        file.write('\nЧастоты триграмм в шифротексте:\n')
        for key, value in trigrams.items():
            file.write(f'{key} {value}\n')


def magic():
    worknown_word = ''
    pass



if __name__ == '__main__':
    cipher_text = get_text()
    letter_frequencies = count_letter_frequencies(cipher_text)
    bigrams = count_bigrams(cipher_text)
    trigrams = count_trigrams(cipher_text)
    write_statistics(letter_frequencies, bigrams, trigrams)
    magic()
