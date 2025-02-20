from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox,
                           QCalendarWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat
from datetime import datetime, date

class IncomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un revenu")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Montant
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Montant:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("1791.91")
        self.amount_input.setFixedWidth(200)  # Largeur fixe pour le champ montant
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        amount_layout.addStretch()  # Pour aligner à gauche

        # Date
        date_layout = QVBoxLayout()
        date_label = QLabel("Date de réception:")
        self.calendar = QCalendarWidget()
        
        # Configuration du calendrier
        self.calendar.setGridVisible(True)
        self.calendar.setMaximumDate(QDate.currentDate())
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        self.calendar.setFixedHeight(250)  # Hauteur fixe plus petite
        self.calendar.setFixedWidth(350)   # Largeur fixe
        
        # Griser les dates futures
        disabled_format = QTextCharFormat()
        disabled_format.setForeground(Qt.GlobalColor.gray)
        disabled_format.setBackground(Qt.GlobalColor.lightGray)

        current_date = QDate.currentDate()
        future_date = current_date.addDays(1)
        while future_date.year() == current_date.year():
            self.calendar.setDateTextFormat(future_date, disabled_format)
            future_date = future_date.addDays(1)

        date_layout.addWidget(date_label)
        date_layout.addWidget(self.calendar)
        date_layout.setAlignment(self.calendar, Qt.AlignmentFlag.AlignHCenter)  # Centrer le calendrier

        # Description
        desc_layout = QHBoxLayout()
        desc_label = QLabel("Description:")
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Salaire")
        self.desc_input.setFixedWidth(200)  # Largeur fixe pour le champ description
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        desc_layout.addStretch()  # Pour aligner à gauche

        # Boutons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        cancel_btn = QPushButton("Annuler")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        # Ajout des layouts au layout principal
        layout.addLayout(amount_layout)
        layout.addLayout(date_layout)
        layout.addLayout(desc_layout)
        layout.addSpacing(10)  # Espace avant les boutons
        layout.addLayout(button_layout)

        # Définir une taille raisonnable pour la fenêtre
        self.setFixedWidth(400)
        self.setFixedHeight(450)  # Hauteur réduite

    def get_income_data(self):
        try:
            # Nettoyer et normaliser le montant (remplacer la virgule par un point)
            amount_text = self.amount_input.text().replace('€', '').strip()
            amount_text = amount_text.replace(',', '.')
            amount = float(amount_text)
            
            # Récupérer la date du calendrier
            selected_date = self.calendar.selectedDate()
            date = datetime(selected_date.year(), selected_date.month(), selected_date.day())
            
            description = self.desc_input.text().strip()
            
            if amount <= 0:
                QMessageBox.warning(self, "Erreur", 
                    "Le montant doit être supérieur à 0.")
                return None
            
            return {
                'amount': amount,
                'date': date,
                'description': description
            }
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", 
                "Format invalide. Vérifiez le format du montant.")
            return None 