"""This module implements correctly rounded interval arithmetics according to Kahan-Novoa-Ratz
    according to Ratschek H., Rokne J. New computer methods for global optimization. – Halsted Press, 1988. book.
"""

import decimal as dec

# Usefull numerical constants

# +Infinity
c_inf = dec.Decimal('Infinity')

# -Infinity
c_minf = dec.Decimal('-Infinity')

# 0
c_zero = dec.Decimal('0')

# 1 
c_one = dec.Decimal('1')

# -1
c_mone = dec.Decimal('-1')

# 2
c_two = dec.Decimal('2')

# -2
c_mtwo = dec.Decimal('-2')


def set_precision(prec):
    """
    Sets the precision as the number of significant decimal digits in mantissa
    
    Parameters
    ----------
    prec : integer
        The number of decimal places (should be between 1 and some reasonable value)
    """
    prev = dec.getcontext().prec
    dec.getcontext().prec = prec
    return prev


def _set_rounding_mode(rounding_mode):
    prev = dec.getcontext().rounding
    dec.getcontext().rounding = rounding_mode
    return prev


def _set_rounding_mode_default():
    return _set_rounding_mode(dec.ROUND_HALF_EVEN)


def _set_rounding_mode_ceil():
    return _set_rounding_mode(dec.ROUND_CEILING)


def _set_rounding_mode_floor():
    return _set_rounding_mode(dec.ROUND_FLOOR)


def _my_mul(a, b):
    if (a == c_zero) or (b == c_zero):
        return c_zero
    else:
        return a * b


def _my_div(a, b):
    if b.is_infinite():
        if a.is_infinite():
            raise ValueError('Infinity by infinity division')
        else:
            return dec.Decimal('0')
    return a / b


