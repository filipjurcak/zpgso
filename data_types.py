from math import sqrt


class Mat:
    @staticmethod
    def multiply_mat_with_vec(mat: 'Mat4', vec: 'Vec4') -> 'Vec4':
        vec_list = [vec.x, vec.y, vec.z, vec.v]
        res = [sum([a * b for a, b in zip(vec_list, mat.matrix[i])]) for i in range(4)]
        return Vec4(res[0], res[1], res[2], res[3])


class Vec4(Mat):
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
            return self.multiply_mat_with_vec(other, self)

    # substraction of points creates a vector
    def __sub__(self, other: 'Vec4'):
        return Vec4(self.x - other.x, self.y - other.y, self.z - other.z, 0)

    def __add__(self, other: 'Vec4'):
        # min here is to prevent value of v to be 2 when adding two points for computing centroids
        return Vec4(self.x + other.x, self.y + other.y, self.z + other.z, min(self.v + other.v, 1))

    def __truediv__(self, divisor: float):
        assert divisor != 0
        return Vec4(self.x / divisor, self.y / divisor, self.z / divisor, self.v)

    def cross(self, other: 'Vec4'):
        cx = (self.y * other.z) - (self.z * other.y)
        cy = (self.z * other.x) - (self.x * other.z)
        cz = (self.x * other.y) - (self.y * other.x)
        return Vec4(cx, cy, cz, 0)

    def dot(self, other: 'Vec4'):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    # normalizes vector, vector has v == 0
    def normalize(self):
        assert self.v == 0
        norm = sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))
        return self / norm

    def __str__(self):
        # better formatting for debugging
        return "{} {} {} {}".format(self.x, self.y, self.z, self.v)


class Mat4(Mat):
    def __init__(self, matrix):
        assert len(matrix) == 4 and len(matrix[0]) == 4
        self.matrix = matrix

    def __mul__(self, other):
        assert isinstance(other, Vec4) or isinstance(other, Mat4)
        if isinstance(other, Vec4):
            return self.multiply_mat_with_vec(self, other)
        elif isinstance(other, Mat4):
            transposed = [[other.matrix[j][i] for j in range(len(other.matrix))] for i in range(len(other.matrix[0]))]
            res = [[sum([a * b for a, b in zip(self.matrix[i], transposed[j])]) for j in range(4)] for i in range(4)]
            return Mat4(res)

    def __str__(self):
        # better formatting for debugging
        return "\n".join([str(row) for row in self.matrix])


class Triangle:
    def __init__(self, vertex1: int, vertex2: int, vertex3: int):
        self.vertex1: int = vertex1
        self.vertex2: int = vertex2
        self.vertex3: int = vertex3
