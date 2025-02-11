#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from collections import Counter
import os


STOP_WORDS = {
    'en': {"the", "and", "is", "in", "to", "it", "of", "that", "with", "as", "for", "on", "was", "at", "by", "an"},
    'ru': {"и", "в", "на", "с", "по", "о", "из", "а", "это", "к", "от", "у", "за", "то", "как", "же", "но", "они"}
}



UNINFORMATIVE_TAGS = {"DET", "AUX", "SCONJ", "CCONJ", "ADP", "PRON", "ADV", "SPACE", "PUNCT", "PART"}
class SearchEngineApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Простейшая поисковая система")

        self.language_var = tk.StringVar(value='en')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Выберите язык:").pack()
        self.en_button = tk.Button(self.master, text="English", command=lambda: self.set_language('en'))
        self.en_button.pack(pady=5)
        self.ru_button = tk.Button(self.master, text="Русский", command=lambda: self.set_language('ru'))
        self.ru_button.pack(pady=5)
        self.ru_button = tk.Button(self.master, text="Italian", command=lambda: self.set_language('it'))
        self.ru_button.pack(pady=5)
        
        self.load_button = tk.Button(self.master, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(pady=5)

        self.process_button = tk.Button(self.master, text="Обработать документ", command=self.process_document)
        self.process_button.pack(pady=5)

        self.sort_freq_button = tk.Button(self.master, text="Сортировать по частоте", command=lambda: self.display_results(sorted_by="frequency"))
        self.sort_freq_button.pack(pady=5)

        self.query_label = tk.Label(self.master, text="Введите запрос:")
        self.query_label.pack()
        self.query_entry = tk.Entry(self.master)
        self.query_entry.pack(pady=5)

        self.search_button = tk.Button(self.master, text="Искать", command=self.search_documents)
        self.search_button.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(pady=5)

        self.results = []

    def set_language(self, lang):
        self.language_var.set(lang)
        messagebox.showinfo("Информация", f"Выбран язык: {lang}")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path = file_path
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, text)

    def process_document(self):
        if not hasattr(self, 'file_path'):
            messagebox.showwarning("Внимание", "Сначала загрузите файл.")
            return

        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        words_with_tags = text.split()
        informative_words = [word.split('/')[0] for word in words_with_tags if word.split('/')[-1] not in UNINFORMATIVE_TAGS and word.split('/')[0] not in STOP_WORDS[self.language_var.get()]]
        
        
        self.cleaned_text = " ".join(informative_words)

    
        canonical_words = informative_words

        
        word_frequencies = Counter(canonical_words)

    
        max_frequency = max(word_frequencies.values())
        word_weights = {word: freq / max_frequency for word, freq in word_frequencies.items()}

        
        self.results.append({
            "file_path": self.file_path,
            "word_frequencies": word_frequencies,
            "word_weights": word_weights
        })

        # Display results
        self.display_results()

    def display_results(self, sorted_by=None):
        if not self.results:
            messagebox.showwarning("Внимание", "Сначала обработайте документ.")
            return

        word_frequencies = self.results[-1]['word_frequencies']
        word_weights = self.results[-1]['word_weights']

        if sorted_by == "frequency":
            sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
        else:
            sorted_words = word_frequencies.items()

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Информативные слова, их частоты и веса:\n")
        for word, value in sorted_words:
            freq = word_frequencies[word]
            weight = word_weights[word]
            self.text_area.insert(tk.END, f"{word}: частота={freq}, вес={weight:.4f}\n")

    def search_documents(self):
        query = self.query_entry.get().strip().split()
        if not query:
            messagebox.showwarning("Внимание", "Введите запрос.")
            return

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Результаты поиска для запроса: {' '.join(query)}\n\n")

        relevant_docs = []
        for result in self.results:
            relevance = sum(result["word_weights"].get(word, 0) for word in query)
            if relevance > 0:
                relevant_docs.append((relevance, result["file_path"]))

        relevant_docs.sort(reverse=True, key=lambda x: x[0])
        for relevance, file_path in relevant_docs:
            self.text_area.insert(tk.END, f"Документ: {os.path.basename(file_path)}, Релевантность: {relevance:.4f}\n")

        if not relevant_docs:
            self.text_area.insert(tk.END, "Нет релевантных документов.")

    def save_results(self):
        if not self.results:
            messagebox.showwarning("Внимание", "Сначала обработайте документ.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as file:
                for result in self.results:
                    file.write(f"Документ: {os.path.basename(result['file_path'])}\n")
                    file.write("Информативные слова, их частоты и веса:\n")
                    for word, freq in result['word_frequencies'].items():
                        weight = result['word_weights'][word]
                        file.write(f"{word}: частота={freq}, вес={weight:.4f}\n")
                    file.write("\n")

            if hasattr(self, 'cleaned_text'):
                cleaned_text_path = os.path.splitext(save_path)[0] + "_cleaned.txt"
                with open(cleaned_text_path, 'w', encoding='utf-8') as file:
                    file.write(self.cleaned_text)

            messagebox.showinfo("Информация", "Результаты сохранены успешно.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchEngineApp(root)
    root.mainloop()
    