import numpy as np
import math
from compute_coordinates import compute_coordinates


class CAHVOR(object):

    def __init__(self):
        print("----------------------------------------------------------")
        print('Note: Enter Vector Inputs Row by Row with Space in between')
        print("----------------------------------------------------------")
        print("")
        self.principal = input('Enter Principal Point (x0, y0): ')
        self.principal = [float(x) for x in self.principal.split()]
        self.imsize = input('Enter Image Size (Row, Column): ')
        self.imsize = [float(x) for x in self.imsize.split()]
        self.focallength = float(input('Enter Focal Length in mm: '))
        self.center = input('Enter Camera Center (Xc, Yc, Zc): ')
        self.center = [float(x) for x in self.center.split()]
        self.pixelsize = float(input('Enter pixel size in mm: '))
        w = float(input('Enter Rotation Angle w: '))
        phi = float(input('Enter Rotation Angle phi: '))
        k = float(input('Enter Rotation Angle k: '))
        self.distortion = input('Enter Distortion Parameters (k0, k1, k2): ')
        self.distortion = [float(x) for x in self.distortion.split()]
        print("")
        self.r_matrix = compute_rotation_matrix(w, phi, k)
        pinhole_model = dict([('center', self.center),
                              ('image_size', self.imsize),
                              ('pixelsize', self.pixelsize),
                              ('rotation_mat', self.r_matrix),
                              ('f', self.focallength),
                              ('principal', self.principal),
                              ('K', self.distortion),
                              ('az', 0), ('el', 0)])

        self.cahvor = compute_CAHVOR(pinhole_model)
        print_CAHVOR(self.cahvor)


def compute_rotation_matrix(w, phi, k):
    """
    Computes Rotation matrix from the rotation angle w, phi, k
    related to x, y and z.

    Returns
    -------
    r_matrix: Rotational Matrix M

         [cos(phi)cos(k)   sin(w)sin(phi)cos(k)+cos(w)sin(k)   -cos(w)sin(phi)cos(k)+sin(w)sin(k)]
     M = [-cos(phi)sin(k)  -sin(w)sin(phi)sin(k)+cos(w)cos(k)  cos(w)sin(phi)sin(k)+sin(w)cos(k) ]
         [   sin(phi)              -sin(w)cos(phi)                        cos(w)cos(phi)         ]

    """

    # Degree to Radians
    w = math.radians(w)
    phi = math.radians(phi)
    k = math.radians(k)

    # Rotational Matrix M generation
    r_matrix = np.zeros((3, 3))
    r_matrix[0, 0] = math.cos(phi) * math.cos(k)
    r_matrix[0, 1] = math.sin(w) * math.sin(phi) * math.cos(k) + \
        math.cos(w) * math.sin(k)
    r_matrix[0, 2] = - math.cos(w) * math.sin(phi) * math.cos(k) + \
        math.sin(w) * math.sin(k)
    r_matrix[1, 0] = - math.cos(phi) * math.sin(k)
    r_matrix[1, 1] = - math.sin(w) * math.sin(phi) * math.sin(k) + \
        math.cos(w) * math.cos(k)
    r_matrix[1, 2] = math.cos(w) * math.sin(phi) * math.sin(k) + \
        math.sin(w) * math.cos(k)
    r_matrix[2, 0] = math.sin(phi)
    r_matrix[2, 1] = - math.sin(w) * math.cos(phi)
    r_matrix[2, 2] = math.cos(w) * math.cos(phi)

    return r_matrix


def compute_CAHVOR(pinhole_model):
    """
    Computation of CAHVOR from photogrammetric parameters.

    Parameters
    ----------
    dict: dict
        Take dictionary containing photogrammetric camera Parameters
        such as 'camera center', 'focallength', 'rotation matrix',
        'pixel size', 'principal point', 'image size' and 'az' and 'el'
        to get back to origin position of PTU.

    Returns:
    cahvor: dict
        Returns dict containing computed CAHVOR parameters from
        photogrammetric model.
    """
    hs = pinhole_model['f'] / pinhole_model['pixelsize']
    vs = pinhole_model['f'] / pinhole_model['pixelsize']
    hc = (pinhole_model['image_size'][1] / 2) + \
         (pinhole_model['principal'][0] / pinhole_model['pixelsize'])
    vc = (pinhole_model['image_size'][0] / 2) - \
         (pinhole_model['principal'][1] / pinhole_model['pixelsize'])

    C = pinhole_model['center']
    A = - pinhole_model['rotation_mat'][2, :]
    Hn = pinhole_model['rotation_mat'][0, :]
    Vn = - pinhole_model['rotation_mat'][1, :]

    H = hs * Hn + hc * A
    V = vs * Vn + vc * A
    O = A        # We assume O = A in converted CAHVOR Model

    # Fixing Axis specifically for PTU unit.
    A[0], A[1], A[2] = A[2], -A[0], -A[1]
    H[0], H[1], H[2] = H[2], -H[0], -H[1]
    V[0], V[1], V[2] = V[2], -V[0], -V[1]
    O[0], O[1], O[2] = O[2], -O[0], -O[1]

    A = compute_coordinates(A, pinhole_model['az'], pinhole_model['el'])
    H = compute_coordinates(H, pinhole_model['az'], pinhole_model['el'])
    V = compute_coordinates(V, pinhole_model['az'], pinhole_model['el'])
    O = compute_coordinates(O, pinhole_model['az'], pinhole_model['el'])

    try:
        R = pinhole_model['K']
    except KeyError:
        R = None

    if not (R is None):
        R = np.array([R[0], R[1] * (pinhole_model['f']**2),
                      R[2] * (pinhole_model['f']**4)])
        R = compute_coordinates(R, pinhole_model['az'], pinhole_model['el'])

    cahvor = dict([('C', C), ('A', A), ('H', H), ('V', V), ('O', O), ('R', R),
                   ('hs', hs), ('hc', hc), ('vs', vs), ('vc', vc)])
    return cahvor


def print_CAHVOR(cahvor):
    print("--------------------------------------------------------------")
    print("")
    print("hs: ", cahvor['hs'])
    print("vs: ", cahvor['vs'])
    print("hc: ", cahvor['hc'])
    print("vc: ", cahvor['vc'])

    print('C: ', cahvor['C'])
    print('A: ', cahvor['A'])
    print('H: ', cahvor['H'])
    print('V: ', cahvor['V'])
    print('O: ', cahvor['O'])
    print('R: ', cahvor['R'])
    print("")
    print("--------------------------------------------------------------")

if __name__ == '__main__':
    cahvor = CAHVOR()
