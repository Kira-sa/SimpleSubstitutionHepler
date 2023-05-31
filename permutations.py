import itertools


rus_vowels = ['о', 'е', 'а', 'и', 'у', 'я', 'ы', 'ю', 'э']
rus_consonants = ['н', 'т', 'с', 'р', 'в', 'л', 'к', 'м', 'д', 'п', 'з', 'ь', 'б', 'г', 'ч', 'й', 'х', 'ж', 'ш', 'ц',
                  'щ', 'ф']


def main(vowels, consonants):
    # построить перестановки vowels
    vowels_count = min(len(vowels), len(rus_vowels))
    possible_vowels = rus_vowels[:vowels_count]
    possible_vowels_perm = list(itertools.permutations(possible_vowels))

    # построить перестановки consonants
    consonants_count = min(len(consonants), len(rus_consonants))
    possible_consonants = rus_consonants[:consonants_count]
    possible_consonants_perm = list(itertools.permutations(possible_consonants))

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


if __name__ == "__main__":
    vowels = ['з', 'и', 'э', 'д']
    consonants = ['г', 'с', 'л', 'т', 'п', 'у', 'м', 'ф']
    result_key = main(vowels, consonants)
    a = 23