"""This module implements correctly rounded interval functions
"""
import decimal as dec
import interval_arithmetics as ia


# -------------- Factorial function --------

def factorial(n):
    """
    Computes interval extension for a factorial function
    
    Parameters
    ----------
    n : Interval 
        
    Returns:
    --------
    The interval that enclose the range of the factorial function
    """
    a = ia.c_one
    ia._set_rounding_mode_floor()
    for i in range(2, int(n.a) + 1):
        a = a * dec.Decimal(i)
    b = ia.c_one
    ia._set_rounding_mode_ceil()
    for i in range(2, int(n.b) + 1):
        b = b * dec.Decimal(i)    
    return ia.Interval(a, b)



# --------------- Exponential ---------------

#     Number of Taylor's series terms for exponential
#     Notice, that this number will be multiplied by two to bound the exp(x) between the consecutive sums
#     1 + x + ... + x^(2n - 1) < exp(x) < 1 + x + ... + x^(2n)
exp_taylor_terms_number = 5


def get_exp_taylor_terms_number():
    """
    Retrieves the number of Taylor's series terms
    
    Notice, that this number will be multiplied by two to bound the exp(x) between the consecutive sums
    1 + x + ... + x^(2n - 1) < exp(x) < 1 + x + ... + x^(2n)
    
    Returns:
    ----------
    the  value of exp_taylor_terms_number    
    """
    global exp_taylor_terms_number
    return exp_taylor_terms_number


def set_exp_taylor_terms_number(number):
    """
    Sets new number of Taylor's series members to approximate the exponential. 
    
    Notice, that this number will be multiplied by two to bound the exp(x) between the consecutive sums
    1 + x + ... + x^(2n - 1) < exp(x) < 1 + x + ... + x^(2n)
    
    Parameters:
    ----------
    number : new value of exp_taylor_terms_number
    
    Returns:
    ----------
    the previous value of exp_taylor_terms_number
    """
    global exp_taylor_terms_number
    old = exp_taylor_terms_number
    exp_taylor_terms_number = number
    return old

# Exponential for x in a range [-1, 0], lower bound, x is a dot interval
def _exp_f_m1_to_0_lb(x):
    global exp_taylor_terms_number
    n = 2 * exp_taylor_terms_number
    s = ia.Interval(ia.c_one, ia.c_one)
    for i in range(1, n):
        ii = ia.Interval(dec.Decimal(i), dec.Decimal(i))
        term = (x ** i) / factorial(ii)
        s += term
    return s.a

# Exponential for x in a range [-1, 0], upper bound, x is a dot interval
def _exp_f_m1_to_0_ub(x):
    global exp_taylor_terms_number
    n = 2 * exp_taylor_terms_number + 1 
    s = ia.Interval(ia.c_one, ia.c_one)
    for i in range(1, n):
        ii = ia.Interval(dec.Decimal(i), dec.Decimal(i))
        term = (x ** i) / factorial(ii)
        s += term
    return s.b

# Exponential for x in a range [-inf, -1), lower bound, x is a dot interval
def _exp_f_minf_to_m1_lb(x):
    z = -(x.a.to_integral(rounding = dec.ROUND_FLOOR))
    ivz = ia.Interval(z,z)
    ivf = x / ivz
    etv = _exp_f_m1_to_0_lb(ivf)
    ietv = ia.Interval(etv,etv)
    iev = ietv ** int(z)
    return iev.a

# Exponential for x in a range [-inf, -1), upper bound, x is a dot interval
def _exp_f_minf_to_m1_ub(x):
    z = -(x.a.to_integral(rounding = dec.ROUND_FLOOR))
    ivz = ia.Interval(z,z)
    ivf = x / ivz
    etv = _exp_f_m1_to_0_ub(ivf)
    ietv = ia.Interval(etv,etv)
    iev = ietv ** int(z)
    return iev.b

# Exponential for x in a range (0, +inf], lower bound, x is a dot interval
def _exp_f_0_to_inf_lb(x):
    if x.a > ia.c_one:
        irev = _exp_f_minf_to_m1_ub(-x)
    else:
        irev = _exp_f_m1_to_0_ub(-x)
    ione = ia.Interval(dec.Decimal('1'),dec.Decimal('1'))
    iev = ione / irev
    return iev.a

