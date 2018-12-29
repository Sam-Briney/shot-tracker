import numpy as np
import mod.Global as Global

def smooth(y):
    rft = np.fft.rfft(y)
    rft[5:] = 0
    y_smooth = np.fft.irfft(rft)
    return y_smooth

def curveFit(shot, xt):
    x = []
    y = []
    time0 = shot[0][1]
    for point in shot:
        if xt == "x":
            x.append(point[0][0])
        else:
            x.append(point[1] - time0)
        y.append(Global.hoopY - point[0][1])

    # xn = np.array(x)

    #remove outliers
    z0 = np.polyfit(np.array(x), np.array(y), 2)

    x_filtered = []
    y_filtered = []

    std_multiple_cutoff = 0.4

    err = []

    i = 0
    for x0 in x:
        y0 = y[i]

        a = z0[0]
        b = z0[1]
        c = z0[2]

        yCalc = a * x0**2 + b * x0 + c

        err.append(abs(yCalc - y0))
        i += 1

    i = 0

    erStd = np.std(err)
    erMean = np.mean(err)

    for er in err:
        if er < (erStd * std_multiple_cutoff + erMean):
            x_filtered.append(x[i])
            y_filtered.append(y[i])
        i += 1

    x = x_filtered
    y = y_filtered

    try:
        # return np.polyfit(xn, np.array(y_smooth), 2)
        return np.polyfit(np.array(x), np.array(y), 2)
    except:
        pass

def filterRaw(shots):
    #remove duplicates
    shots2 = []
    for shot in shots:
        shot2 = []
        for point in shot:
            add = True
            for point2 in shot2:
                if point2 == point:
                    add = False
                    break
            if add:
                shot2.append(point)
        shots2.append(shot2)

    shots3 = []
    for shot in shots2:
        shot3 = [shot[0]]
        for i in range(1, len(shot)):
            if not shot[i][0] == shot[i-1][0]:
                shot3.append(shot[i])

        shots3.append(shot3)

    # remove points that go backwards
    shots4 = []
    for shot in shots3:
        shot4 = [shot[0]]
        # assumes first data point is OK
        for i in range(1, len(shot)):
            if shot[i][0][0] * Global.basketOn < shot[i-1][0][0] * Global.basketOn:
                shot4.append(shot[i])
        shots4.append(shot4)

    # set curves to t=0 at beginning
    shots5 = []
    for shot in shots4:
        times = []
        for point in shot:
            times.append(point[1])
        min_t = min(times)

        shot5 = []

        for point in shot:
            point5 = point
            point5[1] = point5[1] - min_t
            shot5.append(point5)

        shots5.append(shot5)

    # remove all points where t > 1 second
    time_cutoff = 1
    shots6 = []
    for shot in shots5:
        shot6 = []
        for point in shot:
            if point[1] < time_cutoff:
                shot6.append(point)
        shots6.append(shot6)

    #check for linear relationship between x and t -> filter
    shots7 = []
    std_multiple_cutoff = 2.5

    for shot in shots6:
        #fit curve
        t = []
        x = []
        for point in shot:
            t.append(point[1])
            x.append(point[0][0])

        x = np.array(x)
        t = np.array(t)

        z0 = np.polyfit(t, x, 1)

        # calculate error

        #m = slope, B = intercept
        m = z0[0]
        B = z0[1]

        err = []

        for i in range(0, len(t)):
            xCalc = t[i] * m + B
            err.append(abs(x[i] - xCalc))

        err_np = np.array(err)

        err_mean = np.mean(err_np)
        err_std = np.std(err_np)

        err_max = err_mean + (err_std * std_multiple_cutoff)

        shot7 = []
        for i in range(0, len(err)):
            if err[i] < err_max:
                shot7.append(shot[i])

        shots7.append(shot7)

    return shots7



def angle(shot):
    a = shot[0]
    b = shot[1]
    c = shot[2]

    #avoid imaginary numbers
    if (b**2 - 4 * a * c) >= 0:
        x0 = (-1 * b + (b**2 - 4 * a * c)**(0.5))/(2 * a)

        m = 2 * a * x0 + b

        return np.arctan2(m, 1) * 180 / np.pi
    else:
        print "in"

def maxHeight(shot):
    a = shot[0] * -1
    b = shot[1] * -1
    c = shot[2] * -1 + Global.hoopY

    xMax = -b / (2 * a)
    yMax = a * xMax ** 2 + b * xMax + c

    return Global.videoH - yMax

def filterShots(shots, raw_shots):
    shots2 = []

    # filter parabolas that face the wrong way
    for i in range(0, len(shots)):
        shot = shots[i]
        a = shot[0][0]

        if a < 0:
            shots2.append(shot)

    #filter results with ridiculous angles
    shots3 = []

    A = []
    for shot in shots2:
        A.append(shot[0][0])

    A_np = np.array(A)

    a_mean = np.mean(A_np)
    a_std = np.std(A_np)

    std_multiple_cutoff = 2

    for i in range(0, len(A)):
        if A[i] > a_mean - a_std * std_multiple_cutoff and A[i] < a_mean + a_std * std_multiple_cutoff:
            shots3.append(shots2[i])


    return shots3
