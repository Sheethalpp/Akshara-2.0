import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from tkinter.scrolledtext import ScrolledText
import subprocess

def ask_for_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_input = simpledialog.askstring("Input", "Please enter your text:")
    if user_input is not None:
        print(f"You entered: {user_input}")
    else:
        print("No input provided")
    return user_input

class SpecialTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Akshara 2.0")

        self.current_lang = "Plain Text"
        self.syntax_themes = {
            "Plain Text": {"foreground": "black", "background": "white"},
            "Python": {"foreground": "#dcdcaa", "background": "#1e1e1e"},
            "JavaScript": {"foreground": "#dcdcaa", "background": "#1e1e1e"},
            "Markdown": {"foreground": "#dcdcaa", "background": "#1e1e1e"},
            "C": {"foreground": "#dcdcaa", "background": "#1e1e1e"},
            "C++": {"foreground": "#dcdcaa", "background": "#1e1e1e"},
            "C#": {"foreground": "#dcdcaa", "background": "#1e1e1e"},
        }

        self.text_widget = ScrolledText(root, wrap="word", undo=True, bg="white", fg="black", bd=2, relief=tk.GROOVE)
        self.text_widget.pack(expand="yes", fill="both", side=tk.LEFT)

        # Adding scrollbar for the text widget
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Line numbers
        self.line_numbers = tk.Text(root, width=4, bg="#f0f0f0", bd=0, padx=4, pady=4, wrap="none", state="disabled")
        self.line_numbers.pack(side=tk.LEFT, fill="y")
        self.update_line_numbers()

        # Menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy, accelerator="Alt+F4")

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Bold", command=self.toggle_bold, accelerator="Ctrl+B")
        self.edit_menu.add_command(label="Italic", command=self.toggle_italic, accelerator="Ctrl+I")
        self.edit_menu.add_command(label="Underline", command=self.toggle_underline, accelerator="Ctrl+U")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Align Left", command=self.align_left, accelerator="Ctrl+L")
        self.edit_menu.add_command(label="Align Center", command=self.align_center, accelerator="Ctrl+E")
        self.edit_menu.add_command(label="Align Right", command=self.align_right, accelerator="Ctrl+R")
        self.edit_menu.add_command(label="Justify", command=self.justify, accelerator="Ctrl+J")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        self.edit_menu.add_command(label="Find", command=self.find, accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Replace", command=self.replace, accelerator="Ctrl+H")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Insert Bullets", command=self.insert_bullets, accelerator="Ctrl+Shift+B")

        # Format menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Font", command=self.change_font, accelerator="Ctrl+F")
        self.format_menu.add_command(label="Text Color", command=self.change_text_color, accelerator="Ctrl+T")
        self.format_menu.add_command(label="Background Color", command=self.change_bg_color, accelerator="Ctrl+G")
        self.format_menu.add_command(label="Font Size", command=self.change_font_size, accelerator="Ctrl+Shift+F")
        self.format_menu.add_command(label="Font Style", command=self.change_font_style, accelerator="Ctrl+Shift+S")
        self.format_menu.add_separator()
        self.syntax_menu = tk.Menu(self.format_menu, tearoff=0)
        self.format_menu.add_cascade(label="Syntax Highlighting", menu=self.syntax_menu)
        self.syntax_lang = tk.StringVar()
        for lang in self.syntax_themes.keys():
            self.syntax_menu.add_radiobutton(label=lang, variable=self.syntax_lang, value=lang, command=self.change_syntax_highlighting)

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Line Count", command=self.word_count, accelerator="Ctrl+W")
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode, accelerator="Ctrl+D")

       # Theme menu (added)
        self.theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Themes", menu=self.theme_menu)
        self.theme_menu.add_command(label="Light", command=lambda: self.change_theme("light"))
        self.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))
        self.theme_menu.add_command(label="Solarized", command=lambda: self.change_theme("solarized"))
        self.theme_menu.add_command(label="Github", command=lambda: self.change_theme("Github"))

        # Language menu
        self.lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Compiler", menu=self.lang_menu)
        self.lang_menu.add_command(label="Python", command=self.run_code, accelerator="Ctrl+P")
        self.lang_menu.add_command(label="Java", command=self.run_java_code, accelerator="Ctrl+Shift+J")
        self.lang_menu.add_command(label="C", command=self.run_c_code, accelerator="Ctrl+Shift+C")
        self.lang_menu.add_command(label="C++", command=self.run_cpp_code, accelerator="Ctrl+Shift+P")
        self.lang_menu.add_command(label="C#", command=self.run_csharp_code, accelerator="Ctrl+Shift+H")

        # Status bar
        self.status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Update status bar
        self.text_widget.bind("<KeyRelease>", self.update_status_bar)

        # Bind update line numbers
        self.text_widget.bind("<KeyRelease>", self.update_line_numbers)

        # Bind keyboard shortcuts
        self.bind_shortcuts()
    def change_theme(self, theme):
        if theme == "light":
            self.text_widget.config(bg="white", fg="black")
        elif theme == "dark":
            self.text_widget.config(bg="#1e1e1e", fg="#dcdcaa")
        elif theme == "solarized":
            self.text_widget.config(bg="#fdf6e3", fg="#657b83")
        elif theme == "Github":
            self.text_widget.config(bg="#99ff99", fg="black")
        
    def bind_shortcuts(self):
        # File shortcuts
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda event: self.save_as_file())
        self.root.bind("<Alt-F4>", lambda event: self.root.destroy())

        # Edit shortcuts
        self.root.bind("<Control-b>", lambda event: self.toggle_bold())
        self.root.bind("<Control-i>", lambda event: self.toggle_italic())
        self.root.bind("<Control-u>", lambda event: self.toggle_underline())
        self.root.bind("<Control-l>", lambda event: self.align_left())
        self.root.bind("<Control-e>", lambda event: self.align_center())
        self.root.bind("<Control-r>", lambda event: self.align_right())
        self.root.bind("<Control-j>", lambda event: self.justify())
        self.root.bind("<Control-x>", lambda event: self.cut())
        self.root.bind("<Control-c>", lambda event: self.copy())
        self.root.bind("<Control-v>", lambda event: self.paste())
        self.root.bind("<Control-a>", lambda event: self.select_all())
        self.root.bind("<Control-f>", lambda event: self.find())
        self.root.bind("<Control-h>", lambda event: self.replace())
        self.root.bind("<Control-Shift-b>", lambda event: self.insert_bullets())

        # Format shortcuts
        self.root.bind("<Control-f>", lambda event: self.change_font())
        self.root.bind("<Control-t>", lambda event: self.change_text_color())
        self.root.bind("<Control-g>", lambda event: self.change_bg_color())
        self.root.bind("<Control-Shift-f>", lambda event: self.change_font_size())
        self.root.bind("<Control-Shift-s>", lambda event: self.change_font_style())

        # View shortcuts
        self.root.bind("<Control-w>", lambda event: self.word_count())
        self.root.bind("<Control-d>", lambda event: self.toggle_dark_mode())

        # Language shortcuts
        self.root.bind("<Control-p>", lambda event: self.run_code())
        self.root.bind("<Control-Shift-j>", lambda event: self.run_java_code())
        self.root.bind("<Control-Shift-c>", lambda event: self.run_c_code())
        self.root.bind("<Control-Shift-p>", lambda event: self.run_cpp_code())
        self.root.bind("<Control-Shift-h>", lambda event: self.run_csharp_code())

       

        # Status bar
        self.status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Update status bar
        self.text_widget.bind("<KeyRelease>", self.update_status_bar)

        # Bind update line numbers
        self.text_widget.bind("<KeyRelease>", self.update_line_numbers)

    def run_code(self):
        code = self.text_widget.get("1.0", tk.END)
        try:
            output = subprocess.check_output(["python", "-c", code], stderr=subprocess.STDOUT, universal_newlines=True)
            messagebox.showinfo("Output", output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.output)

    def run_java_code(self):
        code = self.text_widget.get("1.0", tk.END)
        with open("Temp.java", "w") as f:
            f.write(code)
        try:
            compile_output = subprocess.check_output(["javac", "Temp.java"], stderr=subprocess.STDOUT, universal_newlines=True)
            if compile_output == "":
                class_name = simpledialog.askstring("Class Name", "Enter the class name to run:")
                if not class_name:
                    class_name = "Temp"
                run_output = subprocess.check_output(["java", class_name], stderr=subprocess.STDOUT, universal_newlines=True)
                messagebox.showinfo("Output", run_output)
            else:
                messagebox.showerror("Compilation Error", compile_output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.output)

    def run_c_code(self):
        code = self.text_widget.get("1.0", tk.END)
        with open("Temp.c", "w") as f:
            f.write(code)
        try:
            compile_output = subprocess.check_output(["gcc", "-o", "Temp", "Temp.c"], stderr=subprocess.STDOUT, universal_newlines=True)
            if compile_output == "":
                run_output = subprocess.check_output(["./Temp"], stderr=subprocess.STDOUT, universal_newlines=True)
                messagebox.showinfo("Output", run_output)
            else:
                messagebox.showerror("Compilation Error", compile_output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.output)

    def run_cpp_code(self):
        code = self.text_widget.get("1.0", tk.END)
        with open("Temp.cpp", "w") as f:
            f.write(code)
        try:
            compile_output = subprocess.check_output(["g++", "-o", "Temp", "Temp.cpp"], stderr=subprocess.STDOUT, universal_newlines=True)
            if compile_output == "":
                run_output = subprocess.check_output(["./Temp"], stderr=subprocess.STDOUT, universal_newlines=True)
                messagebox.showinfo("Output", run_output)
            else:
                messagebox.showerror("Compilation Error", compile_output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.output)

    def run_csharp_code(self):
        code = self.text_widget.get("1.0", tk.END)
        with open("Temp.cs", "w") as f:
            f.write(code)
        try:
            compile_output = subprocess.check_output(["csc", "Temp.cs"], stderr=subprocess.STDOUT, universal_newlines=True)
            if compile_output == "":
                run_output = subprocess.check_output(["mono", "Temp.exe"], stderr=subprocess.STDOUT, universal_newlines=True)
                messagebox.showinfo("Output", run_output)
            else:
                messagebox.showerror("Compilation Error", compile_output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.output)

    
    def update_line_numbers(self, event=None):
        lines = self.text_widget.get(1.0, "end-1c").count('\n') + 1
        self.line_numbers.config(state="normal")
        self.line_numbers.delete(1.0, "end")
        self.line_numbers.insert("end", "\n".join(str(i) for i in range(1, lines + 1)))
        self.line_numbers.config(state="disabled")

    def new_file(self):
        self.text_widget.delete("1.0", tk.END)
        self.update_line_numbers()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert(tk.END, content)
            self.update_line_numbers()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get("1.0", tk.END)
                file.write(content)

    def save_as_file(self):
        self.save_file()

    def toggle_bold(self):
        current_tags = self.text_widget.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_widget.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_widget.tag_add("bold", "sel.first", "sel.last")
        bold_font = ("Helvetica", 12, "bold")
        self.text_widget.tag_configure("bold", font=bold_font)

    def toggle_italic(self):
        current_tags = self.text_widget.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_widget.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_widget.tag_add("italic", "sel.first", "sel.last")
        italic_font = ("Helvetica", 12, "italic")
        self.text_widget.tag_configure("italic", font=italic_font)

    def toggle_underline(self):
        current_tags = self.text_widget.tag_names("sel.first")
        if "underline" in current_tags:
            self.text_widget.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.text_widget.tag_add("underline", "sel.first", "sel.last")
        underline_font = ("Helvetica", 12, "underline")
        self.text_widget.tag_configure("underline", font=underline_font)

    def align_left(self):
        self.text_widget.tag_configure("left", justify=tk.LEFT)
        self.text_widget.tag_add("left", "sel.first", "sel.last")

    def align_center(self):
        self.text_widget.tag_configure("center", justify=tk.CENTER)
        self.text_widget.tag_add("center", "sel.first", "sel.last")

    def align_right(self):
        self.text_widget.tag_configure("right", justify=tk.RIGHT)
        self.text_widget.tag_add("right", "sel.first", "sel.last")

    def justify(self):
        self.text_widget.tag_configure("justify", justify=tk.JUSTIFY)
        self.text_widget.tag_add("justify", "sel.first", "sel.last")

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")

    def select_all(self):
        self.text_widget.tag_add("sel", "1.0", "end")

    def find(self):
        target = simpledialog.askstring("Find", "Enter text to find:")
        if target:
            start_pos = "1.0"
            while True:
                start_pos = self.text_widget.search(target, start_pos, tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(target)}c"
                self.text_widget.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            self.text_widget.tag_configure("highlight", background="yellow")

    def replace(self):
        target = simpledialog.askstring("Replace", "Enter text to replace:")
        replacement = simpledialog.askstring("Replace", "Enter replacement text:")
        if target and replacement:
            content = self.text_widget.get("1.0", tk.END)
            content = content.replace(target, replacement)
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", content)

    def insert_bullets(self):
        selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        bullet_text = "\n".join([f"• {line}" for line in selected_text.split("\n")])
        self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.insert(tk.INSERT, bullet_text)

    def superscript(self):
        selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.insert(tk.INSERT, selected_text)
        self.text_widget.tag_add("superscript", tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.tag_configure("superscript", offset=4, font=("Helvetica", 8))

    def subscript(self):
        selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.insert(tk.INSERT, selected_text)
        self.text_widget.tag_add("subscript", tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.tag_configure("subscript", offset=-4, font=("Helvetica", 8))

    def change_font(self):
        new_font = simpledialog.askstring("Font", "Enter font family:")
        if new_font:
            self.text_widget.config(font=(new_font, 12))

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_widget.config(fg=color)

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_widget.config(bg=color)

    def change_font_size(self):
        new_size = simpledialog.askinteger("Font Size", "Enter font size:")
        if new_size:
            current_font = self.text_widget.cget("font")
            font_family = current_font.split()[0]
            self.text_widget.config(font=(font_family, new_size))

    def change_font_style(self):
        new_style = simpledialog.askstring("Font Style", "Enter font style (bold/italic/underline):")
        if new_style:
            current_font = self.text_widget.cget("font")
            font_family, font_size = current_font.split()[0], current_font.split()[1]
            self.text_widget.config(font=(font_family, font_size, new_style))

    def change_syntax_highlighting(self):
        selected_lang = self.syntax_lang.get()
        theme = self.syntax_themes.get(selected_lang, {"foreground": "black", "background": "white"})
        self.text_widget.config(fg=theme["foreground"], bg=theme["background"])

    def word_count(self):
        content = self.text_widget.get("1.0", tk.END)
        words = len(content.split())
        messagebox.showinfo("Line Count", f"Line Count: {words}")

    def toggle_dark_mode(self):
        if self.text_widget.cget("bg") == "white":
            self.text_widget.config(bg="#1e1e1e", fg="#dcdcaa", insertbackground="white")
        else:
            self.text_widget.config(bg="white", fg="black", insertbackground="black")

    
    def update_status_bar(self, event=None):
        row, col = self.text_widget.index(tk.INSERT).split(".")
        self.status_bar.config(text=f"Row: {row} | Column: {col}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpecialTextEditor(root)
    root.mainloop()