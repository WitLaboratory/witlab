import unittest

import numpy as np

import witlab.utils.functions as func
from witlab.models.aln import ALNModel
from witlab.utils.loadData import Dataset


class TestFunctions(unittest.TestCase):
    """
    Test functions in witlab/utils/functions.py
    """

    @classmethod
    def setUpClass(cls):
        ds = Dataset("gw")
        aln = ALNModel(Cmat=ds.Cmat, Dmat=ds.Dmat)

        # Resting state fits
        aln.params["mue_ext_mean"] = 1.57
        aln.params["mui_ext_mean"] = 1.6
        aln.params["sigma_ou"] = 0.09
        aln.params["b"] = 5.0
        aln.params["duration"] = 0.2 * 60 * 1000
        aln.run(bold=True, chunkwise=True)

        cls.model = aln
        cls.ds = Dataset("gw")

        cls.single_node = ALNModel()

    def test_kuramoto(self):
        kuramoto = func.kuramoto(self.model.rates_exc[:, ::10], smoothing=1.0)

    def test_fc(self):
        FC = func.fc(self.model.BOLD.BOLD)

    def test_fcd(self):
        rFCD = func.fcd(self.model.rates_exc, stepsize=100)

    def test_matrix_correlation(self):
        FC = func.fc(self.model.BOLD.BOLD)
        cc = func.matrix_correlation(FC, self.ds.FCs[0])

    def test_weighted_correlation(self):
        x = self.model.rates_exc[0, :]
        y = self.model.rates_exc[1, :]
        w = np.ones(x.shape)
        cc = func.weighted_correlation(x, y, w)

    def test_ts_kolmogorov(self):
        func.ts_kolmogorov(
            self.model.rates_exc[::20, :],
            self.model.rates_exc,
            stepsize=250,
            windowsize=30,
        )

    def test_matrix_kolmogorov(self):
        func.matrix_kolmogorov(
            func.fc(self.model.rates_exc[::20, :]),
            func.fc(self.model.rates_exc[::20, :]),
        )

    def test_getPowerSpectrum(self):
        fr, pw = func.getPowerSpectrum(self.model.rates_exc[0, :], dt=self.model.params["dt"])

    def test_getMeanPowerSpectrum(self):
        fr, pw = func.getMeanPowerSpectrum(self.model.rates_exc, dt=self.model.params["dt"])


if __name__ == "__main__":
    unittest.main()
