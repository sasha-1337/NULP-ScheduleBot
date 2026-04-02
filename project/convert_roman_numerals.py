import re


def roman_to_int(roman_numeral):
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    int_value = 0
    prev_value = 0

    for char in reversed(roman_numeral):
        value = roman_values[char]
        int_value = int_value + value if value >= prev_value else int_value - value
        prev_value = value

    return int_value


def find_arabic_numerals(text):
    pattern = r'\b[IVXLCDM]+\b'
    roman_numerals = re.findall(pattern, text)
    arabic_numerals = [roman_to_int(num) for num in roman_numerals]
    return arabic_numerals


# print(find_arabic_numerals("Вільховченко Н.П., XX VII н.к., Практична"))
