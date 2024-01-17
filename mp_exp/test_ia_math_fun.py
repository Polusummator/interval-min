import unittest
import decimal as dec
import interval_arithmetics as ia
import ia_math_fun as iam
import math

class TestIntervalMathFunctions(unittest.TestCase):
    
    def test_factorial(self):
        old_prec = ia.set_precision(2)
        u = ia.Interval(dec.Decimal('5'), dec.Decimal('7'))
        v = iam.factorial(u)        
        ia.set_precision(old_prec)
        self.assertEqual(v.a, dec.Decimal('1.2E+2'))
        self.assertEqual(v.b, dec.Decimal('5.1E+3'))

    def test_exponential(self):
        old_prec = ia.set_precision(2)
        test_set = [[0.25,0.5], [2,10], [-1,-0.5], [-1,0], [-5,5], [0.4, 0.4], [-5,-5]]
        for p in test_set:
            u = ia.Interval(dec.Decimal(p[0]), dec.Decimal(p[1]))
            v = iam.exp(u)  
            a = dec.Decimal(math.exp(p[0]))
            b = dec.Decimal(math.exp(p[1]))
            self.assertTrue(v.a <= a)
            self.assertTrue(b <= v.b)
        ia.set_precision(old_prec)
        
    def test_exponential_inf(self):
        old_prec = ia.set_precision(2)
        test_set = [[ia.c_minf, ia.c_minf], [ia.c_minf, ia.c_zero], [ia.c_zero, ia.c_inf], [ia.c_inf, ia.c_inf]]
        test_res = [[ia.c_zero, ia.c_zero], [ia.c_zero, ia.c_one], [ia.c_one, ia.c_inf], [ia.c_inf, ia.c_inf]]
        l = len(test_set)
        for i in range(0, l):
            p = test_set[i]
            r = test_res[i]
            u = ia.Interval(p[0], p[1])
            rv = ia.Interval(r[0], r[1])
            v = iam.exp(u)  
            self.assertTrue(v == rv)
        ia.set_precision(old_prec)

    def test_logarithm(self):
        old_prec = ia.set_precision(2)
        test_set = [[0.25,0.5], [2,10], [0.4, 0.4], [0.25,50]]
        for p in test_set:
            u = ia.Interval(dec.Decimal(p[0]), dec.Decimal(p[1]))
            v = iam.log(u)  
            a = dec.Decimal(math.log(p[0]))
            b = dec.Decimal(math.log(p[1]))
            self.assertTrue(v.a <= a)
            self.assertTrue(b <= v.b)
        ia.set_precision(old_prec)

    def test_logarithm_inf(self):
        old_prec = ia.set_precision(2)
        test_set = [[ia.c_zero, ia.c_one], [ia.c_inf, ia.c_inf]]
        test_res = [[ia.c_minf, ia.c_zero], [ia.c_inf, ia.c_inf]]
        l = len(test_set)
        for i in range(0, l):
            p = test_set[i]
            r = test_res[i]
            u = ia.Interval(p[0], p[1])
            rv = ia.Interval(r[0], r[1])
            v = iam.log(u)  
            self.assertTrue(v == rv)
        ia.set_precision(old_prec)
        
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestIntervalMathFunctions('test_factorial'))
    suite.addTest(TestIntervalMathFunctions('test_exponential'))
    suite.addTest(TestIntervalMathFunctions('test_exponential_inf'))
    suite.addTest(TestIntervalMathFunctions('test_logarithm'))
    suite.addTest(TestIntervalMathFunctions('test_logarithm_inf'))
    return suite

        
def run_tests():
    runner = unittest.TextTestRunner(verbosity=4)
    runner.run(suite())
    
if __name__ == '__main__':
    unittest.main()

