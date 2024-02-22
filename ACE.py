import tkinter as tk
from tkinter import simpledialog, messagebox
import csv

class Quotation:
    def __init__(self, filepath):
        self.text = self.read_quotation(filepath)
        # Initialize used_positions list based on the length of the quotation text
        self.used_positions = [False] * len(self.text)

    def read_quotation(self, filepath):
        try:
            with open(filepath, 'r') as file:
                # Read the file content, convert to uppercase, and return the text
                return file.read().upper()
        except IOError as e:
            messagebox.showerror("Error", f"Failed to read quotation file: {e}")
            raise

    # Other methods and functionality of the Quotation class...


class LetterPool:
    def __init__(self, quotation):
        self.letters = self.populate_from_quotation(quotation)

    def populate_from_quotation(self, quotation):
        return [{'character': char, 'used': False} for char in quotation if char.isalpha()]

class ValidSolutions:
    def __init__(self, filepath):
        self.words = self.load_words(filepath)

    # The load_words method remains the same...
    def load_words(self, filepath):
        try:
            with open(filepath, newline='') as csvfile:
                reader = csv.reader(csvfile)
                # Create and return a list of dictionaries, each containing a word and a used/unused flag
                return [{'word': row[0].upper(), 'used': False} for row in reader if row]  # Ensure the row is not empty
        except IOError as e:
            messagebox.showerror("Error", f"Failed to read valid solutions file: {e}")
            raise


    def get_next_unused_word_by_length(self, length, quotation):
        for word_info in self.words:
            if not word_info['used'] and len(word_info['word']) == length:
                letter_positions = self.check_and_mark_word(word_info['word'], quotation)
                
                if letter_positions:
                    # If the word can be fully formed, mark it as used and return the word with positions
                    word_info['used'] = True
                    return word_info['word'], letter_positions

        return None, None
    def check_and_mark_word(self, word, quotation):
        temp_used_positions = quotation.used_positions[:]  # Make a temporary copy of used positions
        letter_positions = []

        for letter in word:
            found = False
            for i, (q_letter, used) in enumerate(zip(quotation.text, temp_used_positions)):
                if letter == q_letter and not used:
                    temp_used_positions[i] = True  # Temporarily mark as used
                    letter_positions.append(i)  # Collect the position, already 0-based
                    found = True
                    break
            
            if not found:
                return None  # If any letter can't be matched, return None

        # If all letters can be matched, update the actual used positions in the quotation
        quotation.used_positions = temp_used_positions
        return letter_positions

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        # self.cells = [['' for _ in range(columns)] for _ in range(rows)]
        self.cells = [[{'letter': '', 'number': None, 'bg_color': 'white'} for _ in range(columns)] for _ in range(rows)]
    def populate_from_quotation(self, quotation):
        cell_number = 1
        for i, char in enumerate(quotation.text):
            row = i // self.columns
            col = i % self.columns
            # Skip processing if indices are out of grid bounds
            if row >= self.rows or col >= self.columns:
                break

            if char.isalpha():  # Include only alphabetic characters in the grid
                self.cells[row][col]['letter'] = char
                self.cells[row][col]['number'] = cell_number
                cell_number += 1
class Clue:
    def __init__(self, label, text):
        self.label = label
        self.text = text
        self.answer = None  # To be filled with the verified answer

class ClueList:
    def __init__(self):
        self.clues = []
    
    def delete_clue(self, label):
        self.clues = [clue for clue in self.clues if clue.label != label]
        

