class IndexedFace:
    def __init__(self):
        # self.original_vertices = []
        # self.original_vertex_indices = []
        self.vertices = []
        self.vertex_indices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def remove_vertices(self):
        self.vertices = []

    def add_vertex_index(self, vertex_index):
        self.vertex_indices.append(vertex_index)

    def remove_vertex_index(self):
        self.vertex_indices = []
