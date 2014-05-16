"""
Utility functions around scikits.odes
"""

CVODE_RETURN_FLAGS = {
    0 :  "SUCCESS",
    #1 :  "TSTOP_RETURN", # Reached specified stopping point
    #2 :  "ROOT_RETURN", # Found one or more roots
    99 : "WARNING", # Succeeded but something unusual happened
    -1 : "TOO_MUCH_WORK", # Could not reach endpoint
    -2 : "TOO_MUCH_ACC", # Could not satisfy accuracy
}

CVODE_ERROR_HUMAN_READABLE = {
    "WARNING": "Something unusual happened at {}, with values {}",
    "TOO_MUCH_WORK": "Could not reach endpoint, ended at {}, with values {}",
    "TOO_MUCH_ACC": "Could not reach required level of accuracy, ended at {}, with values {}",
}

CVODE_UNKNOWN_FLAG_MESSAGE = "Unknown CVODE flag returned with value {}"


def validate_cvode_flags(flag, x_vals, y_vals, x_err, y_err):
    if flag not in CVODE_RETURN_FLAGS:
        raise NotImplementedError(CVODE_UNKNOWN_FLAG_MESSAGE.format(flag))
    elif CVODE_RETURN_FLAGS[flag] == "SUCCESS":
        return y_vals
    elif CVODE_RETURN_FLAGS[flag] == "WARNING":
        raise RuntimeWarning(
                CVODE_ERROR_HUMAN_READABLE["WARNING"].format(x_err, y_err)
        )
        return y_vals
    elif CVODE_RETURN_FLAGS[flag] == "TOO_MUCH_WORK":
        raise RuntimeError(
                CVODE_ERROR_HUMAN_READABLE["TOO_MUCH_WORK"].format(x_err, y_err)
        )
    elif CVODE_RETURN_FLAGS[flag] == "TOO_MUCH_ACC":
        raise RuntimeError(
                CVODE_ERROR_HUMAN_READABLE["TOO_MUCH_ACC"].format(x_err, y_err)
        )

