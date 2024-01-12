import tkinter as tk
from tkinter import filedialog as fd
from tkinter import font

class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Text Editor')
        self.root.geometry('1200x700') 
        # set the height of the row and column to grow proportionally to the height of the editor window
        self.root.rowconfigure(0, minsize=900, weight=1) 
        self.root.columnconfigure(1, minsize=900, weight=1)
        self.file_path = ''
        # create field to view or/and edit file
        self.text_edit = tk.Text(self.root, undo=True) 

        # creating separate block for open, save, and save as buttons(operations)
        vertical_frame = tk.Frame(self.root)
        open_button = tk.Button(vertical_frame, text = 'Open file', font = ('Arial', '12'),bg = 'green', fg= 'white', command=self.open_file)
        save_button = tk.Button(vertical_frame, text = 'Save', font = ('Arial', '12'), command=self.save_file)
        save_as_button = tk.Button(vertical_frame, text='Save as...', font = ('Arial', '12'), command=self.save_file_as)
        exit_button = tk.Button(vertical_frame, text='Exit', font = ('Arial', '12'), command=self.exit)

        vertical_frame.grid(row=0, column=0, sticky='ns')
        open_button.grid(column=0, row=1, sticky='ew', padx = 5)
        save_button.grid(column=0, row=2, sticky='ew', padx = 5)
        save_as_button.grid(column=0, row=3, sticky = 'ew', padx=5)
        exit_button.grid(column=0, row=4, sticky = 'ew', padx=5)
        self.text_edit.grid(row=0, column=1, sticky='nsew')
        

        # creatibg separate horizontal block to change text font and style, undo and redo, copy, cut and paste operations
        horizontal_frame = tk.Frame(self.root)
        horizontal_frame.grid(row=0, column=1, sticky='new')

        self.font_var = tk.StringVar(self.root)
        self.font_var.set('Choose a font') 
        font_options = font.families()
        font_dropdown = tk.OptionMenu(horizontal_frame, self.font_var, *font_options, command=self.change_font)
        font_dropdown.grid(column=2, row=0, sticky='ew', padx=5)

        self.size_var = tk.StringVar(self.root)
        self.size_var.set('Choose size') 
        size_options = [i for i in range(1, 101)]
        size_dropdown = tk.OptionMenu(horizontal_frame, self.size_var, *size_options, command=self.change_font)
        size_dropdown.grid(column=3, row=0, sticky='ew', padx=5)

        undo_button = tk.Button(horizontal_frame, text='Undo', fon =('Arial', '10'), command=self.text_edit.edit_undo)
        undo_button.grid(column=9, row=0, sticky='ew', padx = 5)

        redo_button = tk.Button(horizontal_frame, text='Redo', font=('Arial', '10'), command=self.text_edit.edit_redo)
        redo_button.grid(column=10, row=0)

        copy_button = tk.Button(horizontal_frame, text='Copy', font=('Arial', '10'), command=lambda: self.copy_text(0))
        cut_button = tk.Button(horizontal_frame, text='Cut', font=('Arial', '10'), command=lambda: self.cut_text(0))
        paste_button = tk.Button(horizontal_frame, text='Paste', font=('Arial', '10'), command=lambda: self.paste_text(0))

        copy_button.grid(column=5, row=0)
        cut_button.grid(column=6, row=0)
        paste_button.grid(column=7, row=0)


    def open_file(self):
        '''This method allows to choose a file for editing (Initial directory is Desktop)'''
        self.file_path = fd.askopenfilename(initialdir = r"C:\Users\meryi\Desktop", title = 'Choose the file to edit:',
                                        filetypes = [('text files', '*.txt')])
        
        # delete existing text in editor before opening a fdocument from beginning to end
        if self.file_path:
            self.text_edit.delete(1.0, tk.END)

            with open(self.file_path, 'r') as self.file:
                self.text = self.file.read()
                self.text_edit.insert(tk.END, self.text)

            title = self.file_path.split('/')[-1]    
            self.root.title(title)


    def save_file(self):
        '''This method allows to save the current document without changin name and location.'''
        if not self.file_path:
            self.save_file_as()
        else:
            with open(self.file_path, "w") as self.file:
                self.file.write(self.text_edit.get("1.0", tk.END)) 
            # closing editor window automatically after the file has been saved
            self.root.destroy() 


    def save_file_as(self):
        '''This method allows to save the current document with a new name or location.'''

        file_path = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(self.file_path, "w") as self.file:
                self.file.write(self.text_edit.get("1.0", tk.END)) 

    def exit(self):
        self.root.destroy()

 
    def change_font(self, fontt):
        '''This method changes text's font and/or size based on user's selection in dropdown menu.'''
        changed_font = ((self.font_var.get(), int(self.size_var.get())))
        self.text_edit.configure(font=changed_font)


    def copy_text(self, event):
        '''This method copies the selected text in editor window either via button or shortcut 'Ctrl+c'.'''
        self.selected_text = ''
        if event:
            self.selected_text = self.root.clipboard_get()

        if self.text_edit.selection_get():
            # 'taking' selected text from editor window
            self.selected_text = self.text_edit.selection_get()
            # making sure the clipboard is empty 
            self.root.clipboard_clear()
            # setting the clipboard value to selected value
            self.root.clipboard_append(self.selected_text)

        # Bind 'Control+c" to copy_text method
        self.root.bind('<Control-Key-c>', self.copy_text)


    def cut_text(self, event):
        '''This method cuts the selected text in editor window either via button or shortcut 'Ctrl+x'.'''
        self.selected_text = ''
        if event:
            self.selected_text = self.root.clipboard_get()
        else:
            if self.text_edit.selection_get():
                # 'taking' selected text from editor window
                self.selected_text = self.text_edit.selection_get() 
                # delete selected text from the document
                self.text_edit.delete('sel.first', 'sel.last')
                self.root.clipboard_clear()
                self.root.clipboard_append(self.selected_text)

        # Bind 'Control+x" to cut_text method
        self.root.bind('<Control-Key-x>', self.copy_text)
        

    def paste_text(self, event):
        '''This method pastes the cutted/copied text in desired position either via button or 'Ctrl+v.'''
        # taking cursor's position
        if event:
            self.selected_text = self.root.clipboard_get()
        else:
            if self.selected_text:
                pos = self.text_edit.index(tk.INSERT)
                self.text_edit.insert(pos, self.selected_text)

        # Bind 'Control+v" to paste_text method
        self.root.bind('<Control-Key-x>', self.copy_text)