# Exponential for x in a range (0, +inf], upper bound, x is a dot interval
def _exp_f_0_to_inf_ub(x):
    if x.a > ia.c_one:
        irev = _exp_f_minf_to_m1_lb(-x)
    else:
        irev = _exp_f_m1_to_0_lb(-x)
    ione = ia.Interval(ia.c_one,ia.c_one)
    iev = ione / irev
    return iev.b



# Exponential lower bound for x, x is a dot interval
def _exp_lb(x):
    if x.a == ia.c_minf:
        return ia.c_zero
    elif x.a < ia.c_mone:
        return _exp_f_minf_to_m1_lb(x)
    elif ia.c_mone <= x.a < ia.c_zero:
        return _exp_f_m1_to_0_lb(x)
    elif x.a == ia.c_zero:
        return ia.c_one
    elif x.a == ia.c_inf:
        return ia.c_inf
    else:
        return _exp_f_0_to_inf_lb(x)
   
    
# Exponential upper bound for x, x is a dot interval
def _exp_ub(x):
    if x.b == ia.c_minf:
        return ia.c_zero
    elif x.b < ia.c_mone:
        return _exp_f_minf_to_m1_ub(x)
    elif ia.c_mone <= x.b < ia.c_zero:
        return _exp_f_m1_to_0_ub(x)
    elif x.b == ia.c_zero:
        return ia.c_one
    elif x.b == ia.c_inf:
        return ia.c_inf
    else:
        return _exp_f_0_to_inf_ub(x)
    

    
def exp(x):
    """
    Computes reliable bounds for exponential.
    
    Parameters:
    -----------
    x : an interval
    
    Returns:
    --------
    Enclosing interval for exp(x)
    """
    a = _exp_lb(ia.Interval(x.a, x.a))
    b = _exp_ub(ia.Interval(x.b, x.b))
    return ia.Interval(a, b)
    

#------------ Natural logarithm ------------------------    
#  Natural logarithm approximation based on Taylor series of ln ((1+x)/(1-x))
#

# Number of Taylor expansion terms

log_taylor_terms_number = 5


def get_log_taylor_terms_number():
    """
    Retrieves number of Taylor's series members to approximate the natural logarithm.
    
    Notice, that this number will be multiplied by two to bound the ln(1 + x) between the consecutive sums
    x - (x^2)/2 + (x^3)/3 - ... - (x^2n)/2n < ln(1 + x) <  x - (x^2)/2 + (x^3)/3 - ... - (x^2n)/2n + (x^(2n+1))/(2n+1)
    
    Returns:
    ----------
    the  value of log_taylor_terms_number    
    """
    global log_taylor_terms_number
    return log_taylor_terms_number


def set_log_taylor_terms_number(number):
    """
    Sets new number of Taylor's series members to approximate the natural logarithm. 
    
    Notice, that this number will be multiplied by two to bound the ln(1 + x/1 - x) 
    
    Parameters:
    ----------
    number : new value of ln_taylor_terms_number
    
    Returns:
    ----------
    the previous value of ln_taylor_terms_number
    """
    global log_taylor_terms_number
    old = log_taylor_terms_number
    log_taylor_terms_number = number
    return old

# Point x from 1 to infinity
def _log_f_1_to_inf(xp):
    x = ia.Interval(xp, xp)
    inul = ia.Interval(ia.c_zero, ia.c_zero)
    ione = ia.Interval(ia.c_one, ia.c_one)
    itwo = ia.Interval(ia.c_two, ia.c_two)
    z = (x - ione) / (x + ione)
    s = inul
    zn = z
    zq = pow(z, 2)
    global log_taylor_terms_number
    k = log_taylor_terms_number
    for i in range(0, k + 1):
        ii = ia.Interval(dec.Decimal(2*i + 1), dec.Decimal(2*i + 1))
        s += zn / ii
        zn *= zq
    t = ia.Interval(dec.Decimal(2*k + 3), dec.Decimal(2*k + 3)) * (ione - zq)
    su = s + zn / t 
    s *= itwo
    su *= itwo
    iret = ia.Interval(s.a, su.b)
    return iret

