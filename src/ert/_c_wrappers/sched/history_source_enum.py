from cwrap import BaseCEnum


class HistorySourceEnum(BaseCEnum):
    TYPE_NAME = "history_source_enum"
    REFCASE_SIMULATED = None
    REFCASE_HISTORY = None
    HISTORY_SOURCE_INVALID = None


HistorySourceEnum.addEnum("REFCASE_SIMULATED", 1)
HistorySourceEnum.addEnum("REFCASE_HISTORY", 2)
HistorySourceEnum.addEnum("HISTORY_SOURCE_INVALID", 10)
