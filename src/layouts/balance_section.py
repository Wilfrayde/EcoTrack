from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class BalanceSection(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.balance_label = QLabel()
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(48)
        font.setBold(True)
        self.balance_label.setFont(font)
        
        self.previous_balance_label = QLabel()
        self.previous_balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prev_font = QFont()
        prev_font.setPointSize(12)
        self.previous_balance_label.setFont(prev_font)
        
        self.addWidget(self.balance_label)
        self.addWidget(self.previous_balance_label)

    def update_balance(self, balance: float):
        """Met à jour l'affichage du solde actuel"""
        self.balance_label.setText(self.parent.db.format_amount(balance))
        if balance >= 0:
            self.balance_label.setStyleSheet("color: #2ecc71;")  # Vert
        else:
            self.balance_label.setStyleSheet("color: #e74c3c;")  # Rouge

    def update_previous_balance(self, balance: float, start_date=None, end_date=None):
        """Met à jour l'affichage du solde précédent"""
        # Vérifier s'il y a des données pour le mois précédent
        if self.parent and self.parent.db and start_date and end_date:
            has_previous_data = self.parent.db.has_period_data(start_date, end_date)
            
            if not has_previous_data:
                self.previous_balance_label.setText("Premier mois d'utilisation")
                self.previous_balance_label.setStyleSheet("color: rgba(255, 255, 255, 0.5);")
                return

        # Affichage normal si des données existent
        if balance > 0:
            text = f"Argent économisé le mois dernier : +{balance:.2f} €"
            color = "rgba(46, 204, 113, 0.7)"  # Vert semi-transparent
        else:
            text = f"Dépassement le mois dernier : {balance:.2f} €"
            color = "rgba(231, 76, 60, 0.7)"  # Rouge semi-transparent
        
        self.previous_balance_label.setText(text)
        self.previous_balance_label.setStyleSheet(f"color: {color};") 