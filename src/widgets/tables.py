from PyQt6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt

class ResponsiveTable(QTableWidget):
    def __init__(self, headers, column_widths=None):
        super().__init__()
        self.setup_table(headers, column_widths)

    def setup_table(self, headers, column_widths):
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Configuration par défaut
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.verticalHeader().setVisible(False)

        # Configuration des colonnes
        for i, (header, width) in enumerate(zip(headers, column_widths or [])):
            if width is None:
                self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                self.setColumnWidth(i, width)

    def format_amount(self, amount: float) -> QTableWidgetItem:
        """Crée un QTableWidgetItem formaté pour un montant"""
        item = QTableWidgetItem(f"{amount:.2f} €")
        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return item

class ChargesTable(ResponsiveTable):
    def __init__(self):
        headers = ["Nom", "Montant", "Actions"]
        widths = [None, 100, 200]  # None pour Stretch
        super().__init__(headers, widths)

class ExpensesTable(ResponsiveTable):
    def __init__(self):
        headers = ["Date", "Description", "Montant", "Catégorie", "Actions"]
        widths = [100, None, 100, 100, 200]
        super().__init__(headers, widths)

    def add_total_row(self, total: float):
        """Ajoute une ligne de total au tableau"""
        last_row = self.rowCount()
        self.insertRow(last_row)
        
        # Cellules vides pour Date et Description
        self.setItem(last_row, 0, QTableWidgetItem(""))
        self.setItem(last_row, 1, QTableWidgetItem("Total:"))
        
        # Total
        total_item = QTableWidgetItem(f"{total:.2f} €")
        total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        font = total_item.font()
        font.setBold(True)
        total_item.setFont(font)
        self.setItem(last_row, 2, total_item)
        
        # Cellules vides pour Catégorie et Actions
        self.setItem(last_row, 3, QTableWidgetItem(""))
        self.setItem(last_row, 4, QTableWidgetItem(""))

    def format_amount(self, amount: float) -> QTableWidgetItem:
        """Crée un QTableWidgetItem formaté pour un montant"""
        item = QTableWidgetItem(f"{amount:.2f} €")
        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return item 