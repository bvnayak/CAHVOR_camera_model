#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy
from numpy.testing import assert_almost_equal
import get_cahvor


def test_get_cahvor():
    r_matrix = get_cahvor.compute_rotation_matrix(-72.2993175, 44.2841281,
                                                  166.5327547)
    pinhole_model = dict([('center', [3.451904, 3.258335, 1.254338]),
                          ('image_size', [506, 762]),
                          ('pixelsize', 0.01838),
                          ('rotation_mat', r_matrix),
                          ('f', 29.4711992),
                          ('principal', [-0.09574394, -0.11071695]),
                          ('K', [0.0002, -0.00012443, 0.00000011]),
                          ('az', 0), ('el', 0)])
    cahvor = get_cahvor.compute_CAHVOR(pinhole_model)

    assert cahvor['hs'] == 1603.4384766050055
    assert cahvor['vs'] == 1603.4384766050055
    assert cahvor['hc'] == 375.79086289445047
    assert cahvor['vc'] == 259.0237731229597
    assert_almost_equal(cahvor['C'] , [3.451904, 3.258335, 1.254338])
    assert_almost_equal(cahvor['A'] , [-0.698217, -0.6819946, -0.21766119])
    assert_almost_equal(cahvor['H'] , [-1378.70002113, 894.469724,
                                       -106.50767804])
    assert_almost_equal(cahvor['V'] , [86.47420373, 49.07120279,
                                       -1621.17935234])
    assert_almost_equal(cahvor['O'] , [-0.698217, -0.6819946, -0.21766119])
    assert_almost_equal(cahvor['R'] , [0.0002, -0.10807387, 0.082982])
