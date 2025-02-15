from ert._c_wrappers.enkf.enums import RealizationStateEnum
from ert.storage import StorageReader


def get_runnable_realizations_mask(storage: StorageReader, casename: str):
    """Return the list of IDs corresponding to realizations that can be run.

    A realization is considered "runnable" if its status is any other than
    STATE_PARENT_FAILED. In that case, ERT does not know why that realization
    failed, so it does not even know whether the parameter set for that
    realization is sane or not.
    If the requested case does not exist, an empty list is returned
    """
    try:
        ensemble = storage.get_ensemble_by_name(casename)
    except KeyError:
        return []

    runnable_states = [
        RealizationStateEnum.STATE_UNDEFINED,
        RealizationStateEnum.STATE_INITIALIZED,
        RealizationStateEnum.STATE_LOAD_FAILURE,
        RealizationStateEnum.STATE_HAS_DATA,
    ]
    return ensemble.get_realization_mask_from_state(runnable_states)
