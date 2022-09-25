import unittest


class TestImports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from witlab.models.fhn import FHNModel

        fhn = FHNModel()
        fhn.run()
        cls.model = fhn

        from witlab.utils.parameterSpace import ParameterSpace

        pars = ParameterSpace({"x": [1, 2]})
        cls.pars = pars

    def test_model_imports(self):
        from witlab.models.hopf import HopfModel

        hopf = HopfModel()
        from witlab.models.aln import ALNModel

        aaln = ALNModel()
        from witlab.models.fhn import FHNModel

    def test_utils_imports(self):

        from witlab.utils.parameterSpace import ParameterSpace

        pars = ParameterSpace({"x": [1, 2]})

        from witlab.utils.signal import Signal

        signal = Signal(self.model.xr())

    def test_optimize_imports(self):
        from witlab.optimize.evolution import Evolution

        evolution = Evolution(evalFunction=(lambda f: f), parameterSpace=self.pars)

        from witlab.optimize.exploration import BoxSearch

        search = BoxSearch(evalFunction=(lambda f: f), parameterSpace=self.pars)


if __name__ == "__main__":
    unittest.main()