# Point x from 0 to 1
def _log_f_0_to_1(xp):
    x = ia.Interval(xp, xp)
    inul = ia.Interval(ia.c_zero, ia.c_zero)
    ione = ia.Interval(ia.c_one, ia.c_one)
    itwo = ia.Interval(ia.c_two, ia.c_two)
    z = (x - ione) / (x + ione)
    s = inul
    zn = z
    zq = pow(z, 2)
    global log_taylor_terms_number
    k = log_taylor_terms_number
    for i in range(0, k + 1):
        ii = ia.Interval(dec.Decimal(2*i + 1), dec.Decimal(2*i + 1))
        s += zn / ii
        zn *= zq
    t = ia.Interval(dec.Decimal(2*k + 3), dec.Decimal(2*k + 3)) * (ione - zq)
    su = s + zn / t 
    s *= itwo
    su *= itwo
    iret = ia.Interval(su.a, s.b)
    return iret

# logarithm for a point
def _log_point(xp):
    if xp == ia.c_zero:
        ival = ia.Interval(ia.c_minf,ia.c_minf)
    elif xp == ia.c_one:
        ival = ia.Interval(ia.c_zero, ia.c_zero)
    elif xp < ia.c_one:
        ival = _log_f_0_to_1(xp)
    elif xp == ia.c_inf:
        ival = ia.Interval(ia.c_inf,ia.c_inf)
    else:
        ival = _log_f_1_to_inf(xp)
    return ival
     


def log(x):
    """
    Computes reliable bounds for natural logarithm.
    
    Parameters:
    -----------
    x : an interval
    
    Returns:
    --------
    Enclosing interval for ln(x)
    """
    loga = _log_point(x.a)
    logb = _log_point(x.b)
    iret = ia.Interval(loga.a, logb.b)
    return iret


    
#------------ Natural logarithm ------------------------    

#     Number of Taylor's series terms for ln(1 + x)
#     Notice, that this number will be multiplied by two to bound the ln(1 + x) between the consecutive sums
#     x - (x^2)/2 + (x^3)/3 - ... - (x^2n)/2n < ln(1 + x) <  x - (x^2)/2 + (x^3)/3 - ... - (x^2n)/2n + (x^(2n+1))/(2n+1)




# # Lower bound for ln(x), x in (1, 2]
# def _log_f_1_to_2_lb(x):
#     global log_taylor_terms_number
#     n = 2 * log_taylor_terms_number
#     y = x - ia.Interval(dec.Decimal(1), dec.Decimal(1))
#     s = y
#     for i in range(2, n + 1):
#         ii = ia.Interval(dec.Decimal(i), dec.Decimal(i))
#         term = (y ** i) / ii
#         if i % 2 == 0:
#             s -= term
#         else: 
#             s += term
#     return s.a

# # Upper bound for ln(x), x in (1, 2]
# def _log_f_1_to_2_ub(x):
#     global log_taylor_terms_number
#     n = 2 * log_taylor_terms_number + 1
#     y = x - ia.Interval(dec.Decimal(1), dec.Decimal(1))
#     s = y
#     for i in range(2, n + 1):
#         ii = ia.Interval(dec.Decimal(i), dec.Decimal(i))
#         term = (y ** i) / ii
#         if i % 2 == 0:
#             s -= term
#         else: 
#             s += term
#     return s.b

# # Lower for ln(x)
# def _log_lb(x):
#     return _log_f_1_to_2_lb(x)

# # Upper for ln(x)
# def _log_ub(x):
#     return _log_f_1_to_2_ub(x)


# def log(x):
#     """
#     Computes reliable bounds for logarithm.
    
#     Parameters:
#     -----------
#     x : an interval
    
#     Returns:
#     --------
#     Enclosing interval for ln(x)
#     """
#     a = _log_lb(ia.Interval(x.a, x.a))
#     b = _log_ub(ia.Interval(x.b, x.b))
#     return ia.Interval(a, b)
    


