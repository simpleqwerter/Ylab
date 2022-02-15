
class Figure:
    COUNT_SIDES = None
    sides = []
    angles = []
    def __str__(self):
        return self.__class__.__name__

    def generate_points(self):
        import math
        start_point = (5, 5)
        self.point_lst = [start_point,]
        angle = 0
        for i in range(self.COUNT_SIDES):
            angle += self.angles[i]
            print(angle)
            next_p = (self.point_lst[-1][0] + self.sides[i] * math.cos(math.radians(angle)),
                      self.point_lst[-1][1] + self.sides[i] * math.sin(math.radians(angle)))
            self.point_lst.append(next_p)


class Flat(Figure):
    def __init__(self):
        self._count_sides = None
        self.sides = []

    def get_perimetr(self):
        if len(self.sides) == self._count_sides:
            if all(side is not None for side in self.sides):
                self.perimetr = sum(self.sides)
                self.generate_points()
            else:
                self.clear_sides()
                self.get_sides()
                self.get_perimetr()

    def clear_sides(self):
        for i in self.sides:
            if i is None:
                self.sides.remove(None)

    def get_square(self):
        pass

    def get_sides(self):
        pass

    def generate_points(self):
        pass

class Square(Flat):
    COUNT_SIDES = 4

    def __init__(self, side=None, square=None, diagonal=None, r=None, R=None, perimetr=None):
        self._count_sides = self.COUNT_SIDES
        self.side = side
        self.sides = [self.side, self.side, self.side, self.side]
        self.angles = [90, 90, 90.01, 90]
        self.square = square
        self.diagonal = diagonal
        self.rad_ins = r
        self.rad_out = R
        self.perimetr = perimetr

    def calc(self):
        if self.side is None:
            self.get_sides()

        self.get_square()
        self.get_diagonal()
        self.get_rad_ins()
        self.get_rad_out()
        self.get_perimetr()  # super

    def get_sides(self):
        if self.perimetr:
            self.side = self.perimetr / 4
        elif self.square:
            self.side = self.square ** 0.5
        elif self.diagonal:
            self.side = self.diagonal / (2 ** 0.5)
        elif self.rad_ins:
            self.side = self.rad_ins * 2
        elif self.rad_out:
            self.side = (self.rad_out * 2) / (2 ** 0.5)
        self.sides = [self.side, self.side, self.side, self.side]
        self.calc()

    def get_square(self):
        self.square = self.side ** 2

    def get_diagonal(self):
        self.diagonal = (2 * (self.side ** 2)) ** 0.5
        self.rad_out = self.diagonal

    def get_rad_ins(self):
        self.rad_ins = self.side / 2

    def get_rad_out(self):
        self.rad_out = self.diagonal



class Circle(Flat):
  def __init__(self, radius=None, circumference=None, diametr=None, square=None):
    self.radius = radius
    self.circumference = circumference
    self.diametr = diametr
    self.square = square

  def calc(self):
    if self.radius:
      self.get_diametr()
      self.get_circumference()
      self.get_square()
    else:
      self.get_radius()
      self.calc()


  def get_radius(self):
    if self.diametr:
      self.radius = self.diametr / 2
    elif self.square:
      # не стал заморачиваться с Пи
      self.radius = (self.square / 3.141592) ** 0.5
    elif self.circumference:
      self.radius = self.circumference / (2 * 3.141592)
    else:
      raise ValueError

  def get_diametr(self):
    self.diametr = self.radius * 2

  def get_square(self):
    self.square = 3.141592 * (self.radius ** 2)

  def get_circumference(self):
    self.circumference = 2 * 3.141592 * self.radius


