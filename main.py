from IndexedFace import IndexedFace
from tkinter import Tk, Canvas, filedialog, Label, Entry, StringVar
from tkinter import ttk
from data_types import Mat4, Vec4, Triangle
from math import sin, cos


class Main:
    def __init__(self):
        self.width = 1000
        self.height = 800
        self.scale_image = 200
        self.lines_ids = []
        self.indexed_face = IndexedFace()
        self.tk = Tk()
        self.tk.title("ZPGSO CG")
        self.canvas = Canvas(self.tk, width=self.width, height=self.height)
        self.canvas.pack()
        self.tk.resizable(width=False, height=False)
        self.canvas.create_rectangle(self.width - (self.width - self.height), 0, self.width, self.height, fill='grey')
        self.translate_x_entry = Entry(self.canvas, width=10, bd=0, textvariable=StringVar(self.tk, value='0.0'))
        self.translate_x_entry.place(x=850, y=125)
        self.translate_y_entry = Entry(self.canvas, width=10, bd=0, textvariable=StringVar(self.tk, value='0.0'))
        self.translate_y_entry.place(x=850, y=150)
        self.translate_z_entry = Entry(self.canvas, width=10, bd=0, textvariable=StringVar(self.tk, value='0.0'))
        self.translate_z_entry.place(x=850, y=175)
        self.rotate_x_entry = Entry(self.canvas, width=10, bd=0, textvariable=StringVar(self.tk, value='0.0'))
        self.rotate_x_entry.place(x=850, y=250)
        self.rotate_y_entry = Entry(self.canvas, width=10, bd=0, textvariable=StringVar(self.tk, value='0.0'))
        self.rotate_y_entry.place(x=850, y=275)
        self.rotate_z_entry = Entry(self.canvas, width=10, bd=0, textvariable=StringVar(self.tk, value='0.0'))
        self.rotate_z_entry.place(x=850, y=300)
        self.scale_entry = Entry(self.canvas, width=10, bd=0, textvariable=StringVar(self.tk, value='0.0'))
        self.scale_entry.place(x=825, y=375)

        rotation_z = Mat4(
            [
                [-1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )
        scaling1 = Mat4([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        translation = Mat4([[1, 0, 0, 2], [0, 1, 0, 2], [0, 0, 1, 2], [0, 0, 0, 1]])
        scaling2 = Mat4(
            [
                [self.scale_image, 0, 0, 0],
                [0, self.scale_image, 0, 0],
                [0, 0, self.scale_image, 0],
                [0, 0, 0, 1]
            ]
        )
        self.projection_matrix = scaling2 * translation * scaling1 * rotation_z
        self.original_model_matrix = Mat4([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.model_matrix = Mat4([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    def load_file(self):
        self.indexed_face.reset()
        file_path = filedialog.askopenfilename()
        if file_path != '':
            self.reset()
            with open(file_path) as f:
                for line in f:
                    splitted = line.split()
                    if len(splitted) > 0 and splitted[0] in ["#", "o", "s"]:
                        continue
                    if len(splitted) != 4:
                        print("Data not correctly formatted")
                        break
                    if splitted[0] == "v":
                        vec = Vec4(float(splitted[1]), float(splitted[2]), float(splitted[3]), 1)
                        self.indexed_face.add_vertex(vec)
                    elif splitted[0] == "f":
                        triangle = Triangle(int(splitted[1]), int(splitted[2]), int(splitted[3]))
                        self.indexed_face.add_vertex_index(triangle)
                        self.draw_triangle(triangle)

    def draw_triangle(self, triangle: Triangle):
        vec1 = self.projection_matrix * self.model_matrix * self.indexed_face.vertices[triangle.vertex1 - 1]
        vec2 = self.projection_matrix * self.model_matrix * self.indexed_face.vertices[triangle.vertex2 - 1]
        vec3 = self.projection_matrix * self.model_matrix * self.indexed_face.vertices[triangle.vertex3 - 1]
        line_ids = [
            self.canvas.create_line(vec1.x, vec1.y, vec2.x, vec2.y),
            self.canvas.create_line(vec1.x, vec1.y, vec3.x, vec3.y),
            self.canvas.create_line(vec2.x, vec2.y, vec3.x, vec3.y)
        ]
        for line in line_ids:
            self.canvas.tag_lower(line)  # because later drawn objects get higher priority and then collide with sidebar
            self.lines_ids.append(line)

    def redraw(self):
        for line_id in self.lines_ids:
            self.canvas.delete(line_id)
        self.lines_ids = []
        for triangle in self.indexed_face.vertex_indices:
            self.draw_triangle(triangle)

    def reset(self):
        self.model_matrix = Mat4(self.original_model_matrix.matrix)
        self.redraw()

    def add_translate(self):
        translate_x = float(self.translate_x_entry.get())
        translate_y = -float(self.translate_y_entry.get())  # this is because tkinter y axis is upside down
        translate_z = float(self.translate_z_entry.get())
        translate_matrix = Mat4([[1, 0, 0, translate_x], [0, 1, 0, translate_y], [0, 0, 1, translate_z], [0, 0, 0, 1]])
        self.model_matrix = translate_matrix * self.model_matrix
        self.redraw()

    def add_rotate(self):
        rotate_x = float(self.rotate_x_entry.get())
        rotate_y = float(self.rotate_y_entry.get())
        rotate_z = float(self.rotate_z_entry.get())
        rotate_x_matrix = Mat4([
            [1, 0, 0, 0],
            [0, cos(rotate_x), -sin(rotate_x), 0],
            [0, sin(rotate_x), cos(rotate_x), 0],
            [0, 0, 0, 1]])
        rotate_y_matrix = Mat4([
            [cos(rotate_y), 0, sin(rotate_y), 0],
            [0, 1, 0, 0],
            [-sin(rotate_y), 0, cos(rotate_y), 0],
            [0, 0, 0, 1]])
        rotate_z_matrix = Mat4([
            [cos(rotate_z), -sin(rotate_z), 0, 0],
            [sin(rotate_z), cos(rotate_z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        self.model_matrix = rotate_x_matrix * rotate_y_matrix * rotate_z_matrix * self.model_matrix
        self.redraw()

    def add_scale(self):
        scale = float(self.scale_entry.get())
        scaling_matrix = Mat4([[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, scale, 0], [0, 0, 0, 1]])
        self.model_matrix = scaling_matrix * self.model_matrix
        self.redraw()

    def start(self):
        load_button = ttk.Button(self.canvas, text="Load", command=self.load_file)
        load_button.place(x=825, y=25)

        reset = ttk.Button(self.canvas, text="Reset", command=self.reset)
        reset.place(x=825, y=75)

        translate_x_label = Label(self.canvas, text="X:")
        translate_x_label.place(x=825, y=125)

        translate_y_label = Label(self.canvas, text="Y:")
        translate_y_label.place(x=825, y=150)

        translate_z_label = Label(self.canvas, text="Z:")
        translate_z_label.place(x=825, y=175)

        translate_button = ttk.Button(self.canvas, text="Translate", command=self.add_translate)
        translate_button.place(x=825, y=200)

        rotate_x_label = Label(self.canvas, text="X:")
        rotate_x_label.place(x=825, y=250)

        rotate_y_label = Label(self.canvas, text="Y:")
        rotate_y_label.place(x=825, y=275)

        rotate_z_label = Label(self.canvas, text="Z:")
        rotate_z_label.place(x=825, y=300)

        rotate_button = ttk.Button(self.canvas, text="Rotate", command=self.add_rotate)
        rotate_button.place(x=825, y=325)

        scale_button = ttk.Button(self.canvas, text="Scale", command=self.add_scale)
        scale_button.place(x=825, y=400)

        quit_button = ttk.Button(self.canvas, text="Quit", command=quit)
        quit_button.place(x=825, y=450)

        self.tk.mainloop()


if __name__ == '__main__':
    Main().start()
