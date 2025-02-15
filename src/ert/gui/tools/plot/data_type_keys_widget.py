from qtpy.QtCore import Signal
from qtpy.QtWidgets import QHBoxLayout, QListView, QToolButton, QVBoxLayout, QWidget

from ert.gui.ertwidgets import Legend, SearchBox, resourceIcon

from .data_type_keys_list_model import DataTypeKeysListModel
from .data_type_proxy_model import DataTypeProxyModel
from .filter_popup import FilterPopup


class DataTypeKeysWidget(QWidget):
    dataTypeKeySelected = Signal()

    def __init__(self, key_defs):
        QWidget.__init__(self)

        self.__filter_popup = FilterPopup(self, key_defs)
        self.__filter_popup.filterSettingsChanged.connect(self.onItemChanged)

        layout = QVBoxLayout()

        self.model = DataTypeKeysListModel(key_defs)
        self.filter_model = DataTypeProxyModel(self, self.model)

        filter_layout = QHBoxLayout()

        self.search_box = SearchBox()
        self.search_box.filterChanged.connect(self.setSearchString)
        filter_layout.addWidget(self.search_box)

        filter_popup_button = QToolButton()
        filter_popup_button.setIcon(resourceIcon("filter_list.svg"))
        filter_popup_button.clicked.connect(self.showFilterPopup)
        filter_layout.addWidget(filter_popup_button)
        layout.addLayout(filter_layout)

        self.data_type_keys_widget = QListView()
        self.data_type_keys_widget.setModel(self.filter_model)
        self.data_type_keys_widget.selectionModel().selectionChanged.connect(
            self.itemSelected
        )

        layout.addSpacing(15)
        layout.addWidget(self.data_type_keys_widget, 2)
        layout.addStretch()

        layout.addWidget(
            Legend("Observations available", DataTypeKeysListModel.HAS_OBSERVATIONS)
        )

        self.setLayout(layout)

    def onItemChanged(self, item):
        # self.filter_model.setShowBlockKeys(item["block"])
        for value, visible in item.items():
            self.filter_model.setFilterOnMetadata("data_origin", value, visible)

    def itemSelected(self):
        selected_item = self.getSelectedItem()
        if selected_item is not None:
            self.dataTypeKeySelected.emit()

    def getSelectedItem(self) -> str:
        index = self.data_type_keys_widget.currentIndex()
        source_index = self.filter_model.mapToSource(index)
        item = self.model.itemAt(source_index)
        return item

    def selectDefault(self):
        self.data_type_keys_widget.setCurrentIndex(self.filter_model.index(0, 0))

    def setSearchString(self, _filter):
        self.filter_model.setFilterFixedString(_filter)

    def showFilterPopup(self):
        self.__filter_popup.show()
