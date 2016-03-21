import numpy as np
import math


class pinhole_model(object):

    def __init__(self):
        print('Enter Vector/Matrix Elements Row by Row with Space in between')
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

        self.compute_rotation_matrix(w, phi, k)

    def compute_rotation_matrix(self, w, phi, k):
        ##################################################################################################
        # self.rotation = Rotational Matrix M                                                            #
        #                                                                                                #
        #     [cos(phi)cos(k)   sin(w)sin(phi)cos(k)+cos(w)sin(k)   -cos(w)sin(phi)cos(k)+sin(w)sin(k)]  # 
        # M = [-cos(phi)sin(k)  -sin(w)sin(phi)sin(k)+cos(w)cos(k)  cos(w)sin(phi)sin(k)+sin(w)cos(k) ]  #
        #     [   sin(phi)              -sin(w)cos(phi)                        cos(w)cos(phi)         ]  #
        #                                                                                                #
        ##################################################################################################

        # Degree to Radians
        w = math.radians(w)
        phi = math.radians(phi)
        k = math.radians(k)

        self.r_matrix = np.zeros((3, 3))
        self.r_matrix[0, 0] = math.cos(phi) * math.cos(k)
        self.r_matrix[0, 1] = math.sin(w) * math.sin(phi) * math.cos(k) + math.cos(w) * math.sin(k)
        self.r_matrix[0, 2] = - math.cos(w) * math.sin(phi) * math.cos(k) + math.sin(w) * math.sin(k)
        self.r_matrix[1, 0] = - math.cos(phi) * math.sin(k)
        self.r_matrix[1, 1] = - math.sin(w) * math.sin(phi) * math.sin(k) + math.cos(w) * math.cos(k)
        self.r_matrix[1, 2] = math.cos(w) * math.sin(phi) * math.sin(k) + math.sin(w) * math.cos(k)
        self.r_matrix[2, 0] = math.sin(phi)
        self.r_matrix[2, 1] = - math.sin(w) * math.cos(phi)
        self.r_matrix[2, 2] = math.cos(w) * math.cos(phi)

        self.compute_CAHV()

    def compute_CAHV(self):
        hs = self.focallength / self.pixelsize
        vs = self.focallength / self.pixelsize
        hc = (self.imsize[1] / 2) + (self.principal[0] / self.pixelsize)
        vc = (self.imsize[0] / 2) - (self.principal[1] / self.pixelsize)

        A = - self.r_matrix[2, :]
        Hn = self.r_matrix[0, :]
        Vn = - self.r_matrix[1, :]

        H = hs * Hn + hc * A
        V = vs * Vn + vc * A

        print("--------------------------------------------------------------")
        print()
        print("hs: ", hs)
        print("vs: ", vs)
        print("hc: ", hc)
        print("vc: ", vc)

        print('C: ', self.center)
        print('A: ', A)
        print('H: ', H)
        print('V: ', V)
        print()
        print("--------------------------------------------------------------")


if __name__ == '__main__':
    pinhole_model()
