import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog

class NexeoText:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexeo | text")
        self.root.geometry("1100x750")
        
        self.current_file = None
        self.font_family = "Consolas"
        self.font_size = 12
        
        self.bg_color = "#1e1e1e"
        self.fg_color = "#d4d4d4"
        self.linenum_color = "#858585"
        self.accent_color = "#007acc"

        self.setup_ui()

    def setup_ui(self):
        self.menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=lambda: self.text_area.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.text_area.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        format_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        font_sub = tk.Menu(format_menu, tearoff=0)
        for f in ["Consolas", "Arial", "Courier New", "Verdana", "Times New Roman"]:
            font_sub.add_command(label=f, command=lambda font=f: self.change_font(font))
        format_menu.add_cascade(label="Font Family", menu=font_sub)
        
        size_sub = tk.Menu(format_menu, tearoff=0)
        for s in [10, 12, 14, 16, 20, 24, 32]:
            size_sub.add_command(label=str(s), command=lambda size=s: self.change_size(size))
        format_menu.add_cascade(label="Font Size", menu=size_sub)
        
        format_menu.add_separator()
        format_menu.add_command(label="Text Color", command=self.change_fg)
        format_menu.add_command(label="Background Color", command=self.change_bg)
        self.menu_bar.add_cascade(label="Format", menu=format_menu)

        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Toggle Fullscreen", command=self.toggle_fullscreen, accelerator="F11")
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=self.menu_bar)

        self.status_bar = tk.Label(self.root, text="Ready", anchor='e', bg=self.accent_color, fg="white", font=("Segoe UI", 9), padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.line_numbers = tk.Text(self.root, width=4, padx=5, takefocus=0, border=0, background="#252526", foreground=self.linenum_color, state='disabled', font=(self.font_family, self.font_size))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area = tk.Text(self.root, undo=True, wrap='none', background=self.bg_color, foreground=self.fg_color, insertbackground="white", selectbackground="#264f78", border=0, font=(self.font_family, self.font_size), padx=10, pady=10)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        self.text_area.bind('<KeyRelease>', self.update_ui)
        self.text_area.bind('<MouseWheel>', self.update_ui)
        self.text_area.bind('<Control-f>', lambda e: self.find_text())
        
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())

    def update_ui(self, event=None):
        self.update_line_numbers()
        self.update_status_bar()

    def update_line_numbers(self):
        line_count = self.text_area.get('1.0', 'end-1c').count('\n') + 1
        lines = '\n'.join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.config(state='normal', font=(self.font_family, self.font_size))
        self.line_numbers.delete('1.0', tk.END)
        self.line_numbers.insert('1.0', lines)
        self.line_numbers.config(state='disabled')
        self.line_numbers.yview_moveto(self.text_area.yview()[0])

    def update_status_bar(self):
        cursor_pos = self.text_area.index(tk.INSERT).split('.')
        content = self.text_area.get('1.0', 'end-1c')
        words = len(content.split())
        chars = len(content)
        self.status_bar.config(text=f"Words: {words} | Chars: {chars} | Line: {cursor_pos[0]} | Col: {cursor_pos[1]}")

    def change_font(self, font):
        self.font_family = font
        self.text_area.config(font=(self.font_family, self.font_size))
        self.update_ui()

    def change_size(self, size):
        self.font_size = size
        self.text_area.config(font=(self.font_family, self.font_size))
        self.update_ui()

    def change_fg(self):
        color = colorchooser.askcolor(title="Select Text Color")[1]
        if color:
            self.fg_color = color
            self.text_area.config(foreground=self.fg_color)

    def change_bg(self):
        color = colorchooser.askcolor(title="Select Background Color")[1]
        if color:
            self.bg_color = color
            self.text_area.config(background=self.bg_color)

    def toggle_fullscreen(self):
        is_full = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_full)

    def find_text(self):
        search_query = simpledialog.askstring("Find", "Enter text to find:")
        if search_query:
            idx = '1.0'
            while True:
                idx = self.text_area.search(search_query, idx, nocase=1, stopindex=tk.END)
                if not idx: break
                lastidx = f"{idx}+{len(search_query)}c"
                self.text_area.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text_area.tag_config('found', background='yellow', foreground='black')
            self.root.after(2000, lambda: self.text_area.tag_remove('found', '1.0', tk.END))

    def new_file(self):
        self.text_area.delete('1.0', tk.END)
        self.current_file = None
        self.root.title("Nexeo | text")
        self.update_ui()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if file_path:
            self.text_area.delete('1.0', tk.END)
            with open(file_path, 'r') as file:
                self.text_area.insert('1.0', file.read())
            self.current_file = file_path
            self.root.title(f"Nexeo | {file_path}")
            self.update_ui()

    def save_file(self):
        if self.current_file:
            try:
                content = self.text_area.get('1.0', tk.END)
                with open(self.current_file, 'w') as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", e)
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if file_path:
            self.current_file = file_path
            self.save_file()
            self.root.title(f"Nexeo | {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NexeoText(root)
    root.mainloop()
