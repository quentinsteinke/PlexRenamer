import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def browse_files():
    files = filedialog.askopenfilenames(title="Select MKV files", filetypes=[("MKV files", "*.mkv")])
    if files:
        for file in files:
            listbox_files.insert(tk.END, file)

def move_elements_up():
    selected_indices = list(listbox_files.curselection())
    if not selected_indices:
        return

    for index in selected_indices:
        if index > 0:
            listbox_files.insert(index-1, listbox_files.get(index))
            listbox_files.delete(index+1)
            listbox_files.select_set(index-1)

def move_elements_down():
    selected_indices = list(listbox_files.curselection())
    if not selected_indices:
        return

    selected_indices.reverse()

    for index in selected_indices:
        if index < listbox_files.size() - 1:
            listbox_files.insert(index+2, listbox_files.get(index))
            listbox_files.delete(index)
            listbox_files.selection_set(index+1)

def group_as_special():
    SPECIAL_PREFIX = "[Special] "
    selected_indices = list(listbox_files.curselection())
    
    if not selected_indices:
        return
    
    for index in selected_indices:
        file = listbox_files.get(index)
        
        if SPECIAL_PREFIX not in file:
            new_item_text = SPECIAL_PREFIX + file
            listbox_files.delete(index)
            listbox_files.insert(index, new_item_text)

def rename_files():
    SPECIAL_PREFIX = "[Special] "
    files = list(listbox_files.get(0, tk.END))
    show_name = entry_show_name.get()
    season_number = int(entry_season_number.get())
    episode_start_number = int(entry_episode_start_number.get()) if entry_episode_start_number.get() else 1
    special_start_number = int(entry_special_start_number.get()) if entry_special_start_number.get() else 1
    
    episode_number = episode_start_number
    special_episode_number = special_start_number
    for file in files:
        file_without_special = file.replace(SPECIAL_PREFIX, '')
        if SPECIAL_PREFIX not in file:
            old_path = file
            new_name = f"{show_name} - s{season_number:02d}e{episode_number:02d}.mkv"
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            episode_number += 1
        else:
            old_path = file_without_special
            new_name = f"{show_name} - s00e{special_episode_number:02d}.mkv"
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            special_episode_number += 1

    print("Files renamed successfully.")



root = tk.Tk()
root.title("Plex Renamer")
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10))

top_frame = ttk.Frame(root, padding=(10, 10), borderwidth=2, relief="groove")
top_frame.pack(fill=tk.BOTH, expand=True)

listbox_frame = ttk.Frame(top_frame)
listbox_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

top_frame.rowconfigure(0, weight=1)
top_frame.columnconfigure(0, weight=1)

listbox_files = tk.Listbox(listbox_frame, width=50, selectmode=tk.EXTENDED)
listbox_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_horizontal = ttk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL, command=listbox_files.xview)
scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

listbox_files.config(xscrollcommand=scrollbar_horizontal.set)

scrollbar_vertical = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox_files.yview)
scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

listbox_files.config(yscrollcommand=scrollbar_vertical.set)

# Create a frame for the buttons
buttons_frame = ttk.Frame(top_frame, padding=(10, 10), borderwidth=2, relief="groove")
buttons_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)

# Add the move up button to the buttons frame
button_up = ttk.Button(buttons_frame, text="Move Up", command=move_elements_up)
button_up.pack(side=tk.TOP, padx=5, pady=5)

# Add the move down button to the buttons frame
button_down = ttk.Button(buttons_frame, text="Move Down", command=move_elements_down)
button_down.pack(side=tk.TOP, padx=5, pady=5)

# Add the group as special button to the buttons frame
button_group_special = ttk.Button(buttons_frame, text="Group as Special", command=group_as_special)
button_group_special.pack(side=tk.TOP, padx=5, pady=5)

# Create a frame for the entry fields
entry_frame = ttk.Frame(top_frame, padding=(10, 10), borderwidth=2, relief="groove")
entry_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N)

# Add the show name label and entry to the entry frame
ttk.Label(entry_frame, text="Show Name:").pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)
entry_show_name = ttk.Entry(entry_frame, width=50)
entry_show_name.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)

# Add the season number label and entry to the entry frame
ttk.Label(entry_frame, text="Season Number:").pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)
entry_season_number = ttk.Entry(entry_frame, width=10)
entry_season_number.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)

# Add the episode start number label and entry to the entry frame
ttk.Label(entry_frame, text="Episode Start Number:").pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)
entry_episode_start_number = ttk.Entry(entry_frame, width=10)
entry_episode_start_number.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)

# Add the special start number label and entry to the entry frame
ttk.Label(entry_frame, text="Special Start Number:").pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)
entry_special_start_number = ttk.Entry(entry_frame, width=10)
entry_special_start_number.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)

# Add the rename files button to the frame
button_rename = ttk.Button(entry_frame, text="Rename Files", command=rename_files)
button_rename.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.W)

# Start the main loop
root.mainloop()
