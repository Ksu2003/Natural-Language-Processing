import numpy as np
import scipy as sp

print(np.__version__)
print(sp.__version__)
import re
import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Scrollbar, filedialog
from collections import Counter
import os

# Функции для работы с текстами и частотными словарями
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

def create_frequency_dictionary(text):
    words = text.split()
    frequency = Counter(words)
    return frequency

def save_frequency_dictionary(frequency_dict, language):
    with open(f'{language}_frequency.txt', 'w', encoding='utf-8') as file:
        for word, count in frequency_dict.items():
            file.write(f'{word}\t{count}\n')

# Класс UI приложения
class WordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Частотный Словарь")
        
        self.language = None
        self.frequency_dict = {}
        
        # Меню выбора языка
        self.language_menu = tk.Menu(self.root)
        self.root.config(menu=self.language_menu)
#       self.sorted_menu = tk.Menu(self.root)
#       self.root.config(menu=self.sorted_menu)
        
        
        self.language_submenu = tk.Menu(self.language_menu, tearoff=0)
        self.language_menu.add_cascade(label="Выбор языка", menu=self.language_submenu)
        self.language_submenu.add_command(label="Русский", command=lambda: self.load_language('russian'))
        self.language_submenu.add_command(label="Английский", command=lambda: self.load_language('english'))
        self.language_submenu.add_command(label="Итальянский", command=lambda: self.load_language('italian'))
        
