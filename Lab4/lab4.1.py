import re
import string
from collections import defaultdict

def generate_trigrams(word):
    padded = f'_{word}_'
    trigrams = [padded[i:i + 3] for i in range(len(padded) - 2)]
    return trigrams

def process_file(file_path):
    trigram_freq = defaultdict(int)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r"[^a-zA-Z'\- ]+", ' ', text)
        words = text.split()
        
        for word in words:
            trigrams = generate_trigrams(word)
            for trigram in trigrams:
                trigram_freq[trigram] += 1
                
    return trigram_freq

def all_possible_trigrams():
    alphabet = string.ascii_lowercase
    possible_trigrams = set()
    
    for first in ['_'] + list(alphabet):  # Первое положение
        for second in alphabet:            # Второе положение
            for third in ['_'] + list(alphabet):  # Третье положение
                possible_trigrams.add(first + second + third)
    
    return possible_trigrams

def identify_invalid_trigrams(trigram_freq):
    
    valid_trigrams = set(trigram_freq.keys())
    all_trigrams = all_possible_trigrams()
    
    
    invalid_trigrams = all_trigrams - valid_trigrams
#   for trigram, freq in trigram_freq.items():
#       if freq < 100:
#           invalid_trigrams.add(trigram) #  
            # Сортируем триграммы по их частоте
    sorted_trigrams = sorted(trigram_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Вычисляем порог для 95% от общей частоты
    total_count = sum(freq for _, freq in sorted_trigrams)
    threshold_count = total_count * 0.93
    cumulative_count = 0
    
    
    for trigram, freq in sorted_trigrams:
        cumulative_count += freq
        if cumulative_count > threshold_count:
            invalid_trigrams.add(trigram)

    return invalid_trigrams

def save_trigram_frequencies(trigram_freq, output_file):
    """Сохранение частот триграмм в файл."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for trigram, freq in sorted(trigram_freq.items(), key=lambda x: x[1], reverse=True):
            file.write(f'{trigram}: {freq}\n')
            
def save_invalid_trigrams(invalid_trigrams, output_file):
    """Сохранение недопустимых триграммов в файл."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for trigram in sorted(invalid_trigrams):
            file.write(f'{trigram}\n')

def verify_text(text, valid_trigrams, invalid_trigrams, trigram_freq):
    """Верификация текста с использованием триграмм."""
    text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r"[^a-zA-Z'\- ]+", ' ', text)
    
    words = text.split()
    results = []
    
    for word in words:
        trigrams = list(generate_trigrams(word))  # Генерируем триграммы для слова
        #print(f'Слово: {word}, Триграммы: {trigrams}')  # Распечатка триграмм для текущего слова
        
        # Проверка на наличие двух ошибочных триграмм подряд
        found_error = False
        
        # Проходим по триграммам и ищем два подряд стоящих недопустимых
        for i in range(len(trigrams) - 1):
            if trigrams[i] in invalid_trigrams and trigrams[i + 1] in invalid_trigrams:
#               print(trigrams[i], trigrams[i+1])
#               print(" ")
                found_error = True
                break
            
        # Если найдена подряд стоящая пара ошибочных триграмм, слово считается неверным
        if found_error:
            results.append((word, 'неверное'))
        else:
            results.append((word, 'верное'))
            
    return results

def save_verification_results(results, output_file):
    """Сохранение результатов верификации в файл."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, status in results:
            file.write(f'{word}: {status}\n')
            
def calculate_metrics(A, B, C):
    """Расчет точности и полноты."""
    precision = A / ((A) + (B)) if (A + (B)) > 0 else 0
    recall = (A) / ((A) + (C)) if ((A) + (C)) > 0 else 0
    return precision, recall
def compare_with_correct_text(verification_results, correct_text_file):
    """Сравнение результатов верификации с текстом из другого файла."""
    with open(correct_text_file, 'r', encoding='utf-8') as file:
        correct_text = file.read().lower()
        correct_words = set(re.sub(r'[^\w\s]', '', correct_text).split())  # Удаляем знаки препинания и делим на слова
        
    detailed_results = []
    for word, status in verification_results:
        if word.lower() in correct_words:
            detailed_results.append((word, status, 'верно в тексте'))
        else:
            detailed_results.append((word, status, 'неверно в тексте'))
            
    return detailed_results

def save_detailed_verification_results(results, output_file):
    """Сохранение подробных результатов верификации в файл."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, status, detail in results:
            file.write(f'{word}: {status}, {detail}\n')
def count_statuses_in_results(results_file):
    """Подсчет количества строк с определенными статусами в файле результатов проверки."""
    A = B = C = 0
    
    with open(results_file, 'r', encoding='utf-8') as file:
        for line in file:
            if 'неверное' in line and 'неверно в тексте' in line:
                A += 1
            elif 'верное' in line and 'неверно в тексте' in line:
                C += 1
            elif 'неверное' in line and 'верно в тексте' in line:
                B += 1
                
    return A, B, C

if __name__ == '__main__':
    input_file_path = 'english copy.txt'  #  путь к вашему текстовому файлу
    output_freq_file = 'trigram_frequencies2.txt'
    output_invalid_file = 'invalid_trigrams2.txt'  # Файл для недопустимых триграмм
    output_verification_file = 'verification_results2.txt'  # Файл для результатов проверки
    correct_text_file = 'Correct_text.txt'  # путь к файлу с корректным текстом
    
    
    trigram_freq = process_file(input_file_path)
    save_trigram_frequencies(trigram_freq, output_freq_file)
    
    
    valid_trigrams = set(trigram_freq.keys())
    invalid_trigrams = identify_invalid_trigrams(trigram_freq)
    
    # Сохранение недопустимых триграммов в файл
    save_invalid_trigrams(invalid_trigrams, output_invalid_file)
    
    
    text_to_verify_path = 'text_to_verify.txt'  
    with open(text_to_verify_path, 'r', encoding='utf-8') as file:
        input_text = file.read()  # Читаем текст из файла
        
    verification_results = verify_text(input_text, valid_trigrams, invalid_trigrams, trigram_freq)
    
    
    save_verification_results(verification_results, output_verification_file)
    
    
    detailed_results = compare_with_correct_text(verification_results, correct_text_file)
    
    
    save_detailed_verification_results(detailed_results, output_verification_file)
    
    
    A, B, C = count_statuses_in_results(output_verification_file)
    
    
    print(f'Количество "неверное, неверно в тексте": {A}')
    print(f'Количество "верное, неверно в тексте": {C}')
    print(f'Количество "неверное, верно в тексте": {B}')
    
    detected_errors = [word for word, status in verification_results if status == 'неверное']
    precision, recall = calculate_metrics(A, B, C)
    print(f'Precision: {precision:.2f}, Recall: {recall:.2f}')  # Вывод метрик