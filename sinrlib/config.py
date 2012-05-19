class Config:
    # transmission power
    power = 1.0

    # path-loss exponent
    alpha = 2

    # SINR threshold
    beta = 1.0

    # background noise model
    noise = lambda _ : 1.0
    
    range = 1.0
