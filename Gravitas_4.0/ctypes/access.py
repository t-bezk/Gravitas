import ctypes as ct

almbert = ct.WinDLL("./Gravitas_4.0/ctypes/lambert.so")

householder = almbert.householder
tof_equation_p = almbert._tof_equation_p


householder.argtypes = [ ct.c_double, ct.c_double, ct.c_double, ct.c_int, ct.c_double, ct.c_int ]
householder.restype = ct.c_double

tof_equation_p.argtypes = [ ct.c_double, ct.c_double, ct.c_double, ct.c_double ]
tof_equation_p.restype = ct.c_double

house = householder(0.5, 100., 0.5, 0, 0.1, 10)
tof = tof_equation_p(0.3, 0.2, 200., 0.5)


print(house)