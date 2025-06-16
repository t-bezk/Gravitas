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

    "step":         3600*24*1,
    "out_title":    "Mars 2020 Transfer Window",
}

v_2020 = {
    "d_time0":      "2021-04-01T00:00:00",
    "d_time1":      "2022-12-01T00:00:00",
    "a_time0":      "2021-01-01T00:00:00",
    "a_time1":      "2023-01-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*5,
    "out_title":    "Mars 2020",
}

e_2020 = {
    "d_time0":      "2021-01-01T00:00:00",
    "d_time1":      "2023-01-01T00:00:00",
    "a_time0":      "2021-06-01T00:00:00",
    "a_time1":      "2023-12-01T00:00:00",

    "target":       "EARTH BARYCENTER",
    "origin":       "MARS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*5,
    "out_title":    "Mars 2020",
}