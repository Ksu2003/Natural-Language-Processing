#!/usr/bin/env python3

import re
import os
from collections import Counter
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import spacy

# Загрузка моделей
nlp_ru = spacy.load('ru_core_news_sm')
nlp_it = spacy.load('it_core_news_sm')
nlp_en = spacy.load('en_core_web_sm')
nlp_en.max_length = 6000000
nlp_it.max_length = 1502128 
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('averaged_perceptron_tagger_ru')
nltk.download('punkt')

def load_texts(file_paths):
    texts = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                texts.append(file.read())
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
    return ' '.join(texts)

def preprocess_text(text):
    text = re.sub(r"[^a-zA-Zа-яА-ЯёЁàèéìòùÀÈÉÌÒÙ'\- ]+", ' ', text)
    text = text.replace("--", '')
    text = text.replace(" - ", '')
    text = text.replace(" -- ", '')
    text = text.replace(" -", '')
    text = text.replace("- ", '')
    text = text.replace(" '' ", '')
    text = text.replace(" ' ", '')
    text = text.replace(" '", '')
    text = text.replace("' ", '')
    
    
    return text.lower()

def annotate_text(text, language):
    if language == 'russian':
        doc = nlp_ru(text)
        annotated = [f"{token.text}/{token.pos_}" for token in doc]
    elif language == 'italian':
        doc = nlp_it(text)
        annotated = [f"{token.text}/{token.pos_}" for token in doc]
    else:  # english by default
        doc = nlp_en(text)
        annotated = [f"{token.text}/{token.pos_}" for token in doc]

    return ' '.join(annotated)  # Возвращаем в виде строки

def lemmatize_annotated_text(annotated_text, language):
    lemmatized_words = []
    for token_tag in annotated_text.split():
        word, tag = token_tag.rsplit('/', 1)  # Разделяем слово и тег
        if language == 'russian':
            lemma = nlp_ru(word)
        elif language == 'english':
            lemma = nlp_en(word)
        elif language == 'italian':
            lemma = nlp_it(word)

        # Проверка, был ли создан токен, если нет, используем оригинальное слово
        if lemma and len(lemma) > 0:
            lemmatized_words.append(f"{lemma[0].lemma_}/{tag}")  # Используем лемму из первого токена
        else:
            lemmatized_words.append(f"{word}/{tag}")  # Используем оригинальное слово, если лемма не найдена

    return ' '.join(lemmatized_words)

def save_annotated_lemmatized_text(lemmatized_text, language):
    with open(f'{language}21.txt', 'w', encoding='utf-8') as file:
        file.write(lemmatized_text)

def annotate_and_lemmatize(file_paths, language):
    text = load_texts(file_paths)

    # Предобработка текста
    preprocessed_text = preprocess_text(text)

    # Аннотирование текста
    annotated_text = annotate_text(preprocessed_text, language)

    # Лемматизация аннотированного текста
    lemmatized_annotated_text = lemmatize_annotated_text(annotated_text, language)

    # Сохранение лемматизированного текста с аннотациями
    save_annotated_lemmatized_text(lemmatized_annotated_text, language)

    print("Аннотирование и лемматизация завершены.")

# Пример использования
if __name__ == '__main__':
    # Укажите пути к файлам, которые вы хотите загрузить
    file_paths = ['italian2.txt']  # Замените на свои пути
    language = 'italian'  # Укажите язык: 'russian', 'english', 'italian'
    annotate_and_lemmatize(file_paths, language)