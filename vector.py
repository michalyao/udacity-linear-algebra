from math import acos, sqrt, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format([round(x, 3) for x in self.coordinates])

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        ret =  Decimal(sqrt(sum([coord ** 2 for coord in self.coordinates])))
        return ret

    def normalize(self):
        try:
            return self.times_scalar(Decimal('1.0')/self.magnitude())
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        return sum([x*y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalize()
            u2 = v.normalize()
            d = u1.dot(u2)
            angle_in_radians = acos(round(d,2))
            if in_degrees:
                degrees_per_radian = 180. / pi
                return degrees_per_radian * angle_in_radians
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with zero vector')
            else:
                raise e

    def is_parallel_to(self, v):
        return self.is_zero() or v.is_zero() or self.angle_with(v) in [0, pi]

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def component_orthogonal_to(self, basis):
        return self.minus(self.component_parallel_to(basis))

    def component_parallel_to(self, basis):
        try:
            u = basis.normalize()
            return u.times_scalar(self.dot(u))
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        self_coordinates = self.coordinates
        v_coordinates_ = v.coordinates
        if self.dimension == 2:
            self_coordinates = self.coordinates + ('0',)
        if v.dimension == 2:
            v_coordinates_ = v.coordinates + ('0',)

        x1, y1, z1 = self_coordinates
        x2, y2, z2 = v.coordinates
        return Vector([
            x1 * y2 - y1 * x2,
            y1 * z2 - z1 * y2,
            -(x1 * z2) - (z1 * x2)
        ])

    def area_of_parallelogram_with(self, v):
        return self.cross(v).magnitude()

    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance


if __name__ == '__main__':
    getcontext().prec = 30

    v = Vector([8.218, -9.341])
    w = Vector([-1.129, 2.111])
    addition = v.plus(w)
    print('addition: {}'.format(addition))

    v = Vector([7.119, 8.215])
    w = Vector([-8.223, 0.878])
    subtraction = v.minus(w)
    print('subtraction: {}'.format(subtraction))

    v = Vector([1.671, -1.012, -0.318])
    multiplication = v.times_scalar(7.41)
    print('multiplication: {}'.format(multiplication))

    # *****************

    v = Vector([-0.221, 7.437])
    first_magintude = v.magnitude()
    print('first_magintude: {}'.format(round(first_magintude, 3)))

    v = Vector([8.813, -1.331, -6.247])
    second_magintude = v.magnitude()
    print('second_magintude: {}'.format(round(second_magintude, 3)))

    v = Vector([5.581, -2.136])
    first_normalization = v.normalize()
    print('first_normailization: {}'.format(first_normalization))

    v = Vector([1.996, 3.108, -4.554])
    second_normalization = v.normalize()
    print('second_normailization: {}'.format(second_normalization))

    # *****************

    v = Vector([7.887, 4.138])
    w = Vector([-8.802, 6.776])
    dot_product = v.dot(w)
    print('first_dot_product: {}'.format(round(dot_product, 3)))

    v = Vector([-5.955, -4.904, -1.874])
    w = Vector([-4.496, -8.755, 7.103])
    dot_product = v.dot(w)
    print('second_dot_product: {}'.format(round(dot_product, 3)))

    # *****************

    v = Vector([3.183, -7.627])
    w = Vector([-2.668, 5.319])
    angle_rads = v.angle_with(w)
    print('first_angle_rads: {}'.format(angle_rads))

    v = Vector([7.35, 0.221, 5.188])
    w = Vector([2.751, 8.259, 3.985])
    angle_degrees = v.angle_with(w)
    print('first_angle_rads: {}'.format(angle_degrees))

    # *****************

    v = Vector([-7.579, -7.88])
    w = Vector([22.737, 23.64])
    is_parallel = v.is_parallel_to(w)
    is_orthogonal = v.is_orthogonal_to(w)

    print('1 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal))

    v = Vector([-2.029, 9.97, 4.172])
    w = Vector([-9.231, -6.639, -7.245])
    is_parallel = v.is_parallel_to(w)
    is_orthogonal = v.is_orthogonal_to(w)

    print('2 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal))

    v = Vector([-2.328, -7.284, -1.214])
    w = Vector([-1.821, 1.072, -2.94])
    is_parallel = v.is_parallel_to(w)
    is_orthogonal = v.is_orthogonal_to(w)
    print('3 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal))

    v = Vector([2.118, 4.827])
    w = Vector([0, 0])
    is_parallel = v.is_parallel_to(w)
    is_orthogonal = v.is_orthogonal_to(w)

    print('4 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal))

    # *****************

    v = Vector([3.039, 1.879])
    w = Vector([0.825, 2.036])
    projected_vector = v.component_parallel_to(w)

    print('projected vector is: {}'.format(projected_vector))

    v = Vector([-9.88, -3.264, -8.159])
    w = Vector([-2.155, -9.353, -9.473])
    orthogonal_vector = v.component_orthogonal_to(w)

    print('orthogonal vector is: {}'.format(orthogonal_vector))

    v = Vector([3.009, -6.172, 3.692, -2.51])
    w = Vector([6.404, -9.144, 2.759, 8.718])
    projected_vector = v.component_parallel_to(w)
    orthogonal_vector = v.component_orthogonal_to(w)

    print('second projected vector is: {}'.format(projected_vector))

    print('second orthogonal vector is: {}'.format(orthogonal_vector))

    # *****************

    v1 = Vector([8.462, 7.893, -8.187])
    w1 = Vector([6.984, -5.975, 4.778])

    v2 = Vector([-8.987, -9.838, 5.031])
    w2 = Vector([-4.268, -1.861, -8.866])

    v3 = Vector([1.5, 9.547, 3.691])
    w3 = Vector([-6.007, 0.124, 5.772])

    first_cross_product = v1.cross(w1)
    print('cross product is: {}'.format(first_cross_product))

    area_parallelogram = v2.area_of_parallelogram_with(w2)
    print('area parallelogram is: {}'.format(round(area_parallelogram, 3)))

    area_triangle = v3.area_of_triangle_with(w3)
    print('area triangle is: {}'.format(round(area_triangle, 3)))
