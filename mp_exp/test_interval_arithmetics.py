import unittest
from decimal import *
import interval_arithmetics as ia

class TestInterval(unittest.TestCase):
    
    def test_neg(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('101'), Decimal('201'))
        iv2 = - iv1
        self.assertEqual(iv2.a, Decimal('-210'))
        self.assertEqual(iv2.b, Decimal('-100'))
        iv1 = ia.Interval(Decimal('101'), Decimal('Infinity'))
        iv2 = - iv1
        self.assertEqual(iv2.a, Decimal('-Infinity'))
        self.assertEqual(iv2.b, Decimal('-100'))
        ia.set_precision(old_prec)
    
    def test_add(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('101'), Decimal('201'))
        iv2 = ia.Interval(Decimal('401'), Decimal('501'))
        iv3 = iv1 + iv2 + Decimal('601')
        ia.set_precision(old_prec)
        self.assertEqual(iv3.a, Decimal('1100'))
        self.assertEqual(iv3.b, Decimal('1400'))
    
    def test_add_inf(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('-Infinity'), Decimal('-1'))
        iv2 = ia.Interval(Decimal('-Infinity'), Decimal('-1'))
        iv3 = iv1 + iv2
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('-2'))
        iv4 = ia.Interval(Decimal('1'), Decimal('Infinity'))
        iv5 = iv4 + iv1
        ia.set_precision(old_prec)
        self.assertEqual(iv5.a, Decimal('-Infinity'))
        self.assertEqual(iv5.b, Decimal('Infinity'))

    def test_sub(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('101'), Decimal('201'))
        iv2 = ia.Interval(Decimal('402'), Decimal('502'))
        iv3 = (iv1 - iv2) - Decimal('601')
        ia.set_precision(old_prec)
        self.assertEqual(iv3.a, Decimal('-1100'))
        self.assertEqual(iv3.b, Decimal('-800'))

    def test_sub_inf(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('2'), Decimal('Infinity'))
        iv3 = iv1 - iv1
        ia.set_precision(old_prec)
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('Infinity'))

    def test_mul(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('-21'), Decimal('31'))
        iv2 = ia.Interval(Decimal('11'), Decimal('12'))
        iv3 = iv1 * iv2        
        ia.set_precision(old_prec)
        self.assertEqual(iv3.a, Decimal('-260'))
        self.assertEqual(iv3.b, Decimal('380'))
        
    def test_mul_inf(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('-Infinity'), Decimal('-1'))
        iv2 = ia.Interval(Decimal('1'), Decimal('-Infinity'))
        iv3 = iv1 * iv2        
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('Infinity'))
        iv1 = ia.Interval(Decimal('0'), Decimal('Infinity'))
        iv2 = ia.Interval(Decimal('1'), Decimal('Infinity'))
        iv3 = iv1 * iv2        
        self.assertEqual(iv3.a, Decimal('0'))
        self.assertEqual(iv3.b, Decimal('Infinity'))
        ia.set_precision(old_prec)

    def test_pow(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('-11'), Decimal('12'))
        iv2 = iv1 ** 2
        self.assertEqual(iv2.a, Decimal('0'))
        self.assertEqual(iv2.b, Decimal('150'))
        iv2 = iv1 ** 3
        self.assertEqual(iv2.a, Decimal('-1400'))
        self.assertEqual(iv2.b, Decimal('1800'))
        iv1 = ia.Interval(Decimal('11'), Decimal('12'))
        iv2 = iv1 ** 2
        self.assertEqual(iv2.a, Decimal('120'))
        self.assertEqual(iv2.b, Decimal('150'))
        iv1 = ia.Interval(Decimal('-12'), Decimal('-11'))
        iv2 = iv1 ** 2
        self.assertEqual(iv2.a, Decimal('120'))
        self.assertEqual(iv2.b, Decimal('150'))
        ia.set_precision(old_prec)
    
    def test_pow_inf(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('-Infinity'), Decimal('Infinity'))
        iv2 = iv1 ** 2
        self.assertEqual(iv2.a, Decimal('0'))
        self.assertEqual(iv2.b, Decimal('Infinity'))
        iv2 = iv1 ** 3
        self.assertEqual(iv2.a, Decimal('-Infinity'))
        self.assertEqual(iv2.b, Decimal('Infinity'))
        ia.set_precision(old_prec)

    def test_truediv(self):
        old_prec = ia.set_precision(2)
        iv1 = ia.Interval(Decimal('3'), Decimal('4'))
        iv2 = ia.Interval(Decimal('4'), Decimal('8'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('1'))
        self.assertEqual(iv3.b, Decimal('2.8'))        
        ia.set_precision(old_prec)

    def test_truediv_inf(self):
        old_prec = ia.set_precision(2)
        
        iv1 = ia.Interval(Decimal('0'), Decimal('0'))
        iv2 = ia.Interval(Decimal('-4'), Decimal('8'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('Infinity'))

        iv1 = ia.Interval(Decimal('0'), Decimal('0'))
        iv2 = ia.Interval(Decimal('4'), Decimal('8'))
        iv3 = iv2 / iv1
        self.assertIsNone(iv3)
        
        iv1 = ia.Interval(Decimal('-1'), Decimal('4'))
        iv2 = ia.Interval(Decimal('-4'), Decimal('8'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('Infinity'))
        
        iv1 = ia.Interval(Decimal('-4'), Decimal('0'))
        iv2 = ia.Interval(Decimal('-4'), Decimal('-2'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('0.5'))
        self.assertEqual(iv3.b, Decimal('Infinity'))
        
        iv1 = ia.Interval(Decimal('-Infinity'), Decimal('0'))
        iv2 = ia.Interval(Decimal('-4'), Decimal('-2'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('0'))
        self.assertEqual(iv3.b, Decimal('Infinity'))
        
        iv1 = ia.Interval(Decimal('-4'), Decimal('0'))
        iv2 = ia.Interval(Decimal('2'), Decimal('4'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('-0.5'))
        
        iv1 = ia.Interval(Decimal('-Infinity'), Decimal('0'))
        iv2 = ia.Interval(Decimal('2'), Decimal('4'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('0'))
        
        iv1 = ia.Interval(Decimal('0'), Decimal('8'))
        iv2 = ia.Interval(Decimal('1'), Decimal('4'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('0.12'))
        self.assertEqual(iv3.b, Decimal('Infinity'))
       
        iv1 = ia.Interval(Decimal('0'), Decimal('Infinity'))
        iv2 = ia.Interval(Decimal('1'), Decimal('4'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('0'))
        self.assertEqual(iv3.b, Decimal('Infinity'))

        iv1 = ia.Interval(Decimal('0'), Decimal('8'))
        iv2 = ia.Interval(Decimal('-4'), Decimal('-1'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('-0.12'))
       
        iv1 = ia.Interval(Decimal('0'), Decimal('Infinity'))
        iv2 = ia.Interval(Decimal('-4'), Decimal('-1'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3.a, Decimal('-Infinity'))
        self.assertEqual(iv3.b, Decimal('0'))

        ia.set_precision(old_prec)
        
    def test_truediv_split(self):
        old_prec = ia.set_precision(2)
        
        iv1 = ia.Interval(Decimal('-3'), Decimal('4'))
        iv2 = ia.Interval(Decimal('2'), Decimal('3'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3[0].b, Decimal('-0.66'))
        self.assertEqual(iv3[1].a, Decimal('0.5'))
        
                
        iv1 = ia.Interval(Decimal('-3'), Decimal('4'))
        iv2 = ia.Interval(Decimal('-3'), Decimal('-2'))
        iv3 = iv2 / iv1
        self.assertEqual(iv3[0].b, Decimal('-0.5'))
        self.assertEqual(iv3[1].a, Decimal('0.66'))

        ia.set_precision(old_prec)

        
    def test_reverse(self):
        old_prec = ia.set_precision(2)
        
        iv1 = Decimal('2')
        iv2 = ia.Interval(Decimal('2'), Decimal('4'))
        iv3 = iv1 + iv2
        self.assertEqual(iv3.a, Decimal('4'))
        self.assertEqual(iv3.b, Decimal('6'))
        
        iv3 = iv1 - iv2
        self.assertEqual(iv3.a, Decimal('-2'))
        self.assertEqual(iv3.b, Decimal('0'))

        iv3 = iv1 * iv2
        self.assertEqual(iv3.a, Decimal('4'))
        self.assertEqual(iv3.b, Decimal('8'))
        
        iv3 = iv1 / iv2
        self.assertEqual(iv3.a, Decimal('0.5'))
        self.assertEqual(iv3.b, Decimal('1'))

        ia.set_precision(old_prec)
       
    
    def test_convert_interval(self):
        old_prec = ia.set_precision(2)
        iv2 = ia.Interval(Decimal('2'), Decimal('4'))
        iv3 = 1 + iv2 + Decimal('2')
        self.assertEqual(iv3.a, Decimal('5'))
        self.assertEqual(iv3.b, Decimal('7'))        
        ia.set_precision(old_prec)
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestInterval('test_neg'))
    suite.addTest(TestInterval('test_add'))
    suite.addTest(TestInterval('test_add_inf'))
    suite.addTest(TestInterval('test_sub'))
    suite.addTest(TestInterval('test_sub_inf'))
    suite.addTest(TestInterval('test_mul'))
    suite.addTest(TestInterval('test_mul_inf'))
    suite.addTest(TestInterval('test_pow'))
    suite.addTest(TestInterval('test_pow_inf'))
    suite.addTest(TestInterval('test_truediv'))    
    suite.addTest(TestInterval('test_truediv_inf'))    
    suite.addTest(TestInterval('test_truediv_split')) 
    suite.addTest(TestInterval('test_reverse')) 
    suite.addTest(TestInterval('test_convert_interval')) 
    return suite

        
def run_tests():
    runner = unittest.TextTestRunner(verbosity=4)
    runner.run(suite())
    
if __name__ == '__main__':
    unittest.main()
