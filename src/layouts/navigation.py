from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QComboBox, QCheckBox
from PyQt6.QtCore import Qt
from datetime import date

class NavigationLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Navigation période
        self.prev_btn = QPushButton("◀ Période précédente")
        self.period_label = QLabel()
        self.next_btn = QPushButton("Période suivante ▶")
        
        # Style pour les boutons désactivés
        disabled_style = """
            QPushButton:disabled {
                color: #666666;
                background-color: #353535;
                border: 1px solid #666666;
            }
        """
        self.prev_btn.setStyleSheet(disabled_style)
        self.next_btn.setStyleSheet(disabled_style)
        
        # Désactiver les deux boutons par défaut
        self.prev_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        
        if self.parent:
            today = date.today()
            current_period = self.parent.period_controller.get_current_period_start()
            self.next_btn.setEnabled(False)  # Désactivé par défaut pour la période courante
        
        # Filtre catégorie
        filter_label = QLabel("Filtrer par catégorie:")
        self.category_filter = QComboBox()
        self.category_filter.addItem("Toutes les catégories", None)
        if self.parent and self.parent.db:
            categories = self.parent.db.get_categories()
            for category in categories:
                self.category_filter.addItem(category[1], category[0])
        
        # Case à cocher dépenses exceptionnelles
        self.show_exceptional = QCheckBox("Inclure dépenses exceptionnelles")
        self.show_exceptional.setChecked(True)
        # Connexion du signal pour mettre à jour la table
        if self.parent:
            self.show_exceptional.stateChanged.connect(self.parent.update_expenses_table)
            self.category_filter.currentIndexChanged.connect(self.parent.update_expenses_table)
        
        # Assemblage
        self.addWidget(self.prev_btn)
        self.addWidget(self.period_label)
        self.addWidget(self.next_btn)
        self.addStretch()
        self.addWidget(filter_label)
        self.addWidget(self.category_filter)
        self.addWidget(QLabel("|"))  # Séparateur
        self.addWidget(self.show_exceptional) 

    def update_categories(self):
        """Met à jour la liste des catégories"""
        current_category = self.category_filter.currentData()
        self.category_filter.clear()
        self.category_filter.addItem("Toutes les catégories", None)
        
        if self.parent and self.parent.db:
            categories = self.parent.db.get_categories()
            for category in categories:
                self.category_filter.addItem(category[1], category[0])
        
        # Restaurer la sélection précédente si possible
        index = self.category_filter.findData(current_category)
        if index >= 0:
            self.category_filter.setCurrentIndex(index) 

    def update_next_button_state(self, next_period_enabled: bool):
        """Met à jour l'état du bouton période suivante"""
        self.next_btn.setEnabled(next_period_enabled) 

    def update_period_label(self, start_date: date, end_date: date):
        """Met à jour le label de la période"""
        self.period_label.setText(
            f"Période du {start_date.strftime('%d/%m/%Y')} "
            f"au {end_date.strftime('%d/%m/%Y')}"
        ) 