from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import date

class OverviewDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Vue d'ensemble annuelle")
        self.setMinimumWidth(600)
        self.setup_ui()
        self.update_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Sélecteur d'année
        year_layout = QHBoxLayout()
        year_label = QLabel("Année:")
        self.year_combo = QComboBox()
        
        # Remplir les années depuis la première dépense jusqu'à l'année courante
        current_year = date.today().year
        for year in range(current_year - 4, current_year + 1):
            self.year_combo.addItem(str(year), year)
        
        # Sélectionner l'année courante
        current_year_index = self.year_combo.findData(current_year)
        self.year_combo.setCurrentIndex(current_year_index)
        
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_combo)
        year_layout.addStretch()

        # Labels pour les totaux
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)

        value_font = QFont()
        value_font.setPointSize(24)

        # Revenus
        income_layout = QVBoxLayout()
        income_title = QLabel("Total des revenus")
        income_title.setFont(title_font)
        income_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.income_value = QLabel()
        self.income_value.setFont(value_font)
        self.income_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.income_value.setStyleSheet("color: #2ecc71;")  # Vert
        income_layout.addWidget(income_title)
        income_layout.addWidget(self.income_value)

        # Dépenses
        expenses_layout = QVBoxLayout()
        expenses_title = QLabel("Total des dépenses")
        expenses_title.setFont(title_font)
        expenses_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.expenses_value = QLabel()
        self.expenses_value.setFont(value_font)
        self.expenses_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.expenses_value.setStyleSheet("color: #e74c3c;")  # Rouge
        expenses_layout.addWidget(expenses_title)
        expenses_layout.addWidget(self.expenses_value)

        # Dépenses exceptionnelles
        exceptional_layout = QVBoxLayout()
        exceptional_title = QLabel("Dépenses exceptionnelles")
        exceptional_title.setFont(title_font)
        exceptional_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.exceptional_value = QLabel()
        self.exceptional_value.setFont(value_font)
        self.exceptional_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.exceptional_value.setStyleSheet("color: #f39c12;")  # Orange
        exceptional_layout.addWidget(exceptional_title)
        exceptional_layout.addWidget(self.exceptional_value)

        # Solde final
        balance_layout = QVBoxLayout()
        balance_title = QLabel("Solde annuel")
        balance_title.setFont(title_font)
        balance_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balance_value = QLabel()
        self.balance_value.setFont(value_font)
        self.balance_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        balance_layout.addWidget(balance_title)
        balance_layout.addWidget(self.balance_value)

        # Assemblage
        layout.addLayout(year_layout)
        layout.addSpacing(20)
        layout.addLayout(income_layout)
        layout.addSpacing(20)
        layout.addLayout(expenses_layout)
        layout.addLayout(exceptional_layout)
        layout.addSpacing(20)
        layout.addLayout(balance_layout)

        # Connexion du signal
        self.year_combo.currentIndexChanged.connect(self.update_data)

    def update_data(self):
        selected_year = self.year_combo.currentData()
        start_date = date(selected_year, 1, 1)
        end_date = date(selected_year, 12, 31)

        # Calcul des revenus annuels
        total_income = self.db.get_annual_income(start_date, end_date)
        self.income_value.setText(f"+{total_income:.2f} €")

        # Calcul des dépenses annuelles (incluant les charges récurrentes)
        total_expenses = self.db.get_annual_expenses(start_date, end_date)
        self.expenses_value.setText(f"-{total_expenses:.2f} €")

        # Calcul des dépenses exceptionnelles
        exceptional_expenses = self.db.get_exceptional_expenses(start_date, end_date)
        total_exceptional = sum(expense[2] for expense in exceptional_expenses)
        self.exceptional_value.setText(f"-{total_exceptional:.2f} €")

        # Calcul du solde (en excluant les dépenses exceptionnelles du total)
        balance = total_income - (total_expenses - total_exceptional)
        self.balance_value.setText(f"{balance:+.2f} €")
        if balance >= 0:
            self.balance_value.setStyleSheet("color: #2ecc71;")  # Vert
        else:
            self.balance_value.setStyleSheet("color: #e74c3c;")  # Rouge 