class Interval:
    """Class for storing interval values and perform interval operations"""

    @classmethod
    def to_interval(cls, other):
        """
        Constructs a new dot Interval Decimal, int or float.
        Returns Interval if Interval is given.
        """

        if type(other) is dec.Decimal:
            return Interval(other, other)
        elif type(other) is int or type(other) is float:
            v = dec.Decimal(other)
            return Interval(v, v)
        else:
            return other

    def __init__(self, a: dec.Decimal, b: dec.Decimal):
        """
        Constructor

        Parameters
        ----------
        a : interval's left end
        b : interval's right end

        """
        self.a = a
        self.b = b

    def __neg__(self):
        _set_rounding_mode_floor()
        a = -self.b
        _set_rounding_mode_ceil()
        b = -self.a
        return Interval(a, b)

    def __eq__(self, other):
        return (self.a == other.a) and (self.b == other.b)

    def __add__(self, other):
        nother = Interval.to_interval(other)
        _set_rounding_mode_floor()
        a = self.a + nother.a
        _set_rounding_mode_ceil()
        b = self.b + nother.b
        return Interval(a, b)

    def __sub__(self, other):
        nother = Interval.to_interval(other)
        _set_rounding_mode_floor()
        a = self.a - nother.b
        _set_rounding_mode_ceil()
        b = self.b - nother.a
        return Interval(a, b)

    def __mul__(self, other):
        nother = Interval.to_interval(other)
        _set_rounding_mode_floor()
        aa = _my_mul(self.a, nother.a)
        ab = _my_mul(self.a, nother.b)
        ba = _my_mul(self.b, nother.a)
        bb = _my_mul(self.b, nother.b)
        a = min(aa, ab, ba, bb)
        _set_rounding_mode_ceil()
        aa = _my_mul(self.a, nother.a)
        ab = _my_mul(self.a, nother.b)
        ba = _my_mul(self.b, nother.a)
        bb = _my_mul(self.b, nother.b)
        b = max(aa, ab, ba, bb)
        return Interval(a, b)

    def __pow__(self, other):
        if type(other) is int:
            copy = Interval(self.a, self.b)
            if other == 0:
                return Interval.to_interval(1)
            if other < 0:
                copy = Interval.to_interval(1) / self
                other *= -1

            _set_rounding_mode_floor()
            if other % 2 == 0:
                if copy.a <= c_zero <= copy.b:
                    a = c_zero
                    _set_rounding_mode_ceil()
                    if -copy.a < copy.b:
                        b = copy.b ** other
                    else:
                        b = copy.a ** other
                elif copy.a > c_zero:
                    a = copy.a ** other
                    _set_rounding_mode_ceil()
                    b = copy.b ** other
                elif copy.b < c_zero:
                    a = copy.b ** other
                    _set_rounding_mode_ceil()
                    b = copy.a ** other
            else:
                a = copy.a ** other
                _set_rounding_mode_ceil()
                b = copy.b ** other
            return Interval(a, b)
        else:
            raise TypeError("Power must be an integer")

    def __truediv__(self, other):
        nother = Interval.to_interval(other)
        if nother.a == nother.b == c_zero:
            if self.a <= c_zero <= self.b:
                return Interval(c_minf, c_inf)
            else:
                return None
        elif nother.a > c_zero or nother.b < c_zero:
            _set_rounding_mode_floor()
            ra = c_one / nother.b
            _set_rounding_mode_ceil()
            rb = c_one / nother.a
            return self.__mul__(Interval(ra, rb))
        elif self.a <= c_zero <= self.b:
            return Interval(c_minf, c_inf)
        elif nother.a == c_zero:
            if self.b < c_zero:
                _set_rounding_mode_ceil()
                rb = _my_div(self.b, nother.b)
                return Interval(c_minf, rb)
            elif self.a > c_zero:
                _set_rounding_mode_floor()
                ra = _my_div(self.a, nother.b)
                return Interval(ra, c_inf)
        elif nother.b == c_zero:
            if self.b < c_zero:
                _set_rounding_mode_floor()
                ra = _my_div(self.b, nother.a)
                return Interval(ra, c_inf)
            elif self.a > c_zero:
                _set_rounding_mode_ceil()
                rb = _my_div(self.a, nother.a)
                return Interval(c_minf, rb)
        else:  # nother.a < 0 < nother.b:
            if self.b < c_zero:
                _set_rounding_mode_ceil()
                ra = _my_div(self.b, nother.b)
                _set_rounding_mode_floor()
                rb = _my_div(self.b, nother.a)
            elif self.a > c_zero:
                _set_rounding_mode_ceil()
                ra = _my_div(self.a, nother.a)
                _set_rounding_mode_floor()
                rb = _my_div(self.a, nother.b)
            return [Interval(c_minf, ra), Interval(rb, c_inf)]

    def __radd__(self, other):
        nother = Interval.to_interval(other)
        return nother.__add__(self)

    def __rsub__(self, other):
        nother = Interval.to_interval(other)
        return nother.__sub__(self)

    def __rmul__(self, other):
        nother = Interval.to_interval(other)
        return nother.__mul__(self)

    def __rtruediv__(self, other):
        nother = Interval.to_interval(other)
        return nother.__truediv__(self)

    def __repr__(self):
        return "[" + str(self.a) + ", " + str(self.b) + "]"

    @property
    def mid(self):
        """Returns the best approximation of the interval central point"""
        _set_rounding_mode_default()
        return dec.Decimal('0.5') * (self.a + self.b)

    @property
    def mid_interval(self):
        """Returns the narrowest interval, containing the interval central point"""
        _set_rounding_mode_floor()
        a = dec.Decimal('0.5') * (self.a + self.b)
        _set_rounding_mode_ceil()
        b = dec.Decimal('0.5') * (self.a + self.b)
        return Interval(a, b)

    @property
    def wid(self):
        """Returns the closest outer approximation of the interval's width"""
        _set_rounding_mode_ceil()
        return self.b - self.a

    @property
    def rad(self):
        """Returns the closest outer approximation of the interval's width"""
        return self.wid / 2

    def __contains__(self, point):
        return self.a <= point <= self.b

    @property
    def is_dot_interval(self):
        """
        Checks whether the interval is a dot interval, i.e. left end = right end

        Returns:
        --------
        True if x is a dot interval, False otherwise
        """
        res = dec.compare(self.a, self.b)
        return True if res == c_zero else False

    # Some utility function for working with intervals


def intersect(ival1, ival2):
    """
    Computes the intersection of intervals

    Parameters
    ----------
    ival1 : 1st interval
    ival2 : 2nd interval

    Returns
    -------
    The intersection of intervals ival1 and ival2 (None in there is no intersection)
    """
    if ival1.b < ival2.a or ival2.b < ival1.a:
        return None
    else:
        a = max(ival1.a, ival2.a)
        b = min(ival1.b, ival2.b)
        return Interval(a, b)
