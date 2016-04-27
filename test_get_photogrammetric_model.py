#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy
from numpy.testing import assert_almost_equal
import get_photogrammetric_model


def test_get_photogrammetric_model():
    cahvor_model = dict([('C', [3.451904, 3.258335, 1.254338]),
                         ('A', [-0.698217, -0.681994, -0.217661]),
                         ('H', [-1378.872803, 894.719666, -106.732689]),
                         ('V', [86.414558, 49.038635, -1620.883789]),
                         ('O', [-0.695858, -0.679843, -0.231508]),
                         ('R', [0.0002, -0.108075, 0.086320]),
                         ('K', [0.0002, -0.00012443, 0.00000011]),
                         ('hs', 1603.741455), ('vs', 1603.1354),
                         ('hc', 375.790863), ('vc', 259.023773),
                         ('imsize', [506, 762]), ('pixel_size', 0.01838),
                         ('az', 0), ('el', 0)])
    cam_model = get_photogrammetric_model.compute_photogrammetric(cahvor_model)

    assert cam_model['f'] == 29.476767942900004
    assert cam_model['Xc'] == 3.451904
    assert cam_model['Yc'] == 3.258335
    assert cam_model['Zc'] == 1.254338
    assert cam_model['x0'] == -0.09574393805999998
    assert cam_model['y0'] == -0.1107169477400001
    assert cam_model['w'] == -72.29916094406916
    assert cam_model['phi'] == 44.28412812851018
    assert cam_model['k'] == 166.5245817162046
    assert cam_model['k0'] == 0.0002
    assert cam_model['k1'] == -0.00012438428650870753
    assert cam_model['k2'] == 1.1433836611397755e-07