#       self.sorted_menu = tk.Menu(self.sort, tearoff=0)
#       self.sorted_menu.add_cascade(label="Сортировка", menu=self.language_submenu)
#       self.sorted_submenu.add_command(label="По алфавиту", command=lambda: self.sort())
#       self.sorted_submenu.add_command(label="По убыванию частоты", command=lambda: self.sort())
#       self.sorted_submenu.add_command(label="По возрастанию частоты", command=lambda: self.sort())
#       
        self.sort_menu = tk.Menu(self.language_menu, tearoff=0)
        self.language_menu.add_cascade(label="Сортировка", menu=self.sort_menu)
        self.sort_menu.add_command(label="По алфавиту", command=self.sort_alphabetically)
        self.sort_menu.add_command(label="По убыванию частоты", command=self.sort_by_frequency_desc)
        self.sort_menu.add_command(label="По возрастанию частоты", command=self.sort_by_frequency_asc)
        self.sort_menu.add_command(label="В обратном алфавитном порядке", command=self.sort_reverse_alphabetically)
        # Кнопки функционала
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        tk.Button(self.btn_frame, text="Показать словарь", command=self.show_dictionary).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Поиск слова", command=self.search_word).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Добавить слово", command=self.add_word).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Удалить слово", command=self.delete_word).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Исправить слово", command=self.correct_word).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Загрузить тексты из папки", command=self.load_texts_from_folder).pack(side=tk.LEFT)
        

        # Список для отображения словаря
        
        self.listbox = Listbox(self.root, width=90, height=20)
        self.listbox.pack(pady=10)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
    
    def sort_alphabetically(self):
            self.listbox.delete(0, tk.END)
            for word, count in sorted(self.frequency_dict.items(), key=lambda x: x[0]):  # Сортировка по алфавиту
                self.listbox.insert(tk.END, f"{word}: {count}")
        
    def sort_by_frequency_desc(self):
        self.listbox.delete(0, tk.END)
        for word, count in sorted(self.frequency_dict.items(), key=lambda x: x[1], reverse=True):  # По убыванию частоты
            self.listbox.insert(tk.END, f"{word}: {count}")
            
    def sort_by_frequency_asc(self):
        self.listbox.delete(0, tk.END)
        for word, count in sorted(self.frequency_dict.items(), key=lambda x: x[1]):  # По возрастанию частоты
            self.listbox.insert(tk.END, f"{word}: {count}")
            
    def load_language(self, lang):
        self.language = lang
        self.frequency_dict = self.load_frequency_dictionary(lang)
        messagebox.showinfo("Информация", f"{lang.capitalize()} словарь загружен.")

    def load_frequency_dictionary(self, language):
        frequency_dict = {}
        try:
            with open(f'{language}_frequency.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    word, count = line.strip().split('\t')
                    frequency_dict[word] = int(count)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Частотный словарь не найден.")
        return frequency_dict

    def show_dictionary(self):
        self.listbox.delete(0, tk.END)
        for word, count in sorted(self.frequency_dict.items(), key=lambda x: x[0]):  # Сортировка по алфавиту
            self.listbox.insert(tk.END, f"{word}: {count}")

    def search_word(self):
        pattern = simpledialog.askstring("Поиск слова", "Введите начало слова:")
        if pattern:
            self.listbox.delete(0, tk.END)
            # Собираем слова, которые соответствуют паттерну
            matching_words = [(word, count) for word, count in self.frequency_dict.items() if word.startswith(pattern)]
            
            # Сортируем результаты
            sort_option = simpledialog.askstring("Сортировка", "Введите 'a' для алфавита, 'd' для убывания частоты, 'i' для возрастания частоты, 'r' для обратного алфавита:")
            
            if sort_option == 'a':
                # Сортировка по алфавиту
                matching_words.sort(key=lambda x: x[0])
            elif sort_option == 'd':
                # Сортировка по убыванию частоты
                matching_words.sort(key=lambda x: x[1], reverse=True)
            elif sort_option == 'i':
                # Сортировка по возрастанию частоты
                matching_words.sort(key=lambda x: x[1])
            elif sort_option == 'r':
                # Сортировка по обратному алфавиту
                matching_words.sort(key=lambda x: x[0], reverse=True)
                
            # Выводим найденные слова в Listbox
            for word, count in matching_words:
                self.listbox.insert(tk.END, f"{word}: {count}")
                
    def sort_reverse_alphabetically(self):
        self.listbox.delete(0, tk.END)
        for word, count in sorted(self.frequency_dict.items(), key=lambda x: x[0], reverse=True):  # Сортировка по обратному алфавиту
            self.listbox.insert(tk.END, f"{word}: {count}")
            
    def add_word(self):
        new_word = simpledialog.askstring("Добавить слово", "Введите новое слово:")
        if new_word and new_word not in self.frequency_dict:
            self.frequency_dict[new_word] = 0
            messagebox.showinfo("Информация", f"Слово '{new_word}' добавлено.")
        else:
            messagebox.showinfo("Информация", f"Слово '{new_word}' уже в словаре.")
        
        self.save_dictionary()  # Сохранить изменения

    def delete_word(self):
        word_to_delete = simpledialog.askstring("Удалить слово", "Введите слово для удаления:")
        if word_to_delete in self.frequency_dict:
            confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить '{word_to_delete}'?")
            if confirm:
                del self.frequency_dict[word_to_delete]
                messagebox.showinfo("Информация", f"Слово '{word_to_delete}' удалено.")
                self.save_dictionary()  # Сохранить изменения
        else:
            messagebox.showinfo("Информация", f"Слово '{word_to_delete}' не найдено.")
#   def correct_word(self):
#       old_word = simpledialog.askstring("Исправить слово", "Введите слово для исправления:")
#       if old_word in self.frequency_dict:
#           new_word = simpledialog.askstring("Исправление слова", "Введите правильное написание:")
#           if new_word not in self.frequency_dict and self.frequency_dict[old_word] == 0:
#               #self.frequency_dict[new_word] += self.frequency_dict[old_word]
#               self.frequency_dict[old_word] == 1
#           if new_word and self.frequency_dict[old_word] == 0:
#               self.frequency_dict[new_word] += self.frequency_dict[old_word]
#                 # Суммируем частоты
#           
#           del self.frequency_dict[old_word]  # Удаляем старое слово
#           messagebox.showinfo("Информация", f"Слово '{old_word}' исправлено на '{new_word}'.")
#       else:
#           messagebox.showwarning("Ошибка", f"Слово '{old_word}' не найдено.")
    def correct_word(self):
        word_to_correct = simpledialog.askstring("Исправить слово", "Введите слово для исправления:")
        if not word_to_correct:
            return  # Если пользователь ничего не ввел, завершаем выполнение функции
        if word_to_correct not in self.frequency_dict:
            messagebox.showinfo("Информация", f"Слово '{word_to_correct}' отсутствует.")
            return 
        corrected_word = simpledialog.askstring("Исправить слово", "Введите исправленный вариант:")
        if not corrected_word:
            return  # Если пользователь ничего не ввел, завершаем выполнение функции
        
        # Обновляем частоту
        if corrected_word in self.frequency_dict:
            self.frequency_dict[corrected_word] += (self.frequency_dict[word_to_correct] + (1 if self.frequency_dict[word_to_correct] == 0 else 0))
        else:
            self.frequency_dict[corrected_word] = self.frequency_dict[word_to_correct]   # Новое слово, частота 1
            
        if word_to_correct in self.frequency_dict:
            del self.frequency_dict[word_to_correct]  # Удаляем старое слово из словаря
            
        # Обновляем текстовые файлы
        self.update_text_files(" "+ word_to_correct +" ", " "+corrected_word +" ")
        
        messagebox.showinfo("Информация", f"Слово '{word_to_correct}' исправлено на '{corrected_word}'.")
        
        self.save_dictionary()  # Сохраняем изменения
        
    def update_text_files(self, old_word, new_word):
        # Запрашиваем конкретный текстовый файл для обновления
        file_path = filedialog.askopenfilename(title="Выберите текстовый файл", filetypes=[("Текстовые файлы", "*.txt")])
        
        if not file_path:
            return  # Если пользователь ничего не выбрал, завершаем выполнение функции
        
        try:
            # Читаем содержимое файла
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Заменяем старое слово на новое
            updated_content = content.replace(old_word, new_word)
            
            # Сохраняем обновлённое содержимое назад в файл
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
                
            messagebox.showinfo("Информация", f"Слово '{old_word}' было заменено на '{new_word}' в файле '{file_path}'.")
            
        except Exception as e:
            print(f"Ошибка при обновлении файла {file_path}: {e}")
            messagebox.showerror("Ошибка", f"Не удалось обновить файл {file_path}.")
    def load_texts_from_folder(self):
        # Запрашиваем конкретный текстовый файл для загрузки
        file_path = filedialog.askopenfilename(title="Выберите текстовый файл", filetypes=[("Текстовые файлы", "*.txt")])
        
        if not file_path:
            return  # Если пользователь ничего не выбрал, завершаем выполнение функции
        
        try:
            # Читаем содержимое файла
            with open(file_path, 'r', encoding='utf-8') as file:
                all_texts = file.read()
                
            if self.language == 'russian':
                all_texts = re.sub(r'[^а-яА-ЯёЁ\s-]+', '', all_texts)
                
            preprocessed_text = preprocess_text(all_texts)
            new_frequency_dict = create_frequency_dictionary(preprocessed_text)
            
            # Объединяем старый и новый словари
            for word, count in new_frequency_dict.items():
                if word in self.frequency_dict:
                    self.frequency_dict[word] += count
                else:
                    self.frequency_dict[word] = count
                    
            self.save_dictionary()  # Сохраняем обновленный словарь
            messagebox.showinfo("Информация", f"Тексты из файла '{file_path}' загружены и обработаны.")
            
        except Exception as e:
            print(f"Ошибка при загрузке файла {file_path}: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл {file_path}.")
                
    def save_dictionary(self):
        save_frequency_dictionary(self.frequency_dict, self.language)
def main():
    # Путь к вашим текстовым файлам
    russian_file = 'russian.txt'
    english_file = 'english.txt'
    italian_file = 'italian.txt' 
    
    # Загрузка и обработка текстов
    russian_text = load_texts([russian_file])
    english_text = load_texts([english_file])
    italian_text = load_texts([italian_file])
    
    # Предобработка текста
    if(russian_text):
        russian_text = re.sub(r'[^а-яА-ЯёЁ\s-]+', '', russian_text)
        russian_text = preprocess_text(russian_text)
        
    english_text = preprocess_text(english_text)
    italian_text = preprocess_text(italian_text)
    
    # Создание частотных словарей
    russian_frequency = create_frequency_dictionary(russian_text)
    english_frequency = create_frequency_dictionary(english_text)
    italian_frequency = create_frequency_dictionary(italian_text)
    
    # Сохранение частотных словарей в файлы
    save_frequency_dictionary(russian_frequency, 'russian')
    save_frequency_dictionary(english_frequency, 'english')
    save_frequency_dictionary(italian_frequency, 'italian')
    
# Основной блок приложения
if __name__ == '__main__':
    main()
    root = tk.Tk()
    app = WordApp(root)
    root.mainloop()