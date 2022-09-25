"""
Set of tests for Hopf normal form model.
"""
import unittest
import pytest

import numpy as np
import xarray as xr
from jitcdde import jitcdde_input
from witlab.models.hopf import HopfModel
from witlab.models.multimodel.builder.hopf import HOPF_DEFAULT_PARAMS, HopfMass, HopfNetwork, HopfNode
from witlab.utils.stimulus import ZeroInput

SEED = 42
DURATION = 100.0
DT = 0.1
CORR_THRESHOLD = 0.95
witlab_VARIABLES_TO_TEST = ["x", "y"]

# dictionary as backend name: format in which the noise is passed
BACKENDS_TO_TEST = {
    "jitcdde": lambda x, d, dt: x.as_cubic_splines(d, dt),
    "numba": lambda x, d, dt: x.as_array(d, dt),
}


class MassTestCase(unittest.TestCase):
    def _run_mass(self, node, duration, dt):
        coupling_variables = {k: 0.0 for k in node.required_couplings}
        noise = ZeroInput(n=node.num_noise_variables).as_cubic_splines(duration, dt)
        system = jitcdde_input(node._derivatives(coupling_variables), input=noise)
        system.constant_past(np.array(node.initial_state))
        system.adjust_diff()
        times = np.arange(dt, duration + dt, dt)
        return np.vstack([system.integrate(time) for time in times])


class TestHopfMass(MassTestCase):
    def _create_mass(self):
        hopf = HopfMass()
        hopf.index = 0
        hopf.idx_state_var = 0
        hopf.init_mass()
        return hopf

    def test_init(self):
        hopf = self._create_mass()
        self.assertTrue(isinstance(hopf, HopfMass))
        self.assertDictEqual({k: v for k, v in hopf.params.items() if "input" not in k}, HOPF_DEFAULT_PARAMS)
        coupling_variables = {k: 0.0 for k in hopf.required_couplings}
        self.assertEqual(len(hopf._derivatives(coupling_variables)), hopf.num_state_variables)
        self.assertEqual(len(hopf.initial_state), hopf.num_state_variables)
        self.assertEqual(len(hopf.noise_input_idx), hopf.num_noise_variables)

    def test_run(self):
        hopf = self._create_mass()
        result = self._run_mass(hopf, DURATION, DT)
        self.assertTrue(isinstance(result, np.ndarray))
        self.assertTupleEqual(result.shape, (int(DURATION / DT), hopf.num_state_variables))


class TestHopfNode(unittest.TestCase):
    def _create_node(self):
        node = HopfNode(seed=SEED)
        node.index = 0
        node.idx_state_var = 0
        node.init_node()
        return node

    def test_init(self):
        hopf = self._create_node()
        self.assertTrue(isinstance(hopf, HopfNode))
        self.assertEqual(len(hopf), 1)
        self.assertDictEqual({k: v for k, v in hopf[0].params.items() if "input" not in k}, HOPF_DEFAULT_PARAMS)
        self.assertEqual(len(hopf.default_network_coupling), 2)
        np.testing.assert_equal(np.array(hopf[0].initial_state), hopf.initial_state)

    @pytest.mark.xfail
    def test_run(self):
        hopf = self._create_node()
        all_results = []
        for backend, noise_func in BACKENDS_TO_TEST.items():
            result = hopf.run(
                DURATION,
                DT,
                noise_func(ZeroInput(hopf.num_noise_variables), DURATION, DT),
                backend=backend,
            )
            self.assertTrue(isinstance(result, xr.Dataset))
            self.assertEqual(len(result), hopf.num_state_variables)
            self.assertTrue(all(state_var in result for state_var in hopf.state_variable_names[0]))
            self.assertTrue(
                all(result[state_var].shape == (int(DURATION / DT), 1) for state_var in hopf.state_variable_names[0])
            )
            all_results.append(result)
        # test results are the same from different backends
        for state_var in all_results[0]:
            corr_mat = np.corrcoef(
                np.vstack([result[state_var].values.flatten().astype(float) for result in all_results])
            )
            self.assertTrue(np.greater(corr_mat, CORR_THRESHOLD).all())

    @pytest.mark.xfail
    def test_compare_w_witlab_native_model(self):
        """
        Compare with witlab's native Hopf model.
        """
        # run this model
        hopf_multi = self._create_node()
        multi_result = hopf_multi.run(
            DURATION, DT, ZeroInput(hopf_multi.num_noise_variables).as_array(DURATION, DT), backend="numba"
        )
        # run witlab's model
        hopf_witlab = HopfModel(seed=SEED)
        hopf_witlab.params["duration"] = DURATION
        hopf_witlab.params["dt"] = DT
        hopf_witlab.run()
        for var in witlab_VARIABLES_TO_TEST:
            corr_mat = np.corrcoef(hopf_witlab[var], multi_result[var].values.T)
            self.assertTrue(np.greater(corr_mat, CORR_THRESHOLD).all())


