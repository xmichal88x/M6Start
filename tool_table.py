import json
import tkinter as tk
from tkinter import ttk, messagebox

JSON_FILE = "narzedzia.json"

TRYB_PRACY_MAP = {0: "Dół", 1: "Góra"}
TRYB_PRACY_REVERSE = {"Dół": 0, "Góra": 1}

sort_order = {"Narzędzie": True, "Kieszeń": True, "Tryb pracy": True}  # Domyślnie sortowanie rosnące

def wczytaj_ustawienia():
    """Wczytuje dane z JSON i konwertuje wartości liczbowe na opisy."""
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
        for tool, params in data.items():
            params["tryb_pracy"] = TRYB_PRACY_MAP.get(params.get("tryb_pracy", 0), "Nieznany")
            params["kieszen"] = params.get("kieszen", 0)  # Domyślnie 0, jeśli brak
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def zapisz_ustawienia(data):
    """Zamienia opisy na wartości liczbowe i zapisuje do JSON."""
    for tool, params in data.items():
        params["tryb_pracy"] = TRYB_PRACY_REVERSE.get(params.get("tryb_pracy", "Dół"), 0)
        params["kieszen"] = params.get("kieszen", 0)
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def odswiez_tabele():
    """Odświeża tabelę danymi z JSON."""
    data = wczytaj_ustawienia()
    tree.delete(*tree.get_children())
    for tool, params in sorted(data.items(), key=lambda x: int(x[0])):  # Domyślnie sortowanie po nr narzędzia
        tree.insert("", "end", values=(tool, params["kieszen"], params["tryb_pracy"]))


def sortuj_tabele(col):
    """Sortuje tabelę po kliknięciu w nagłówek kolumny."""
    data = [tree.item(row)["values"] for row in tree.get_children()]
    
    if col == "Narzędzie":
        key = lambda x: int(x[0])  # Sortowanie numeryczne
    elif col == "Kieszeń":
        key = lambda x: int(x[1])
    else:  # Tryb pracy
        key = lambda x: x[2]

    sort_order[col] = not sort_order[col]  # Zmiana kierunku sortowania
    data.sort(key=key, reverse=not sort_order[col])

    tree.delete(*tree.get_children())
    for row in data:
        tree.insert("", "end", values=row)

def on_double_click(event):
    """Tworzy pole Entry nad zaznaczoną komórką i umożliwia edycję."""
    global entry_widget, combo_widget

    selected_item = tree.selection()
    if not selected_item:
        return
    
    column = tree.identify_column(event.x)
    column_index = int(column[1:]) - 1
    row_id = tree.selection()[0]
    x, y, width, height = tree.bbox(row_id, column_index)

    if column_index == 2:  # Jeśli edytujemy Tryb Pracy -> Pokaż ComboBox
        combo_widget = ttk.Combobox(root, values=["Dół", "Góra"])
        combo_widget.place(x=x+tree.winfo_x(), y=y+tree.winfo_y(), width=width, height=height)
        combo_widget.set(tree.item(row_id, "values")[column_index])
        combo_widget.focus()
        combo_widget.bind("<Return>", lambda e: save_edit(row_id, column_index, combo_widget.get()))
        combo_widget.bind("<FocusOut>", lambda e: combo_widget.destroy())
    else:  # Normalna edycja dla innych kolumn
        entry_widget = tk.Entry(root)
        entry_widget.place(x=x+tree.winfo_x(), y=y+tree.winfo_y(), width=width, height=height)
        entry_widget.insert(0, tree.item(row_id, "values")[column_index])
        entry_widget.focus()
        entry_widget.bind("<Return>", lambda e: save_edit(row_id, column_index, entry_widget.get()))
        entry_widget.bind("<FocusOut>", lambda e: entry_widget.destroy())

def save_edit(row_id, column_index, new_value):
    """Zapisuje nową wartość do tabeli i JSON."""
    values = list(tree.item(row_id, "values"))
    values[column_index] = new_value
    tree.item(row_id, values=values)

    data = wczytaj_ustawienia()
    tool_number = values[0]

    if str(tool_number) in data:
        if column_index == 1:  # Kieszeń
            data[str(tool_number)]["kieszen"] = int(new_value)
        elif column_index == 2:  # Tryb pracy
            data[str(tool_number)]["tryb_pracy"] = new_value

    zapisz_ustawienia(data)

def dodaj_narzedzie():
    """Dodaje nowe narzędzie do listy."""
    tool = entry_tool.get()
    kieszen = entry_kieszen.get()
    tryb_pracy = combo_tryb_pracy.get()

    if not tool.isdigit() or not kieszen.isdigit():
        messagebox.showerror("Błąd", "Numer narzędzia i kieszeni muszą być liczbami.")
        return

    data = wczytaj_ustawienia()
    data[tool] = {"kieszen": int(kieszen), "tryb_pracy": tryb_pracy}
    zapisz_ustawienia(data)
    odswiez_tabele()

# Tworzenie głównego okna
root = tk.Tk()
root.title("Edycja ustawień narzędzi")

# Tworzenie tabeli
tree = ttk.Treeview(root, columns=("Narzędzie", "Kieszeń", "Tryb pracy"), show="headings")
tree.heading("Narzędzie", text="Narzędzie", command=lambda: sortuj_tabele("Narzędzie"))
tree.heading("Kieszeń", text="Kieszeń", command=lambda: sortuj_tabele("Kieszeń"))
tree.heading("Tryb pracy", text="Tryb pracy", command=lambda: sortuj_tabele("Tryb pracy"))
tree.bind("<Double-1>", on_double_click)
tree.pack()

# Pola do dodawania nowych narzędzi
frame_add = tk.Frame(root)
frame_add.pack(pady=5)

tk.Label(frame_add, text="Nr narzędzia:").pack(side=tk.LEFT, padx=5)
entry_tool = tk.Entry(frame_add, width=5)
entry_tool.pack(side=tk.LEFT)

tk.Label(frame_add, text="Kieszeń:").pack(side=tk.LEFT, padx=5)
entry_kieszen = tk.Entry(frame_add, width=5)
entry_kieszen.pack(side=tk.LEFT)

tk.Label(frame_add, text="Tryb pracy:").pack(side=tk.LEFT, padx=5)
combo_tryb_pracy = ttk.Combobox(frame_add, values=["Dół", "Góra"])
combo_tryb_pracy.pack(side=tk.LEFT)

btn_add = tk.Button(frame_add, text="Dodaj", command=dodaj_narzedzie)
btn_add.pack(side=tk.LEFT, padx=10)

btn_refresh = tk.Button(root, text="Odśwież", command=odswiez_tabele)
btn_refresh.pack(side=tk.LEFT, padx=5)

odswiez_tabele()
root.mainloop()
