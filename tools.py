from tkinter.simpledialog import askstring
import tkinter as tk

def window(strings, window_title, add_button, button_width=50):
    def newline(input_string, wrap_length=button_width):
        words = input_string.split()
        lines = []
        line = []
        line_length = 0
        for word in words:
            if line_length + len(word) + 1 <= wrap_length:
                line.append(word)
                line_length += len(word) + 1
            else:
                lines.append(' '.join(line))
                line = [word]
                line_length = len(word)
        if line:
            lines.append(' '.join(line))
        result_string = '\n'.join(lines)
        return result_string

    def save_position(index):
        nonlocal selected_position
        selected_position = index
        root.destroy()

    def right_click_menu(event, index, button):
        context_menu = tk.Menu(root, tearoff=0)
        context_menu.add_command(label="Edit Text", command=lambda i=index, b=button: edit_text(i, b))
        context_menu.post(event.x_root, event.y_root)

    def edit_text(index, button):
        current_text = button.cget("text")
        new_text = askstring("Edit Text", "Edit the text for the button:", initialvalue=current_text)
        if new_text is not None:
            new_definitions[index] = new_text  # Store the new text in the dictionary
            button.config(text=newline(new_text))
    
    selected_position = None
    new_definitions = {}  # Dictionary to store new definitions for buttons

    root = tk.Tk()
    root.title(window_title)
    root.geometry(f'{button_width*10}x270')

    frame = tk.Frame(root)
    frame.pack()

    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar = tk.Scrollbar(frame, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    frame_buttons = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_buttons, anchor="nw")

    buttons = []
    for index, string in enumerate(strings):
        button = tk.Button(frame_buttons, text=newline(string, wrap_length=button_width), command=lambda i=index: save_position(i))
        button.pack(fill=tk.X)
        button.bind("<Button-3>", lambda event, i=index, b=button: right_click_menu(event, i, b))
        buttons.append(button)
    
    if add_button:
        #adding button for typing your own
        index+=1
        button = tk.Button(frame_buttons, text="Right click to add yours", command=lambda i=index: save_position(i))
        button.pack(fill=tk.X)
        button.bind("<Button-3>", lambda event, i=index, b=button: right_click_menu(event, i, b))
        buttons.append(button)

    frame_buttons.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()

    if new_definitions:
        new_definitions = new_definitions[selected_position].replace("\n","")
        return selected_position, new_definitions
    else:  
        return selected_position, False