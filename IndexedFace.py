from data_types import Vec4, Triangle


class IndexedFace:
    def __init__(self):
        self.vertices = []
        self.vertex_indices = []

    def add_vertex(self, vertex: Vec4):
        self.vertices.append(vertex)

    def add_vertex_index(self, vertex_index: Triangle):
        self.vertex_indices.append(vertex_index)

    def reset(self):
        self.vertices = []
        self.vertex_indices = []