class ApplicationForm(tk.Tk):
    # Other parts of the class...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Acrostic Puzzle Creator")

        # Set the size of the form
        self.geometry("800x600")  # Adjust the size as needed

        # Initialize the Quotation object
        self.quotation = Quotation("C:/Users/danin/answer.txt")

        # Create the valid_solutions object.
        # Its nitialization method will cause the entire valid_solutions list
        # to be loaded into its class variable so it can be accessed by other
        # methods in the Validsolutions class.                         
        self.validsolutions = ValidSolutions("C:/Users/danin/valid_solutions.csv")
        print(self.validsolutions.get_next_unused_word_by_length(5,self.quotation))
        
        # Prompt for grid dimensions and initialize the Grid
        self.initialize_grid()
        
        # Add the grid to the form
        self.add_grid_to_form()

         # Variable to control the display of quotation letters in the grid
        self.display_quote_var = tk.StringVar(value="On")

        # Add the 'Display quote' button to the form
        # self.add_display_quote_button()

        # Update the grid based on the initial display state ('On')
        self.update_grid_display()

        # Initialize a variable to keep track of the current clue label index
        self.current_clue_label_index = 0

        # Initialize the clue_answer_label for displaying clue answers
        self.clue_answer_label = tk.Label(self, text="")
        self.clue_answer_label.pack(side="bottom", pady=10)  # Adjust the placement as needed

        # Add the first clue to the form
        self.add_first_clue()

        # Initialize other components...
        self.setup_ui()

    def setup_ui(self):
        # Frame to hold the buttons
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side="bottom", pady=10)

        # Existing button (e.g., 'Display Quote')
        self.display_quote_btn = tk.Button(self.buttons_frame, text="Display Quote", relief=tk.RAISED)
        self.display_quote_btn.menu = tk.Menu(self.display_quote_btn, tearoff=0)
        #self.display_quote_btn['menu'] = self.display_quote_btn.menu
        self.display_quote_btn.menu.add_radiobutton(label='On', variable=self.display_quote_var, value='On', command=self.update_grid_display)
        self.display_quote_btn.menu.add_radiobutton(label='Off', variable=self.display_quote_var, value='Off', command=self.update_grid_display)
        self.display_quote_btn.pack(side="left", padx=5)

        # 'Submit Clue' button
        self.submit_clue_button = tk.Button(self.buttons_frame, text="Submit Clue", command=self.submit_clue)
        self.submit_clue_button.pack(side="left", padx=5)

    
    def submit_clue(self):
        # Placeholder for the submit clue logic, to be defined
        pass


        
    def add_first_clue(self):
        # Ensure the clues_frame exists to hold the clues
        if not hasattr(self, 'clues_frame'):
            self.clues_frame = tk.Frame(self)
            self.clues_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Create the clue label (e.g., "A.")
        clue_label = tk.Label(self.clues_frame, text="A.")
        clue_label.pack(anchor="nw")

        # Create or update the clue text entry
        if not hasattr(self, 'clue_text_entry'):
            self.clue_text_entry = tk.Entry(self.clues_frame, width=50)  # Adjust width as needed
            self.clue_text_entry.pack(anchor="nw", pady=5)  # Padding for spacing between elements

        # Set the focus to the clue text entry
        self.clue_text_entry.focus_set()

        # Get a five-letter word from ValidSolutions and its positions in the quotation
        five_letter_word, letter_positions = self.validsolutions.get_next_unused_word_by_length(5, self.quotation)

        # Format the position numbers for display, adjusting for 1-based indexing
        position_numbers_text = ', '.join(str(pos + 1) for pos in letter_positions)

        # Construct the text for the clue answer, including the word and its position numbers
        clue_answer_text = f"Answer: {five_letter_word} (Positions: {position_numbers_text})"

        # Create or update the clue answer label
        if hasattr(self, 'clue_answer_label'):
            self.clue_answer_label.config(text=clue_answer_text)
        else:
            self.clue_answer_label = tk.Label(self.clues_frame, text=clue_answer_text)
            self.clue_answer_label.pack(anchor="nw", pady=(5, 0))  # Padding above the label for spacing

        # Set the background color of cells containing the clue answer to pale yellow
        for pos in letter_positions:
            row = (pos - 1) // self.grid.columns
            col = (pos - 1) % self.grid.columns

            # Ensure the position is within the grid bounds
            if 0 <= row < self.grid.rows and 0 <= col < self.grid.columns:
                # Get the label widget for the cell at the specified position
                cell_label = self.grid_frame.grid_slaves(row=row, column=col)[0]

                # Set the background color of the label to pale yellow
                cell_label.config(bg='pale goldenrod')

    
    def add_grid_to_form(self):
        # Create a frame for the grid
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(side="top", anchor="ne", padx=20, pady=20)  # Adjust positioning as needed

        # Define cell size and font
        cell_width = 4  # Set cell width to 4
        cell_height = 4 # Set cell height to 4
        cell_font = ('Arial', 8)  # Set font size to 8

        # Initialize cell number
        cell_number = 1

        # Iterate over the rows and columns in the grid
        for row in range(self.grid.rows):
            for col in range(self.grid.columns):
                # Determine the position in the quotation text
                pos = row * self.grid.columns + col
                # Check if the position exceeds the length of the quotation text
                if pos >= len(self.quotation.text):
                    break

                char = self.quotation.text[pos]
                
                if char.isalpha():
                    # Place the cell number in the upper left and the letter in the lower half of the cell
                    cell_text = f"{cell_number}\n\n {char}"
                    cell_number += 1
                    cell_bg = "white"
                elif char == ' ':
                    cell_text = '   '  # Represent spaces as empty
                    cell_bg = "#808080"  # Dark gray background for spaces
                else:
                    cell_text = '   '  # Optionally, represent other characters differently
                    cell_bg = "white"

                # Create a label for the cell with specified background color and alignment
                label = tk.Label(self.grid_frame, text=cell_text, width=cell_width, height=cell_height,
                                 borderwidth=1, relief="solid", font=cell_font, bg=cell_bg,
                                 anchor='center', justify='left')  # Align text to the northwest (upper left)
                label.grid(row=row, column=col, padx=1, pady=1)


    def initialize_grid(self):
        # Prompt the user for the number of rows and columns
        rows = self.prompt_for_dimension("Number of Rows")
        columns = self.prompt_for_dimension("Number of Columns")

        # Instantiate the Grid object
        self.grid = Grid(rows, columns)

        # Populate the grid with the quotation text
        self.grid.populate_from_quotation(self.quotation)

    def prompt_for_dimension(self, prompt_title):
        while True:
            try:
                value = simpledialog.askinteger("Input", f"Enter {prompt_title}:", parent=self)
                if value is not None and value > 0:
                    return value
                else:
                    messagebox.showwarning("Invalid Input", f"Please enter a positive integer for {prompt_title}.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a positive integer.")

    def update_grid_display(self):
    # Update the grid display based on the 'Display quote' toggle state
        for row in range(self.grid.rows):
            for col in range(self.grid.columns):
                # Check if there are any widgets (labels) at the specified grid position
                grid_slaves = self.grid_frame.grid_slaves(row=row, column=col)
                if grid_slaves:  # If there's at least one widget, proceed
                    label = grid_slaves[0]  # Get the first widget, which should be the label for this cell

                    # Determine the position in the quotation text
                    pos = row * self.grid.columns + col
                    if pos < len(self.quotation.text):
                        char = self.quotation.text[pos]
                        cell_number_text = f"{pos + 1}"  # Cell number text based on position
                        
                        if char.isalpha():
                            # If the toggle is 'On', display the letter in the lower half; otherwise, leave it blank
                            cell_letter_text = f"{char}" if self.display_quote_var.get() == 'On' else " "
                            # Combine cell number and letter based on toggle state
                            label_text = f"{cell_number_text}\n\n{cell_letter_text}"
                        elif char == ' ':
                            # For spaces, display a blank or darkened cell without altering the cell number
                            label_text = f"{cell_number_text}\n\n " if self.display_quote_var.get() == 'On' else f"{cell_number_text}"
                        else:
                            # Optionally handle other characters (e.g., punctuation)
                            label_text = f"{cell_number_text}\n\n{char}" if self.display_quote_var.get() == 'On' else f"{cell_number_text}"
                    else:
                        label_text = ''

                    # Update the label text
                    label.config(text=label_text)
     
    
# Running the application
if __name__ == "__main__":
    app = ApplicationForm()
    app.mainloop()

      
