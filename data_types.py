class Vec4:
    def __init__(self, x, y, z, v):
        self.x = x
        self.y = y
        self.z = z
        self.v = v

    def __mul__(self, other):
        assert isinstance(other, Vec4) or isinstance(other, Mat4)
        if isinstance(other, Vec4):
            return Vec4(self.x * other.x, self.y * other.y, self.z * other.z, self.v * other.v)
        elif isinstance(other, Mat4):
            vec = [self.x, self.y, self.z, self.v]
            res = [sum([a * b for a, b in zip(vec, other.matrix[i])]) for i in range(4)]
            return Vec4(res[0], res[1], res[2], res[3])


class Mat4:
    def __init__(self, matrix):
        assert len(matrix) == 4 and len(matrix[0]) == 4
        self.matrix = matrix

    def __mul__(self, other):
        assert isinstance(other, Vec4) or isinstance(other, Mat4)
        if isinstance(other, Vec4):
            vec = [other.x, other.y, other.z, other.v]
            res = [sum([a * b for a, b in zip(vec, self.matrix[i])]) for i in range(4)]
            return Vec4(res[0], res[1], res[2], res[3])
        elif isinstance(other, Mat4):
            res = [[0]*4 for _ in range(4)]
            transposed = [[other.matrix[j][i] for j in range(len(other.matrix))] for i in range(len(other.matrix[0]))]
            # TODO possible optimization
            for i in range(4):
                for j in range(4):
                    res[i][j] = sum([a * b for a, b in zip(self.matrix[i], transposed[j])])

            return res