class TestHopfNetwork(unittest.TestCase):
    SC = np.array(([[0.0, 1.0], [0.0, 0.0]]))
    DELAYS = np.array([[0.0, 0.0], [0.0, 0.0]])

    def test_init(self):
        hopf = HopfNetwork(self.SC, self.DELAYS)
        self.assertTrue(isinstance(hopf, HopfNetwork))
        self.assertEqual(len(hopf), self.SC.shape[0])
        self.assertEqual(hopf.initial_state.shape[0], hopf.num_state_variables)
        self.assertEqual(hopf.default_output, "x")

    def test_run(self):
        hopf = HopfNetwork(self.SC, self.DELAYS)
        all_results = []
        for backend, noise_func in BACKENDS_TO_TEST.items():
            result = hopf.run(
                DURATION,
                DT,
                noise_func(ZeroInput(hopf.num_noise_variables), DURATION, DT),
                backend=backend,
            )
            self.assertTrue(isinstance(result, xr.Dataset))
            self.assertEqual(len(result), hopf.num_state_variables / hopf.num_nodes)
            self.assertTrue(all(result[result_].shape == (int(DURATION / DT), hopf.num_nodes) for result_ in result))
        all_results.append(result)
        # test results are the same from different backends
        for state_var in all_results[0]:
            corr_mat = np.corrcoef(
                np.vstack([result[state_var].values.flatten().astype(float) for result in all_results])
            )
            self.assertTrue(np.greater(corr_mat, CORR_THRESHOLD).all())

    def test_compare_w_witlab_native_model(self):
        """
        Compare with witlab's native Hopf model.
        """
        # run this model - default is diffusive coupling
        hopf_multi = HopfNetwork(self.SC, self.DELAYS, seed=SEED)
        multi_result = hopf_multi.run(
            DURATION, DT, ZeroInput(hopf_multi.num_noise_variables).as_array(DURATION, DT), backend="numba"
        )
        # run witlab's model
        hopf_witlab = HopfModel(Cmat=self.SC, Dmat=self.DELAYS, seed=SEED)
        hopf_witlab.params["duration"] = DURATION
        hopf_witlab.params["dt"] = DT
        # there is no "global coupling" parameter in MultiModel
        hopf_witlab.params["K_gl"] = 1.0
        # delays <-> length matrix
        hopf_witlab.params["signalV"] = 1.0
        hopf_witlab.params["coupling"] = "diffusive"
        hopf_witlab.params["sigma_ou"] = 0.0
        hopf_witlab.params["xs_init"] = hopf_multi.initial_state[::2][:, np.newaxis]
        hopf_witlab.params["ys_init"] = hopf_multi.initial_state[1::2][:, np.newaxis]
        hopf_witlab.run()
        for var in witlab_VARIABLES_TO_TEST:
            corr_mat = np.corrcoef(hopf_witlab[var], multi_result[var].values.T)
            self.assertTrue(np.greater(corr_mat, CORR_THRESHOLD).all())


if __name__ == "__main__":
    unittest.main()
