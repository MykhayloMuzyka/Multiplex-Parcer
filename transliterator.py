letters = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'h',
    'д': 'd',
    'е': 'e',
    'є': 'ye',
    'ж': 'zh',
    'з': 'z',
    'и': 'y',
    'і': 'i',
    'ї': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ь': '',
    'ю': 'yu',
    'я': 'ya',
    ' ': '_'
}

eng_alphabet = 'abcdefghijklmnopqrstuvwxyz'


def transliterate(ukr):
    ukr = ukr.lower()
    eng = ''
    for letter in ukr:
        if letter not in eng_alphabet:
            eng += letters[letter]
        else:
            eng += letter
    return eng
