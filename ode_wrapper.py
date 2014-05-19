"""
Utility functions around scikits.odes
"""

import logging

CVODE_RETURN_FLAGS = {
    0 :  "SUCCESS",
    1 :  "TSTOP_RETURN", # Reached specified stopping point
    2 :  "ROOT_RETURN", # Found one or more roots
    99 : "WARNING", # Succeeded but something unusual happened
    -1 : "TOO_MUCH_WORK", # Could not reach endpoint
    -2 : "TOO_MUCH_ACC", # Could not satisfy accuracy
    -3 : "ERR_FAILURE", # Error test failures occurred too many times during one internal time step or minimum step size was reached.
    -4 : "CONV_FAILURE",       # Convergence test failures occurred too many times during one internal time step or minimum step size was reached.
    -5 : "LINIT_FAIL",         # The linear solver’s initialization function failed.
    -6 : "LSETUP_FAIL",        # The linear solver’s setup function failed in an unrecoverable manner.
    -7 : "LSOLVE_FAIL",        # The linear solver’s solve function failed in an unrecoverable manner.
    -8 : "RHSFUNC_FAIL",       # The right-hand side function failed in an unrecoverable manner.
    -9 : "FIRST_RHSFUNC_ERR",  # The right-hand side function failed at the first call.
    -10 : "REPTD_RHSFUNC_ERR", # The right-hand side function had repeated recoverable errors.
    -11 : "UNREC_RHSFUNC_ERR", # The right-hand side function had a recoverable error, but no recovery is possible.
    -12 : "RTFUNC_FAIL",       # The rootfinding function failed in an unrecoverable manner.
    -20 : "MEM_FAIL",          # A memory allocation failed.
    -21 : "MEM_NULL",          # The cvode_mem argument was NULL.
    -22 : "ILL_INPUT",         # One of the function inputs is illegal.
    -23 : "NO_MALLOC",         # The cvode memory block was not allocated by a call to CVodeMalloc.
    -24 : "BAD_K",             # The derivative order k is larger than the order used.
    -25 : "BAD_T",             # The time t is outside the last step taken.
    -26 : "BAD_DKY",           # The output derivative vector is NULL.
    -27 : "TOO_CLOSE",         # The output and initial times are too close to each other.
}

CVODE_ERROR_HUMAN_READABLE = {
    "WARNING": "Something unusual happened at {}, with values {}",
    "TOO_MUCH_WORK": "Could not reach endpoint, ended at {}, with values {}",
    "TOO_MUCH_ACC": "Could not reach required level of accuracy, ended at {}, with values {}",
}

CVODE_UNKNOWN_FLAG_MESSAGE = "Unknown CVODE flag returned with value {}"

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def validate_cvode_flags(flag, x_vals, y_vals, x_err, y_err):
    if flag not in CVODE_RETURN_FLAGS:
        raise NotImplementedError(CVODE_UNKNOWN_FLAG_MESSAGE.format(flag))
    elif CVODE_RETURN_FLAGS[flag] == "SUCCESS":
        return y_vals
    elif CVODE_RETURN_FLAGS[flag] == "WARNING":
        log.warn(CVODE_ERROR_HUMAN_READABLE["WARNING"].format(x_err, y_err))
        return y_vals
    elif CVODE_RETURN_FLAGS[flag] == "TOO_MUCH_WORK":
        msg = CVODE_ERROR_HUMAN_READABLE["TOO_MUCH_WORK"].format(x_err, y_err)
        log.error(
            msg + "y_vals: " + str(y_vals) + " " + "x_vals: " + str(x_vals)
        )
        raise RuntimeError(msg)
    elif CVODE_RETURN_FLAGS[flag] == "TOO_MUCH_ACC":
        msg = CVODE_ERROR_HUMAN_READABLE["TOO_MUCH_ACC"].format(x_err, y_err)
        log.error(
            msg + "y_vals: " + str(y_vals) + " " + "x_vals: " + str(x_vals)
        )
        raise RuntimeError(msg)
    else:
        msg = CVODE_RETURN_FLAGS[flag]
        if flag < 0:
            log.error(msg)
            raise RuntimeError(msg)
        else:
            log.warn(msg)
            return y_vals
