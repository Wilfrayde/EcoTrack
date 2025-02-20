from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox,
                           QComboBox, QCheckBox)
from PyQt6.QtCore import Qt
from datetime import datetime

class ExpenseDialog(QDialog):
    def __init__(self, parent=None, categories=None, expense=None):
        super().__init__(parent)
        self.categories = categories or []
        self.expense = expense
        self.setWindowTitle("Ajouter une dépense" if not expense else "Modifier la dépense")
        self.setup_ui()
        if expense:
            self.load_expense_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Description
        desc_layout = QHBoxLayout()
        desc_label = QLabel("Description:")
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Restaurant")
        self.desc_input.setFixedWidth(200)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        desc_layout.addStretch()

        # Montant
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Montant:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("25.50")
        self.amount_input.setFixedWidth(200)
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        amount_layout.addStretch()

        # Catégorie
        cat_layout = QHBoxLayout()
        cat_label = QLabel("Catégorie:")
        self.cat_combo = QComboBox()
        self.cat_combo.setFixedWidth(200)
        for category in self.categories:
            self.cat_combo.addItem(category[1], category[0])  # name, id
        cat_layout.addWidget(cat_label)
        cat_layout.addWidget(self.cat_combo)
        cat_layout.addStretch()

        # Exceptionnel
        exceptional_layout = QHBoxLayout()
        self.exceptional_checkbox = QCheckBox("Dépense exceptionnelle")
        exceptional_layout.addWidget(self.exceptional_checkbox)
        exceptional_layout.addStretch()

        # Boutons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        cancel_btn = QPushButton("Annuler")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        # Assemblage
        layout.addLayout(desc_layout)
        layout.addLayout(amount_layout)
        layout.addLayout(cat_layout)
        layout.addLayout(exceptional_layout)
        layout.addSpacing(10)
        layout.addLayout(button_layout)

        self.setFixedWidth(400)

    def load_expense_data(self):
        self.desc_input.setText(self.expense[1])  # description
        self.amount_input.setText(str(self.expense[2]))  # amount
        index = self.cat_combo.findData(self.expense[4])  # category_id
        if index >= 0:
            self.cat_combo.setCurrentIndex(index)
        self.exceptional_checkbox.setChecked(bool(self.expense[5]))  # is_exceptional

    def get_expense_data(self):
        try:
            description = self.desc_input.text().strip()
            if not description:
                raise ValueError("La description est obligatoire")

            amount = self.parent().db.parse_amount(self.amount_input.text())
            if amount <= 0:
                raise ValueError("Le montant doit être supérieur à 0")
            
            category_id = self.cat_combo.currentData()
            
            return {
                'description': description,
                'amount': amount,
                'date': datetime.now(),  # Utilise automatiquement la date du jour
                'category_id': category_id,
                'is_exceptional': self.exceptional_checkbox.isChecked()
            }
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))
            return None 