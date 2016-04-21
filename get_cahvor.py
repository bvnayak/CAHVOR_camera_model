import numpy as np
import math


class PhotogrammetricModel(object):

    def __init__(self, dict_ip=None):
        if dict_ip is None:
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
            pinhole_model = dict([('C', self.center),
                                  ('imsize', self.imsize),
                                  ('pixel_size', self.pixelsize),
                                  ('r_mat', self.r_matrix),
                                  ('f', self.focallength),
                                  ('P', self.principal),
                                  ('K', self.distortion)])
        else:
            pinhole_model = dict([('C', dict_ip['center']),
                                  ('imsize', dict_ip['image_size']),
                                  ('pixel_size', dict_ip['pixelsize']),
                                  ('r_mat', dict_ip['rotation_mat']),
                                  ('f', dict_ip['f']),
                                  ('P', dict_ip['principal']),
                                  ('K', None)])

        self.cahvor = compute_CAHVOR(pinhole_model)
        print_CAHVOR(self.cahvor)


def compute_rotation_matrix(w, phi, k):
    '''
    ##################################################################################################
    # self.rotation = Rotational Matrix M                                                            #
    #                                                                                                #
    #     [cos(phi)cos(k)   sin(w)sin(phi)cos(k)+cos(w)sin(k)   -cos(w)sin(phi)cos(k)+sin(w)sin(k)]  #
    # M = [-cos(phi)sin(k)  -sin(w)sin(phi)sin(k)+cos(w)cos(k)  cos(w)sin(phi)sin(k)+sin(w)cos(k) ]  #
    #     [   sin(phi)              -sin(w)cos(phi)                        cos(w)cos(phi)         ]  #
    #                                                                                                #
    ##################################################################################################
    '''

    # Degree to Radians
    w = math.radians(w)
    phi = math.radians(phi)
    k = math.radians(k)

    # Rotational Matrix M generation
    r_matrix = np.zeros((3, 3))
    r_matrix[0, 0] = math.cos(phi) * math.cos(k)
    r_matrix[0, 1] = math.sin(w) * math.sin(phi) * math.cos(k) + math.cos(w) * math.sin(k)
    r_matrix[0, 2] = - math.cos(w) * math.sin(phi) * math.cos(k) + math.sin(w) * math.sin(k)
    r_matrix[1, 0] = - math.cos(phi) * math.sin(k)
    r_matrix[1, 1] = - math.sin(w) * math.sin(phi) * math.sin(k) + math.cos(w) * math.cos(k)
    r_matrix[1, 2] = math.cos(w) * math.sin(phi) * math.sin(k) + math.sin(w) * math.cos(k)
    r_matrix[2, 0] = math.sin(phi)
    r_matrix[2, 1] = - math.sin(w) * math.cos(phi)
    r_matrix[2, 2] = math.cos(w) * math.cos(phi)

    return r_matrix


def compute_CAHVOR(pinhole_model):
    hs = pinhole_model['f'] / pinhole_model['pixel_size']
    vs = pinhole_model['f'] / pinhole_model['pixel_size']
    hc = (pinhole_model['imsize'][1] / 2) + (pinhole_model['P'][0] / pinhole_model['pixel_size'])
    vc = (pinhole_model['imsize'][0] / 2) - (pinhole_model['P'][1] / pinhole_model['pixel_size'])

    C = pinhole_model['C']
    A = - pinhole_model['r_mat'][2, :]
    Hn = pinhole_model['r_mat'][0, :]
    Vn = - pinhole_model['r_mat'][1, :]

    H = hs * Hn + hc * A
    V = vs * Vn + vc * A
    O = A        # We assume O = A in converted CAHVOR Model
    R = pinhole_model['K']
    if not(R is None):
        R = np.array([R[0], R[1] * (pinhole_model['f']**2),
                      R[2] * (pinhole_model['f']**4)])
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
    cahvor = PhotogrammetricModel()
