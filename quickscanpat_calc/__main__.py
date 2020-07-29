# imports
import datetime as dt

import numpy as np
import pandas as pd

from .suncone import main as suncone
from ..globalimports import *
from ..scanpat_calc.sunforecaster import sunforecaster


# params

_qspatfunc_d = {
    'suncone': suncone
}
_highsun_l = [
    'suncone'
]


# relevant func
def _prompthighsun_func():
    '''
    Prompts if it is not an optimal time for measurement, in this case when the
    sun is not high enough whether the movement of the sun in minimal
    '''
    sf = sunforecaster(LATITUDE, LONGITUDE, ELEVATION)

    # computing optimal time
    starttime = LOCTIMEFN(dt.datetime.combine(dt.date.today(), dt.time()), UTCINFO)
    endtime = starttime + dt.timedelta(1)
    time_sr = pd.date_range(starttime, endtime, freq='min')  # minute intervals

    thetas_a, _ = sf.get_anglesvec(time_sr)
    angdrift = np.min(thetas_a)
    langthres = angdrift - np.deg2rad(HIGHSUNTHRES)
    hangthres = angdrift + np.deg2rad(HIGHSUNTHRES)
    boo_a = (thetas_a > langthres) * (thetas_a < hangthres)

    time_sr = time_sr[boo_a]
    starttime, endtime = time_sr[0], time_sr[-1]

    # prompting
    print(f'sun angular drift approx {np.rad2deg(angdrift)} deg')
    print(f'optimal time of measurement {starttime} to {endtime}')
    now = LOCTIMEFN(dt.datetime.now(), UTCINFO)

    if now < starttime or now > endtime:
        GETRESPONSEFN(
            f'current time {now} is outside of optimal time, '
            'shall we proceed with measurement?',
            True, True
        )


# main func
@announcer(newlineboo=False)
def main(qstype):
    '''
    Calls the appropriate quick scan function to be called.
    The arguments for the functions are adjusted in their respective scripts
    Scan patterns are written to data directory specified in ..params

    Parameters
        qstype (str): type of scan quick scan pattern

    Return
        scanpat_a (np.array): [deg] array produced by _qspatfunc
                              transforming spherical coordinates to angular
                              coordinates
    '''
    if qstype in _highsun_l:
        _prompt_func()

    dir_a = _qspatfunc_d[qstype]()

    # converting spherical coordinates to lidar coordinates
    scanpat_a = SPHERE2LIDARFN(dir_a[:, 1], dir_a[:, 0], np.deg2rad(ANGOFFSET))
    scanpat_a = np.rad2deg(dir_a)

    return scanpat_a


# testing
if __name__ == '__main__':
    # main()
    _prompthighsun_func()
