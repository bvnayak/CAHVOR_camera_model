import numpy as np
import math


class CAHVORModel(object):

    def __init__(self):
        print("--------------------------------------------------------------")
        print('Note: Enter Vector Elements Row by Row with Space in between')
        print("--------------------------------------------------------------")
        print("")
        self.C = input('Enter C Vector: ')
        self.C = [float(x) for x in self.C.split()]
        self.A = input('Enter A Vector: ')
        self.A = [float(x) for x in self.A.split()]
        self.H = input('Enter H Vector: ')
        self.H = [float(x) for x in self.H.split()]
        self.V = input('Enter V Vector: ')
        self.V = [float(x) for x in self.V.split()]
        self.O = input('Enter O Vector: ')
        self.O = [float(x) for x in self.O.split()]
        self.R = input('Enter R Vector: ')
        self.R = [float(x) for x in self.R.split()]
        self.pixelsize = float(input('Enter pixel size in mm: '))
        self.imsize = input('Enter Image Size (Row, Column): ')
        self.imsize = [float(x) for x in self.imsize.split()]

        self.hs = float(input('Enter hs: '))
        self.vs = float(input('Enter vs: '))
        self.hc = float(input('Enter hc: '))
        self.vc = float(input('Enter vc: '))
        print("")

        self.r_matrix = compute_rotation_matrix(self.A, self.H, self.V,
                                                self.hs, self.vs, self.hc,
                                                self.vc)
        cahvor_model = dict([('C', self.C),
                             ('A', self.A),
                             ('H', self.H),
                             ('V', self.V),
                             ('O', self.O),
                             ('R', self.R),
                             ('hs', self.hs),
                             ('vs', self.vs),
                             ('hc', self.hc),
                             ('vc', self.vc),
                             ('imsize', self.imsize),
                             ('pixel_size', self.pixelsize),
                             ('r_matrix', self.r_matrix),
                             ])
        self.photogrammetric = compute_photogrammetric(cahvor_model)
        print_photogrammetric(self.photogrammetric)


def compute_rotation_matrix(A, H, V, hs, vs, hc, vc):
    '''
    ############################################
    # self.rotation = Rotational Matrix M      #
    #                                          #
    #                 [  H' ]                  #
    #             M = [ -V' ]                  #
    #                 [ -A  ]                  #
    #                                          #
    ############################################
    '''

    # Compute H'
    H_n = (np.array(H) - (hc * np.array(A))) / hs

    # Compute V'
    V_n = (np.array(V) - (vc * np.array(A))) / vs

    # Rotational Matrix M generation
    r_matrix = np.zeros((3, 3))
    r_matrix[0, :] = H_n
    r_matrix[1, :] = - V_n
    r_matrix[2, :] = - np.array(A)

    return r_matrix


def compute_photogrammetric(CAHVOR_model):
    M = CAHVOR_model['r_matrix']
    f = CAHVOR_model['pixel_size'] * CAHVOR_model['hs']

    # camera center
    Xc = CAHVOR_model['C'][0]
    Yc = CAHVOR_model['C'][1]
    Zc = CAHVOR_model['C'][2]

    # angles
    phi = math.asin(CAHVOR_model['r_matrix'][2][0])
    w = - math.asin(CAHVOR_model['r_matrix'][2][1] / math.cos(phi))
    k = math.acos(CAHVOR_model['r_matrix'][0][0] / math.cos(phi))

    w = math.degrees(w)
    phi = math.degrees(phi)
    k = math.degrees(k)

    k0 = CAHVOR_model['R'][0]
    k1 = CAHVOR_model['R'][1] / (f**2)
    k2 = CAHVOR_model['R'][2] / (f**4)

    x0 = CAHVOR_model['pixel_size'] * (CAHVOR_model['hc'] - (CAHVOR_model['imsize'][1]/2))
    y0 = - CAHVOR_model['pixel_size'] * (CAHVOR_model['vc'] - (CAHVOR_model['imsize'][0]/2))

    photogrammetric = dict([('M', M), ('f', f), ('Xc', Xc), ('Yc', Yc),
                            ('Zc', Zc), ('w', w), ('phi', phi), ('k', k),
                            ('k0', k0), ('k1', k1), ('k2', k2), ('x0', x0),
                            ('y0', y0)])
    return photogrammetric


def print_photogrammetric(photogrammetric):
    print("--------------------------------------------------------------")
    print("")
    print("f: ", photogrammetric['f'])
    print("Xc: ", photogrammetric['Xc'])
    print("Yc: ", photogrammetric['Yc'])
    print("Zc: ", photogrammetric['Zc'])
    print("x0: ", photogrammetric['x0'])
    print("y0: ", photogrammetric['y0'])

    # print('Rotation Matrix: ', photogrammetric['M'])
    print('Angle w (deg): ', photogrammetric['w'])
    print('Angle phi (deg): ', photogrammetric['phi'])
    print('Angle k (deg): ', photogrammetric['k'])

    print('k0: ', photogrammetric['k0'])
    print('k1: ', photogrammetric['k1'])
    print('k2: ', photogrammetric['k2'])
    print("")
    print("--------------------------------------------------------------")

if __name__ == '__main__':
    camera_matrix = CAHVORModel()
