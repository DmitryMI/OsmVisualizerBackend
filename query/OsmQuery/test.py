import unittest
import OsmQuery

class OsmQueryTest(unittest.TestCase):
    def test_get_all_combinations(self):
        combinations = OsmQuery.get_all_combinations({})
        self.assertTrue(combinations is not None and len(combinations) == 0)

        key_values = {"var1": [1, 2], "var2": ['a', 'b', 'c'], "var3": [-1, -2], "var4": [0], "var5": []}
        correct_combinations = [
            {"var1": 1, "var2": 'a', "var3": -1, "var4": 0},
            {"var1": 2, "var2": 'a', "var3": -1, "var4": 0},
            {"var1": 1, "var2": 'b', "var3": -1, "var4": 0},
            {"var1": 2, "var2": 'b', "var3": -1, "var4": 0},
            {"var1": 1, "var2": 'c', "var3": -1, "var4": 0},
            {"var1": 2, "var2": 'c', "var3": -1, "var4": 0},
            {"var1": 1, "var2": 'a', "var3": -2, "var4": 0},
            {"var1": 2, "var2": 'a', "var3": -2, "var4": 0},
            {"var1": 1, "var2": 'b', "var3": -2, "var4": 0},
            {"var1": 2, "var2": 'b', "var3": -2, "var4": 0},
            {"var1": 1, "var2": 'c', "var3": -2, "var4": 0},
            {"var1": 2, "var2": 'c', "var3": -2, "var4": 0},
            ]
        combinations = OsmQuery.get_all_combinations(key_values)
        self.assertTrue(len(combinations) == len(correct_combinations))

        for i, c in enumerate(combinations):
            print(c)
            
            for key, value in c.items():
                self.assertTrue(correct_combinations[i][key] == value)

        #self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
