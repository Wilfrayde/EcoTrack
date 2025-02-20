from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class RecurringChargeDialog(QDialog):
    def __init__(self, parent=None, charge=None):
        super().__init__(parent)
        self.charge = charge
        self.setWindowTitle("Ajouter une charge récurrente" if not charge else "Modifier la charge")
        self.setup_ui()
        if charge:
            self.load_charge_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Nom de la charge
        name_layout = QHBoxLayout()
        name_label = QLabel("Nom:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Loyer")
        self.name_input.setFixedWidth(200)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        name_layout.addStretch()

        # Montant
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Montant:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("750.00")
        self.amount_input.setFixedWidth(200)
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        amount_layout.addStretch()

        # Boutons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        cancel_btn = QPushButton("Annuler")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        # Ajout des layouts au layout principal
        layout.addLayout(name_layout)
        layout.addLayout(amount_layout)
        layout.addSpacing(10)
        layout.addLayout(button_layout)

        self.setFixedWidth(400)

    def load_charge_data(self):
        """Charge les données d'une charge existante"""
        self.name_input.setText(self.charge[1])  # name
        self.amount_input.setText(str(self.charge[2]))  # amount

    def get_charge_data(self):
        try:
            name = self.name_input.text().strip()
            if not name:
                raise ValueError("Le nom est obligatoire")

            amount_text = self.amount_input.text().replace('€', '').strip()
            amount_text = amount_text.replace(',', '.')
            amount = float(amount_text)
            
            if amount <= 0:
                raise ValueError("Le montant doit être supérieur à 0")
            
            return {
                'name': name,
                'amount': amount
            }
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))
            return None 