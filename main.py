from IndexedFace import IndexedFace
from tkinter import Tk, Canvas, filedialog, Label, Entry
from tkinter import ttk
from data_types import Mat4, Vec4
import math


class Main:
    def __init__(self):
        self.width = 1000
        self.height = 800
        self.scale_image = 200
        self.lines_ids = []
        self.indexed_face = IndexedFace()
        self.tk = Tk()
        self.tk.title("ZPGSO CG Stage 1")
        self.canvas = Canvas(self.tk, width=self.width, height=self.height)
        self.canvas.pack()
        self.tk.resizable(width=False, height=False)
        self.canvas.create_rectangle(self.width - 200, 0, self.width, self.height, fill='grey')
        self.translate_x_entry = Entry(self.canvas, width=10, bd=0)
        self.translate_x_entry.place(x=850, y=125)
        self.translate_y_entry = Entry(self.canvas, width=10, bd=0)
        self.translate_y_entry.place(x=850, y=150)
        self.translate_z_entry = Entry(self.canvas, width=10, bd=0)
        self.translate_z_entry.place(x=850, y=175)
        self.rotate_x_entry = Entry(self.canvas, width=10, bd=0)
        self.rotate_x_entry.place(x=850, y=250)
        self.rotate_y_entry = Entry(self.canvas, width=10, bd=0)
        self.rotate_y_entry.place(x=850, y=275)
        self.rotate_z_entry = Entry(self.canvas, width=10, bd=0)
        self.rotate_z_entry.place(x=850, y=300)
        self.scale_entry = Entry(self.canvas, width=10, bd=0)
        self.scale_entry.place(x=825, y=375)

    def load_file(self):
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
                        # TODO review if this couldn't be made with less transformations
                        rotation_z = Mat4(
                            [
                                [math.cos(math.pi), -math.sin(math.pi), 0, 0],
                                [math.sin(math.pi), math.cos(math.pi), 0, 0],
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
                        vec = Vec4(float(splitted[1]), float(splitted[2]), float(splitted[3]), 1)
                        self.indexed_face.add_vertex(scaling2 * (translation * (scaling1 * (rotation_z * vec))))
                    elif splitted[0] == "f":
                        self.indexed_face.add_vertex_index((int(splitted[1]), int(splitted[2]), int(splitted[3])))
                        vec1 = self.indexed_face.vertices[int(splitted[1]) - 1]
                        vec2 = self.indexed_face.vertices[int(splitted[2]) - 1]
                        vec3 = self.indexed_face.vertices[int(splitted[3]) - 1]
                        self.lines_ids.append(self.canvas.create_line(vec1.x, vec1.y, vec2.x, vec2.y))
                        self.lines_ids.append(self.canvas.create_line(vec1.x, vec1.y, vec3.x, vec3.y))
                        self.lines_ids.append(self.canvas.create_line(vec2.x, vec2.y, vec3.x, vec3.y))

    def reset(self):
        for to_remove in self.lines_ids:
            self.canvas.delete(to_remove)
        self.lines_ids = []
        self.indexed_face.remove_vertices()
        self.indexed_face.remove_vertex_index()

    def reset_transformations(self):
        pass

    def add_translate(self):
        x = float(self.translate_x_entry.get())
        y = float(self.translate_y_entry.get())
        z = float(self.translate_z_entry.get())


    def add_rotate(self):
        pass

    def add_scale(self):
        scale = float(self.scale_entry.get())
        scaling_matrix = Mat4([[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, scale, 0], [0, 0, 0, 1]])
        for i in range(len(self.indexed_face.vertices)):
            self.indexed_face.vertices[i] = scaling_matrix * self.indexed_face.vertices[i]
        # for i in range(len(self.indexed_face.vertex_indices)):
        #     v1, v2, v3 = self.indexed_face.vertex_indices[i]
        #     line_id1 = self.lines_ids[i]
        #     line_id2 = self.lines_ids[i + 1]
        #     line_id3 = self.lines_ids[i + 2]
        #     vec1 = self.indexed_face.vertices[v1 - 1]
        #     vec2 = self.indexed_face.vertices[v2 - 1]
        #     vec3 = self.indexed_face.vertices[v3 - 1]
        #     self.canvas.coords(line_id1, [vec1.x, vec1.y, vec2.x, vec2.y])
        #     self.canvas.coords(line_id2, [vec1.x, vec1.y, vec3.x, vec3.y])
        #     self.canvas.coords(line_id3, [vec2.x, vec2.y, vec3.x, vec3.y])


        for to_remove in self.lines_ids:
            self.canvas.delete(to_remove)
        self.lines_ids = []
        for vertex_indices in self.indexed_face.vertex_indices:
            vec1 = self.indexed_face.vertices[vertex_indices[0] - 1]
            vec2 = self.indexed_face.vertices[vertex_indices[1] - 1]
            vec3 = self.indexed_face.vertices[vertex_indices[2] - 1]
            self.lines_ids.append(self.canvas.create_line(vec1.x, vec1.y, vec2.x, vec2.y))
            self.lines_ids.append(self.canvas.create_line(vec1.x, vec1.y, vec3.x, vec3.y))
            self.lines_ids.append(self.canvas.create_line(vec2.x, vec2.y, vec3.x, vec3.y))

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

        translate_button = ttk.Button(self.canvas, text="Translate", command=self.add_translate )
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
