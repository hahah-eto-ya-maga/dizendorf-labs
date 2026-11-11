import math
import unittest

from intervals import confidence_intervals


class IntervalTests(unittest.TestCase):
    def test_known_table_values_and_variance_tail_order(self):
        # N=2: t has one degree of freedom; reference values from standard tables.
        r = confidence_intervals([0, 2], 1, 1)
        self.assertAlmostEqual(r['student'], 12.706204736, places=7)
        self.assertAlmostEqual(r['chi_low'], 0.000982069, places=8)
        self.assertAlmostEqual(r['chi_high'], 5.023886187, places=7)
        self.assertAlmostEqual(r['rows'][0][1], 1 - 1.95996398454 / math.sqrt(2))
        self.assertAlmostEqual(r['rows'][2][1], 2 / 5.023886187, places=7)
        self.assertAlmostEqual(r['rows'][3][1] ** 2, r['rows'][2][1])
        self.assertAlmostEqual(r['rows'][3][2] ** 2, r['rows'][2][2])

    def test_translation_and_scaling(self):
        values = [-2, -0.3, 0.8, 1.5, 3]
        a = confidence_intervals(values, 2, 1)
        b = confidence_intervals([3*x+7 for x in values], 6, 10)
        for i in [0, 1]:
            for j in [1, 2]:
                self.assertAlmostEqual(b['rows'][i][j], 3*a['rows'][i][j]+7)
        for j in [1, 2]:
            self.assertAlmostEqual(b['rows'][2][j], 9*a['rows'][2][j])
            self.assertAlmostEqual(b['rows'][3][j], 3*a['rows'][3][j])

    def test_higher_confidence_widens_intervals(self):
        narrow = confidence_intervals([0, 1, 2, 3], 1, 0, 0.9)
        wide = confidence_intervals([0, 1, 2, 3], 1, 0, 0.99)
        for x, y in zip(narrow['rows'], wide['rows']):
            self.assertLess(y[1], x[1])
            self.assertGreater(y[2], x[2])

    def test_invalid_samples(self):
        for values in [[], [1], [2, 2], [0, float('nan')]]:
            with self.assertRaises(ValueError):
                confidence_intervals(values, 1, 0)


if __name__ == '__main__':
    unittest.main()
