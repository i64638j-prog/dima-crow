import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class RandomTaskGenerator:
    def __init__(self, window):
        self.window = window
        self.window.title("Random Task Generator - Генератор случайных задач")
        self.window.geometry("900x700")
        
        # Предопределённые задачи
        self.default_tasks = [
            {"task": "Прочитать статью", "type": "Учёба"},
            {"task": "Сделать зарядку", "type": "Спорт"},
            {"task": "Написать код", "type": "Работа"},
            {"task": "Выучить 10 новых слов", "type": "Учёба"},
            {"task": "Пробежка 30 минут", "type": "Спорт"},
            {"task": "Созвониться с клиентом", "type": "Работа"},
            {"task": "Посмотреть вебинар", "type": "Учёба"},
            {"task": "Йога или растяжка", "type": "Спорт"},
            {"task": "Закончить отчёт", "type": "Работа"},
            {"task": "Прочитать главу книги", "type": "Учёба"},
            {"task": "Отжимания 50 раз", "type": "Спорт"},
            {"task": "Спланировать задачи на день", "type": "Работа"},
            {"task": "Решить задачу по математике", "type": "Учёба"},
            {"task": "Плавание", "type": "Спорт"},
            {"task": "Ответить на письма", "type": "Работа"},
            {"task": "Просмотреть документацию", "type": "Учёба"},
            {"task": "Приседания 100 раз", "type": "Спорт"},
            {"task": "Оптимизировать рабочий процесс", "type": "Работа"}
        ]
        
        # Загрузка задач (кастомные + предопределённые)
        self.tasks = []
        self.load_tasks()
        
        self.history = []
        self.current_file = None
        
        self.setup_ui()
        self.create_history_table()
        self.update_tasks_list()
        
    def load_tasks(self):
        """Загрузка задач из файла или использование предопределённых"""
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                saved_tasks = json.load(f)
                self.tasks = saved_tasks
        except FileNotFoundError:
            self.tasks = self.default_tasks.copy()
        except Exception as e:
            print(f"Ошибка загрузки задач: {e}")
            self.tasks = self.default_tasks.copy()
    
    def save_tasks(self):
        """Сохранение задач в файл"""
        try:
            with open('tasks.json', 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения задач: {e}")
    
    def setup_ui(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Панель генерации задачи
        generate_frame = ttk.LabelFrame(main_frame, text="Генератор задач", padding=10)
        generate_frame.pack(fill="x", pady=(0, 10))
        
        # Фильтр типа задачи для генерации
        ttk.Label(generate_frame, text="Тип задачи для генерации:").grid(row=0, column=0, padx=5, pady=5)
        self.gen_type_var = tk.StringVar(value="Все")
        self.gen_type_combo = ttk.Combobox(generate_frame, textvariable=self.gen_type_var, width=15)
        self.gen_type_combo['values'] = ('Все', 'Учёба', 'Спорт', 'Работа')
        self.gen_type_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Кнопка генерации
        self.generate_button = ttk.Button(generate_frame, text="🎲 Сгенерировать задачу", command=self.generate_task)
        self.generate_button.grid(row=0, column=2, padx=20, pady=5)
        
        # Отображение сгенерированной задачи
        self.current_task_label = ttk.Label(generate_frame, text="", font=('Arial', 14, 'bold'), foreground="blue")
        self.current_task_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Панель управления задачами
        tasks_frame = ttk.LabelFrame(main_frame, text="Управление задачами", padding=10)
        tasks_frame.pack(fill="x", pady=(0, 10))
        
        # Добавление новой задачи
        add_frame = ttk.Frame(tasks_frame)
        add_frame.pack(fill="x", pady=5)
        
        ttk.Label(add_frame, text="Новая задача:").pack(side="left", padx=5)
        self.new_task_entry = ttk.Entry(add_frame, width=40)
        self.new_task_entry.pack(side="left", padx=5)
        
        ttk.Label(add_frame, text="Тип:").pack(side="left", padx=5)
        self.new_type_var = tk.StringVar()
        self.new_type_combo = ttk.Combobox(add_frame, textvariable=self.new_type_var, width=12)
        self.new_type_combo['values'] = ('Учёба', 'Спорт', 'Работа')
        self.new_type_combo.pack(side="left", padx=5)
        
        ttk.Button(add_frame, text="➕ Добавить задачу", command=self.add_task).pack(side="left", padx=10)
        
        # Список существующих задач
        list_frame = ttk.Frame(tasks_frame)
        list_frame.pack(fill="both", expand=True, pady=5)
        
        ttk.Label(list_frame, text="Список всех задач:", font=('Arial', 10, 'bold')).pack(anchor="w")
        
        # Таблица задач с прокруткой
        tasks_table_frame = ttk.Frame(list_frame)
        tasks_table_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tasks_table_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tasks_listbox = tk.Listbox(tasks_table_frame, yscrollcommand=scrollbar.set, height=6, font=('Arial', 9))
        self.tasks_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tasks_listbox.yview)
        
        # Кнопки управления задачами (в одном ряду)
        tasks_buttons_frame = ttk.Frame(tasks_frame)
        tasks_buttons_frame.pack(fill="x", pady=5)
        
        ttk.Button(tasks_buttons_frame, text="🗑️ Удалить выбранную", command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(tasks_buttons_frame, text="📋 Сбросить к стандартным", command=self.reset_to_default).pack(side="left", padx=5)
        ttk.Button(tasks_buttons_frame, text="💾 Сохранить задачи", command=self.save_tasks_to_file).pack(side="left", padx=5)
        ttk.Button(tasks_buttons_frame, text="📂 Загрузить задачи", command=self.load_tasks_from_file).pack(side="left", padx=5)
        
        # Панель истории
        history_frame = ttk.LabelFrame(main_frame, text="История задач", padding=10)
        history_frame.pack(fill="both", expand=True)
        
        # Кнопки управления историей
        history_buttons = ttk.Frame(history_frame)
        history_buttons.pack(fill="x", pady=(0, 10))
        
        ttk.Button(history_buttons, text="📊 Показать статистику", command=self.show_statistics).pack(side="left", padx=5)
        ttk.Button(history_buttons, text="🗑️ Очистить историю", command=self.clear_history).pack(side="left", padx=5)
        ttk.Button(history_buttons, text="💾 Сохранить историю", command=self.save_history_to_json).pack(side="left", padx=5)
        ttk.Button(history_buttons, text="📂 Загрузить историю", command=self.load_history_from_json).pack(side="left", padx=5)
        
        # Фильтр истории
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Фильтр по типу:").pack(side="left", padx=5)
        self.history_filter_var = tk.StringVar(value="Все")
        self.history_filter_combo = ttk.Combobox(filter_frame, textvariable=self.history_filter_var, width=12)
        self.history_filter_combo['values'] = ('Все', 'Учёба', 'Спорт', 'Работа')
        self.history_filter_combo.pack(side="left", padx=5)
        
        ttk.Button(filter_frame, text="Применить фильтр", command=self.filter_history).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_history_filter).pack(side="left", padx=5)
        
    def create_history_table(self):
        # Таблица для отображения истории
        table_frame = ttk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        columns = ("#", "Дата и время", "Задача", "Тип")
        self.history_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        self.history_tree.heading("#", text="#")
        self.history_tree.heading("Дата и время", text="Дата и время")
        self.history_tree.heading("Задача", text="Задача")
        self.history_tree.heading("Тип", text="Тип")
        
        self.history_tree.column("#", width=50, anchor="center")
        self.history_tree.column("Дата и время", width=160, anchor="center")
        self.history_tree.column("Задача", width=400)
        self.history_tree.column("Тип", width=100, anchor="center")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.history_tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
    def update_tasks_list(self):
        """Обновление списка задач в Listbox"""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, f"[{task['type']}] {task['task']}")
    
    def generate_task(self):
        """Генерация случайной задачи"""
        filter_type = self.gen_type_var.get()
        
        # Фильтрация задач по типу
        if filter_type == "Все":
            available_tasks = self.tasks
        else:
            available_tasks = [t for t in self.tasks if t['type'] == filter_type]
        
        if not available_tasks:
            messagebox.showwarning("Предупреждение", f"Нет задач типа '{filter_type}'. Добавьте новые задачи или выберите другой тип.")
            return
        
        # Выбор случайной задачи
        selected_task = random.choice(available_tasks)
        
        # Отображение задачи
        self.current_task_label.config(text=f"✨ {selected_task['task']} ✨")
        
        # Добавление в историю
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task": selected_task['task'],
            "type": selected_task['type']
        }
        self.history.append(history_entry)
        self.refresh_history_table()
        
        # Анимация кнопки
        self.generate_button.config(text="✓ Сгенерировано!")
        self.window.after(1500, lambda: self.generate_button.config(text="🎲 Сгенерировать задачу"))
    
    def refresh_history_table(self, filtered_history=None):
        """Обновление таблицы истории"""
        # Очистка таблицы
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        history_to_show = filtered_history if filtered_history is not None else self.history
        
        # Отображение в обратном порядке (сначала новые)
        for i, entry in enumerate(reversed(history_to_show), 1):
            self.history_tree.insert("", "end", values=(
                i,
                entry["timestamp"],
                entry["task"],
                entry["type"]
            ))
    
    def add_task(self):
        """Добавление новой задачи"""
        task_text = self.new_task_entry.get().strip()
        task_type = self.new_type_var.get()
        
        # Валидация
        if not task_text:
            messagebox.showerror("Ошибка", "Текст задачи не может быть пустым")
            return
        
        if not task_type:
            messagebox.showerror("Ошибка", "Выберите тип задачи")
            return
        
        # Проверка на дубликат
        for task in self.tasks:
            if task['task'].lower() == task_text.lower():
                messagebox.showwarning("Предупреждение", "Такая задача уже существует")
                return
        
        self.tasks.append({"task": task_text, "type": task_type})
        self.update_tasks_list()
        self.save_tasks()
        
        # Очистка полей
        self.new_task_entry.delete(0, tk.END)
        self.new_type_var.set("")
        
        messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена в список")
    
    def delete_task(self):
        """Удаление выбранной задачи"""
        selection = self.tasks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return
        
        index = selection[0]
        deleted_task = self.tasks.pop(index)
        self.update_tasks_list()
        self.save_tasks()
        
        messagebox.showinfo("Успех", f"Задача '{deleted_task['task']}' удалена")
    
    def reset_to_default(self):
        """Сброс к стандартным задачам"""
        if messagebox.askyesno("Подтверждение", "Сбросить все задачи к стандартным? Все добавленные задачи будут потеряны."):
            self.tasks = self.default_tasks.copy()
            self.update_tasks_list()
            self.save_tasks()
            messagebox.showinfo("Успех", "Задачи сброшены к стандартным")
    
    def save_tasks_to_file(self):
        """Сохранение задач в JSON-файл"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить задачи"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.tasks, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", f"Задачи сохранены в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
    
    def load_tasks_from_file(self):
        """Загрузка задач из JSON-файла"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Загрузить задачи"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_tasks = json.load(f)
                
                # Валидация загруженных данных
                for task in loaded_tasks:
                    if not all(k in task for k in ("task", "type")):
                        raise ValueError("Неверный формат данных в файле")
                
                self.tasks = loaded_tasks
                self.update_tasks_list()
                self.save_tasks()
                messagebox.showinfo("Успех", f"Загружено {len(self.tasks)} задач")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
    
    def filter_history(self):
        """Фильтрация истории по типу"""
        filter_type = self.history_filter_var.get()
        
        if filter_type == "Все":
            self.refresh_history_table()
        else:
            filtered = [h for h in self.history if h['type'] == filter_type]
            self.refresh_history_table(filtered)
            
            if filtered:
                messagebox.showinfo("Фильтр", f"Найдено {len(filtered)} задач типа '{filter_type}'")
            else:
                messagebox.showinfo("Фильтр", f"Задач типа '{filter_type}' не найдено")
    
    def reset_history_filter(self):
        """Сброс фильтра истории"""
        self.history_filter_var.set("Все")
        self.refresh_history_table()
    
    def clear_history(self):
        """Очистка истории"""
        if self.history:
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
                self.history.clear()
                self.refresh_history_table()
                messagebox.showinfo("Успех", "История очищена")
        else:
            messagebox.showwarning("Предупреждение", "История пуста")
    
    def save_history_to_json(self):
        """Сохранение истории в JSON"""
        if not self.history:
            messagebox.showwarning("Предупреждение", "Нет истории для сохранения")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить историю"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.history, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", f"История сохранена в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
    
    def load_history_from_json(self):
        """Загрузка истории из JSON"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Загрузить историю"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_history = json.load(f)
                
                # Валидация загруженных данных
                for entry in loaded_history:
                    if not all(k in entry for k in ("timestamp", "task", "type")):
                        raise ValueError("Неверный формат данных в файле")
                
                self.history = loaded_history
                self.refresh_history_table()
                messagebox.showinfo("Успех", f"Загружено {len(self.history)} записей истории")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
    
    def show_statistics(self):
        """Показать статистику по истории"""
        if not self.history:
            messagebox.showinfo("Статистика", "История пуста. Сгенерируйте несколько задач для статистики.")
            return
        
        total = len(self.history)
        
        # Подсчёт по типам
        type_counts = {}
        for entry in self.history:
            task_type = entry['type']
            type_counts[task_type] = type_counts.get(task_type, 0) + 1
        
        # Самая популярная задача
        task_counts = {}
        for entry in self.history:
            task = entry['task']
            task_counts[task] = task_counts.get(task, 0) + 1
        
        most_common_task = max(task_counts.items(), key=lambda x: x[1]) if task_counts else ("Нет", 0)
        
        # Формирование сообщения
        stats_text = f"📊 Статистика истории\n\n"
        stats_text += f"Всего сгенерировано задач: {total}\n\n"
        stats_text += f"По типам:\n"
        for task_type, count in type_counts.items():
            percentage = (count / total) * 100
            stats_text += f"  • {task_type}: {count} ({percentage:.1f}%)\n"
        
        stats_text += f"\n⭐ Самая частая задача: '{most_common_task[0]}' ({most_common_task[1]} раз)\n"
        
        messagebox.showinfo("Статистика", stats_text)


if __name__ == "__main__":
    try:
        window = tk.Tk()
        app = RandomTaskGenerator(window)
        window.mainloop()
    except ImportError:
        print("Ошибка: Tkinter не установлен.")
        print("На Linux установите: sudo apt-get install python3-tk")
        input("Нажмите Enter для выхода...")
