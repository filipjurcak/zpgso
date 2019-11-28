from data_types import Vec4


class IndexedFace:
    def __init__(self):
        self.original_vertices = []
        self.vertices = []
        self.vertex_indices = []

    def add_vertex(self, vertex: Vec4):
        self.original_vertices.append(vertex)
        self.vertices.append(vertex)

    def remove_vertices(self):
        self.original_vertices = []
        self.vertices = []

    def add_vertex_index(self, vertex_index):
        self.vertex_indices.append(vertex_index)

    def remove_vertex_index(self):
        self.vertex_indices = []

    def reset(self):
        self.vertices = self.original_vertices
