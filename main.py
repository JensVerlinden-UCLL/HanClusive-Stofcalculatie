import tkinter as tk
from tkinter import ttk

def rectangle_fill(free_width, rectangles, max_height, second_height):

    fitting_rectangles = [i for i in rectangles if (i[0] <= free_width or i[1] <= free_width)]
    
    counter = 0
    while len(fitting_rectangles) != 0: 
        solution = fitting_rectangles[counter]
        solution_check_diff = min(i for i  in [free_width - solution[0], free_width - solution[1]] if i >= 0)
        solution_width = free_width - solution_check_diff
        solution_height = solution[0] if solution_width == solution[1] else solution[1]
        if solution_height - max_height > solution_width:
            fitting_rectangles.remove(solution)
            counter += 1
            continue

        for rectangle_check in fitting_rectangles:
            rectangle_check_diff = min(i for i  in [free_width - rectangle_check[0], free_width - rectangle_check[1]] if i >= 0)
            check_width = free_width - rectangle_check_diff
            check_height = rectangle_check[0] if check_width == solution[1] else rectangle_check[1]

            if rectangle_check_diff < solution_check_diff and check_height - max_height <= check_width:
                solution = rectangle_check
                solution_check_diff = rectangle_check_diff
                solution_width = check_width
                solution_height = check_height

            elif rectangle_check_diff == solution_check_diff:
                if ((solution_height > second_height and check_height - solution_height < solution_height) or (solution_height < second_height and check_height - solution_height > solution_height)) and check_height - max_height <= check_width:
                    solution = rectangle_check
                    check_width = rectangle_check_diff
                    solution_height = check_height
                
        return (solution, solution_width, solution_height)
    
    return

def calculate_next_free_width(widths):
    
    widths.sort(key = lambda x: x[1])
    width_with_lowest_height = min(widths, key = lambda x: x[0])
    index_width_with_lowest_height = widths.index(width_with_lowest_height)
    max_height = max(widths, key = lambda x: x[0])[0]
    widths_by_height = sorted(widths, key = lambda x: x[0])
    try:
        second_min_height = widths_by_height[1][0] 
    except:
        second_min_height = 999999
    
    return width_with_lowest_height, index_width_with_lowest_height, max_height, second_min_height


def positioning_algorithm(roll_width, rectangles):

    first_rectangle, first_rectangle_width, first_rectangle_height = rectangle_fill(roll_width, rectangles, 99999999, 99999999)

    resultaten = [((0, 0), (first_rectangle_width, first_rectangle_height))]

    widths = [(first_rectangle_height, 0, first_rectangle_width)]

    if first_rectangle_width != roll_width:
        widths.append((0, first_rectangle_width, roll_width))

    rectangles.remove(first_rectangle)

    while len(rectangles) != 0:

        current_width, index_current_width, max_height, second_height = calculate_next_free_width(widths)

        fitting_rectangle = rectangle_fill(current_width[2] - current_width[1], rectangles, max_height, second_height)

        if fitting_rectangle:

            widths.append((current_width[0] + fitting_rectangle[2], current_width[1], current_width[1] + fitting_rectangle[1]))

            if fitting_rectangle[1] != current_width[2] - current_width [1]:
                widths.append((current_width[0], current_width[1] + fitting_rectangle[1], current_width[2]))
            
            widths.remove(current_width)

            resultaten.append(((current_width[1], current_width[0]), (current_width[1] + fitting_rectangle[1], current_width[0] + fitting_rectangle[2])))

            rectangles.remove(fitting_rectangle[0])

        else:

            try:
                left_width = widths[index_current_width - 1][0]
            except IndexError:
                left_width = 69420

            try:
                right_width = widths[index_current_width + 1][0]
            except IndexError:
                right_width = 69420

            if left_width != right_width:
                lowest_neighbour = min(left_width, right_width)
                
                if lowest_neighbour == widths[index_current_width - 1][0]:
                    widths.append((widths[index_current_width - 1][0], widths[index_current_width - 1][1], current_width[2]))
                    widths.remove(widths[index_current_width - 1])
                    widths.remove(current_width)

                else:
                    widths.append((widths[index_current_width + 1][0], current_width[1], widths[index_current_width + 1][2]))
                    widths.remove(widths[index_current_width + 1])
                    widths.remove(current_width)

            else:

                widths.append((widths[index_current_width - 1][0], widths[index_current_width - 1][1], widths[index_current_width + 1][2]))
                widths.remove(widths[index_current_width - 1])
                widths.remove(current_width)
                widths.remove(widths[index_current_width + 1])

    return max(widths, key = lambda x: x[0])[0], resultaten

class RectangleStackVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HanClusive Stofcalculator")
        self.background = tk.PhotoImage(file = "./Hanclusive_background.ppm")
        self.geometry("500x400")
        self.minsize(600, 700)  # Set a minimum size for the window
        self.iconbitmap("./Hanclusive_Logo.ico")
        self.background_label = tk.Label(self, image=self.background, bg="#260000")
        self.background_label.place(relwidth=1, relheight=1)
        self.roll_width = None
        self.rectangles = []
        self.result = ''
        self.create_styles()
        self.create_widgets()
        self.bind('<Return>', lambda x: self.on_okay())

    def create_styles(self):
        dark_style = ttk.Style()
        dark_style.theme_use('clam')
        dark_style.configure('.', background='#570102', foreground='white')
        dark_style.configure('TLabel', background='#570102', foreground='white', font=('Helvetica', 14, 'bold', 'underline'))
        dark_style.configure('TButton', background='gray25', foreground='white', font=('Helvetica', 12, 'bold'))
        dark_style.configure('TEntry', background='white', foreground='black', font=('Helvetica', 12))
        dark_style.map('TEntry', foreground=[('readonly', 'black')])
        dark_style.configure('My.TEntry', background='grey25')

    def create_widgets(self):
        self.header_image = tk.PhotoImage(file="./Hanclusive_Logo.png")
        header_label = ttk.Label(self, image=self.header_image)
        header_label.pack(pady=10)

        self.label_roll = ttk.Label(self, text="BREEDTE VAN GEBRUIKTE ROL STOF (CM):")
        self.label_roll.pack(pady=(10, 5), padx=10)

        self.entry_roll = ttk.Spinbox(self, from_=0, to=1000, font=('Helvetica', 12), foreground="black")
        self.entry_roll.pack(pady=(5,10), padx=10)

        self.label_rectangles = ttk.Label(self, text="AFMETINGEN VAN GEWENSTE LAP STOF:")
        self.label_rectangles.pack(pady=(10, 5), padx=10)

        self.label_width = ttk.Label(self, text="HOOGTE (CM):", font=('Helvetica', 12, 'bold'))
        self.label_width.pack(pady=(5, 0), padx=10)

        self.entry_width = ttk.Spinbox(self, from_=0, to=1000, font=('Helvetica', 12), foreground="black")
        self.entry_width.pack(pady=(2, 10), padx=10)

        self.label_height = ttk.Label(self, text="BREEDTE (CM):", font=('Helvetica', 12, 'bold'))
        self.label_height.pack(pady=(5, 0), padx=10)

        self.entry_height = ttk.Spinbox(self, from_=0, to=1000, font=('Helvetica', 12), foreground="black")
        self.entry_height.pack(pady=(2, 10), padx=10)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        self.ok_button = ttk.Button(self.button_frame, text="NEXT", command=self.on_okay)
        self.ok_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(self.button_frame, text="STOP", command=self.on_cancel)
        self.stop_button.pack(side=tk.RIGHT, padx=5)

        self.output_text = tk.Text(self, wrap=tk.WORD, height=10, width=50, bg='#F7EDDB', font=('Helvetica bold', 15), borderwidth=7, highlightcolor="#CDCD9B", highlightbackground="#CDCD9B", relief='ridge')
        self.output_text.pack(pady=10)
        self.output_text.config(state="disabled")


    def on_okay(self):
        if self.roll_width is None:
            try:
                self.roll_width = round(float(self.entry_roll.get().replace(',', '.')), 2)
                self.entry_roll.config(foreground="firebrick4")
                self.entry_roll.config(state=tk.DISABLED)
                self.entry_width.focus_set()
            except ValueError:
                self.show_output("ONGELDIGE WAARDEN VOOR ROLBREEDTE!")
        try:
            width = round(float(self.entry_width.get().replace(',', '.')), 2)
            height = round(float(self.entry_height.get().replace(',', '.')), 2)
            if width > self.roll_width and height > self.roll_width:
                self.show_output("DIT LAP STOF KAN NIET MET DE OPGEGEVEN ROLBREEDTE IN 1 GEHEEL BEKOMEN WORDEN!")
            else:
                self.rectangles.append((width, height))
                self.entry_width.delete(0, tk.END)
                self.entry_height.delete(0, tk.END)
                self.show_output(f"LAP VAN {width} op {height} CM TOEGEVOEGD!")
        except ValueError:
            if self.entry_width.get() and self.entry_height.get():
                self.show_output("ONGELDIGE WAARDEN VOOR BREEDTE EN/OF HOOGTE!")
            else:
                self.show_output("GELIEVE WAARDES VOOR BREEDTE EN/OF HOOGTE OP TE GEVEN!")
                

    def on_cancel(self):
        self.on_okay()
        if app.roll_width is not None:
            if not len(app.rectangles):
                app.show_output("ER ZIJN GEEN LAPPEN STOF OPGEGEVEN!")
            else:
                if self.entry_width.get() or self.entry_height.get():
                    try:
                        width = round(float(self.entry_width.get().replace(',', '.')), 2)
                        height = round(float(self.entry_height.get().replace(',', '.')), 2)
                        if width > self.roll_width and height > self.roll_width:
                            self.show_output("DIT LAP STOF KAN NIET MET DE OPGEGEVEN ROLBREEDTE IN 1 GEHEEL BEKOMEN WORDEN!")
                        else:
                            self.rectangles.append((width, height))
                            self.entry_width.delete(0, tk.END)
                            self.entry_height.delete(0, tk.END)
                            self.show_output("")
                    except ValueError:
                        if width is None or height is None:
                            self.show_output("GELIEVE WAARDES VOOR BREEDTE EN/OF HOOGTE OP TE GEVEN!")
                        else:
                            self.show_output("ONGELDIGE WAARDEN VOOR BREEDTE EN/OF HOOGTE!")
            
                needed_height, output_rectangles = positioning_algorithm(self.roll_width, self.rectangles)
                self.result += f"OPGEGEVEN ROLBREEDTE:\n{round(self.roll_width, 2)} CM\n\nBENODIGDE STOFLENGTE:\n{round(needed_height, 2)} CM\n\n"

                for count, rectangle in enumerate(output_rectangles):
                    self.result += f"RECHTHOEK {count + 1}:\nAFMETINGEN: {round(rectangle[1][0] - rectangle[0][0], 2)} x {round(rectangle[1][1] - rectangle[0][1], 2)}\nLINKERONDERHOEK: ({round(rectangle[0][0], 2)}, {round(rectangle[0][1], 2)})\nRECHTERBOVENHOEK: ({round(rectangle[1][0], 2)}, {round(rectangle[1][1], 2)})\n\n"

                self.show_output(self.result)

            self.roll_width = None
            self.result = ''
            self.rectangles.clear()

            self.entry_roll.config(state="normal")
            self.entry_roll.config(foreground="black")
            self.entry_roll.delete(0, tk.END)

            self.entry_width.delete(0, tk.END)
            self.entry_width.config(state="normal")

            self.entry_height.delete(0, tk.END)
            self.entry_height.config(state="normal")

    def show_output(self, result):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result)
        self.output_text.config(state="disabled")

        start = "1.0"
        while start:
            start = self.output_text.search("RECHTHOEK", start, tk.END)
            if start:
                end = self.output_text.search("\n", start, tk.END)
                self.output_text.tag_add("bold", start, end)
                start = end
    
        start = "1.0"
        while start:
            start = self.output_text.search("TE:", start, tk.END)
            if start:
                end = self.output_text.search("\n\n", start, tk.END)
                self.output_text.tag_add("bold", str(f"{int(float(start))+1}" + ".0"), end)
                start = end

        start = "1.0"
        while start:
            start = self.output_text.search("N:", start, tk.END)
            if start:
                end = self.output_text.search("\n", start, tk.END)
                self.output_text.tag_add("bold", start.split('.')[0] + "." + str(int(start.split('.')[1])+3), end)
                start = end

        start = "1.0"
        while start:
            start = self.output_text.search("K:", start, tk.END)
            if start:
                end = self.output_text.search("\n", start, tk.END)
                self.output_text.tag_add("bold", start.split('.')[0] + "." + str(int(start.split('.')[1])+3), end)
                start = end

        self.output_text.tag_configure("bold", font=("Helvetica bold", 15, "bold"))

if __name__ == "__main__":
    app = RectangleStackVisualizer()
    app.mainloop()