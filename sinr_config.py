class SINRConfig:
    # transmission power
    power = 1.0

    # path-loss exponent
    alpha = 2

    # SINR threshold
    beta = 1.0

    # background noise model
    noise = lambda _ : 0.1
