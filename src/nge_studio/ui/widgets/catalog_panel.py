"""Catalog tree panel."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

from nge_studio.catalog.models import Game, Script


class CatalogPanel(QWidget):
    script_selected = Signal(object)  # Script | None

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["游戏 / 脚本"])
        self._tree.setDragEnabled(False)
        self._tree.setSortingEnabled(False)
        self._tree.itemSelectionChanged.connect(self._on_selection)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._tree)
        self._scripts: dict[str, Script] = {}

    def set_games(self, games: list[Game]) -> None:
        self._tree.clear()
        self._scripts.clear()
        for game in games:
            game_item = QTreeWidgetItem([game.display_name])
            game_item.setToolTip(0, (game.manifest.description if game.manifest else None) or game.game_id)
            game_item.setData(0, 256, None)
            for script in game.scripts:
                child = QTreeWidgetItem([script.display_name])
                child.setToolTip(0, script.manifest.description or script.key)
                child.setData(0, 256, script.key)
                self._scripts[script.key] = script
                game_item.addChild(child)
            self._tree.addTopLevelItem(game_item)
            game_item.setExpanded(True)

    def _on_selection(self) -> None:
        items = self._tree.selectedItems()
        if not items:
            self.script_selected.emit(None)
            return
        key = items[0].data(0, 256)
        self.script_selected.emit(self._scripts.get(key) if key else None)