class Rectangle(Flat):  # прямоугольник
  COUNT_SIDES = 4

  class DataError(BaseException):
    def __str__(self):
      return 'not enought data'

  def __init__(self, a=None, b=None, square=None, diagonal=None, r=None, R=None, perimetr=None):
    self.a = a
    self.b = b
    self.sides = [a, b, a, b]
    self.angles = [90, 90, 90.01, 90]
    self._count_sides = self.COUNT_SIDES
    self.square = square
    self.diagonal = diagonal
    self.perimetr = perimetr
    self.r = r
    self.R = R

  def calc(self):
    if self.a and self.b:
      if self.a <= 0 or self.b <= 0:
        self.a, self.side_b = 0, 0
        raise ValueError("side can't be < 0")
      self.get_perimetr()
      self.get_diagonal()
      self.get_square()
    else:
      self.get_sides()
      self.sides = [self.a, self.a, self.b, self.b]
      self.calc()

  def get_sides(self):
    if self.perimetr and (self.a or self.b): # по периметру и одной стороне
      if self.a:
        self.b = self.perimetr / 2 - self.a
      elif self.b:
        self.a = self.perimetr / 2 - self.b
    elif self.b and self.R:
      self.a = (self.R ** 2 - self.b ** 2) ** 0.5
    elif self.square and (self.a or self.b): # по площади и одной стороне
      if self.a:
        self.b = self.square / self.a
      else:
        self.a = self.square / self.b
    elif self.diagonal and (self.a or self.b): # по диагонали и одной стороне
      if self.a:
        self.b = (self.diagonal ** 2 - self.a ** 2) ** 0.5
      elif self.b:
        self.a = (self.diagonal ** 2 - self.b ** 2) ** 0.5
    elif self.diagonal and self.perimetr: # по диагонали и периметру
      # b=(P+√(8d^2-P^2 ))/4 a=(P-√(8d^2-P^2 ))/4
      self.b = (self.perimetr + (8*self.diagonal ** 2 - self.perimetr ** 2) ** 0.5) / 4
      self.a = (self.perimetr - (8*self.diagonal ** 2 - self.perimetr ** 2) ** 0.5) / 4
      if self.a <= 0 or self.b <= 0:
        self.a, self.side_b = 0, 0
        raise ValueError("side can't be < 0")
    elif self.r and self.R: # по радиусам описанной и вписанной окружности
      self.a, self.b = self.r * 2, (((self.R * 2) ** 2) - (self.r * 2) ** 2) ** 0.5
    else:
      raise self.DataError

  def get_diagonal(self):
    if not self.diagonal:
      self.diagonal = (self.a ** 2 + self.b ** 2) ** 0.5
    self.R = self.diagonal / 2
    self.r = min(self.a, self.b) / 2

  def get_square(self):
    self.square = self.a * self.b




class Triangle(Flat):
  COUNT_SIDES = 3
  _count_sides = COUNT_SIDES


class TriangleEquilateral(Triangle):

    def __init__(self, a=None, h=None, r=None, R=None, perimetr=None, square=None):
        self.a = a
        self.h = h
        self.r = r
        self.R = R
        self.perimetr = perimetr
        self.square = square
        self.angle_a = 60
        self.sides = [self.a, self.a, self.a]
        self.angles = [60, 60, 60]

    def calc(self):
        if self.a <= 0:
            raise ValueError
        if self.a:
            self.get_perimetr()
            self.get_square()
            self.get_height()
            self.get_mediana()
            self.get_r()
            self.get_R()
        else:
            self.get_a()

    def get_a(self):
        if self.r:
            self.a = self.r * 2 * (3 ** 0.5)
        elif self.R:
            self.a = self.R * (3 ** 0.5)
        elif self.h:
            # a=2h/√3
            self.a = 2 * self.h / (3 ** 0.5)
        elif self.perimetr:
            self.a = self.perimetr / 3
        elif self.square:
            # 2√(S/√3)
            self.a = 2 * ((self.square / (3 ** 0.5)) ** 0.5)

    def get_r(self):
        # r=a/(2√3)
        self.r = self.a / (2 * (3 ** 0.5))

    def get_R(self):
        # R=a/√3
        self.R = self.a / (3 ** 0.5)

    def get_height(self):
        self.h = (self.a * (3 ** 0.5)) / 2

    def get_square(self):
        #     S=√(p(p-a)(p-b)(p-c)/2)
        if len(self.sides) == 3:
            self.square = (self.perimetr * (self.perimetr - self.a) *
                           (self.perimetr - self.a) *
                           (self.perimetr - self.a) / 2) ** 0.5

    def get_mediana(self):
        self.mediana = self.h


class Trapezoid(Flat):
    COUNT_SIZE = 4

    def __init__(self, a=None, b=None, c=None, d=None, mid_line=None, h=None):
        # b, d - основания
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.mid_line = mid_line
        self.h = h
        self.sides = [self.a, self.b, self.c, self.d]

        self._count_sides = 4

    def calc(self):
        self.clear_sides()
        if all([self.a, self.b, self.c, self.d]):
            self.get_h()
            self.get_mid_line()
            self.get_square()
            self.get_perimetr()  # super
        elif self.mid_line and self.h:
            self.get_square()

    def get_mid_line(self):
        if all([self.b, self.d]):
            self.mid_line = (self.b + self.d) / 2

    def get_h(self):
        # h=√(a^2-(((d-b)^2+a^2-c^2)/2(d-b) )^2 )
        if all([self.a, self.b, self.c, self.d]):
            self.h = (self.a ** 2 -
                      (((self.d - self.b) ** 2 + self.a ** 2 - self.c ** 2)
                       / (2 * (self.d - self.b))) ** 2) ** 0.5

    def get_square(self):
        self.square = self.mid_line * self.h


# sq = Square(5)
# sq.calc()
# print(vars(sq))
# c = Circle(square=314)
# c.calc()
# print(vars(c))
# rc = Rectangle(10, 20)
# rc.calc()
# print(vars(rc))
# tr = TriangleEquilateral(a=10)
# tr.calc()
# print(vars(tr))
# trap = Trapezoid(a=5, b=10, c=6, d=15)
# trap.calc()
# print(vars(trap))

