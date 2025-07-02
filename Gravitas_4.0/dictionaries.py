"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - dictionaries module
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""

m_2020 = {
    "d_time0":      "2020-05-01T00:00:00",
    "d_time1":      "2020-09-01T00:00:00",
    "a_time0":      "2020-12-01T00:00:00",
    "a_time1":      "2021-04-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24*5,
    "out_title":    "Mars 2020 Transfer Window",
}

MARINER_10_EV = {
    "d_time0":      "1973-10-01T00:00:00",
    "d_time1":      "1973-12-01T00:00:00",
    "a_time0":      "1974-01-01T00:00:00",
    "a_time1":      "1974-03-01T00:00:00",

    "target":       "VENUS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24,
    "out_title":    "Mariner 10 Earth-Venus Window",
}

MARINER_10_VM = {
    "d_time0":      "1974-01-01T00:00:00",
    "d_time1":      "1974-03-01T00:00:00",
    "a_time0":      "1974-03-10T00:00:00",
    "a_time1":      "1974-05-01T00:00:00",

    "target":       "MERCURY BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24,
    "out_title":    "Mariner 10 Venus-Mercury Window",
}