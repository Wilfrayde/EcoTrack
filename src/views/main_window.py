from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QMessageBox, QTableWidget,
                           QTableWidgetItem, QHeaderView, QComboBox, QCheckBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
from views.income_dialog import IncomeDialog
from views.recurring_charge_dialog import RecurringChargeDialog
from views.expense_dialog import ExpenseDialog
from utils.database import Database
from datetime import date, datetime, timedelta
from views.overview_dialog import OverviewDialog
from widgets.tables import ChargesTable, ExpensesTable
from layouts.navigation import NavigationLayout
from layouts.balance_section import BalanceSection
from controllers.period_controller import PeriodController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EcoTrack")
        self.setMinimumSize(800, 600)
        
        self.db = Database()
        self.period_controller = PeriodController()
        self.current_period_start = self.period_controller.get_current_period_start()
        
        # Configuration du thème sombre
        self.setup_dark_theme()
        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Navigation
        self.nav_layout = NavigationLayout(self)
        self.nav_layout.prev_btn.clicked.connect(self.go_to_previous_period)
        self.nav_layout.next_btn.clicked.connect(self.go_to_next_period)
        
        # Balance
        self.balance_section = BalanceSection(self)
        
        # Tables
        self.charges_table = ChargesTable()
        self.expenses_table = ExpensesTable()
        
        # Assemblage
        layout.addLayout(self.nav_layout)
        layout.addLayout(self.balance_section)
        layout.addWidget(self.charges_table)
        layout.addWidget(self.expenses_table)

        # Boutons d'action
        action_layout = self.create_action_buttons()

        # Assemblage du layout principal
        layout.addLayout(action_layout)

    def update_display(self):
        end_date = self.period_controller.get_period_end(self.current_period_start)
        
        # Mettre à jour le label de période
        self.nav_layout.update_period_label(self.current_period_start, end_date)
        
        # Vérifier s'il y a des données pour la période précédente
        previous_start = self.period_controller.get_previous_period_start(self.current_period_start)
        previous_end = self.period_controller.get_period_end(previous_start)
        has_previous_data = self.db.has_period_data(previous_start, previous_end)
        
        # Mettre à jour l'état des boutons de navigation
        self.nav_layout.prev_btn.setEnabled(has_previous_data)
        next_period = end_date + timedelta(days=1)
        self.nav_layout.update_next_button_state(
            self.period_controller.get_period_end(next_period) <= self.period_controller.get_current_period_start()
        )
        
        # Mise à jour du solde actuel
        balance = self.db.get_period_balance(self.current_period_start, end_date)
        self.balance_section.update_balance(balance)

        # Mise à jour du solde précédent
        previous_balance = self.db.get_period_balance(previous_start, previous_end)
        self.balance_section.update_previous_balance(
            previous_balance,
            start_date=previous_start,
            end_date=previous_end
        )

        # Mise à jour des tables
        self.update_charges_table()
        self.update_expenses_table()

    def update_charges_table(self):
        self.charges_table.setRowCount(0)
        self.charges_table.setColumnCount(3)
        self.charges_table.setHorizontalHeaderLabels(["Nom", "Montant", "Actions"])
        
        charges = self.db.get_recurring_charges()
        
        for row, charge in enumerate(charges):
            self.charges_table.insertRow(row)
            
            # Ajout des données
            self.charges_table.setItem(row, 0, QTableWidgetItem(charge[1]))  # Nom
            self.charges_table.setItem(row, 1, self.charges_table.format_amount(charge[2]))  # Montant
            
            # Boutons d'action
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            edit_btn = QPushButton("Modifier")
            delete_btn = QPushButton("Supprimer")
            
            edit_btn.clicked.connect(lambda _, c=charge: self.edit_charge(c))
            delete_btn.clicked.connect(lambda _, c=charge: self.delete_charge(c))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            self.charges_table.setCellWidget(row, 2, action_widget)

    def update_expenses_table(self):
        self.expenses_table.setRowCount(0)
        selected_category = self.nav_layout.category_filter.currentData()
        include_exceptional = self.nav_layout.show_exceptional.isChecked()
        
        # Récupérer les dépenses
        expenses = self.db.get_period_expenses(
            self.current_period_start, 
            self.period_controller.get_period_end(self.current_period_start),
            include_exceptional
        )
        
        # Filtrer par catégorie si nécessaire
        if selected_category is not None:
            expenses = [e for e in expenses if e[4] == selected_category]
        
        for row, expense in enumerate(expenses):
            self.expenses_table.insertRow(row)
            
            # Date
            date = datetime.strptime(expense[3], '%Y-%m-%d').strftime('%d/%m/%Y')
            self.expenses_table.setItem(row, 0, QTableWidgetItem(date))
            
            # Description
            self.expenses_table.setItem(row, 1, QTableWidgetItem(expense[1]))
            
            # Montant
            self.expenses_table.setItem(row, 2, self.expenses_table.format_amount(expense[2]))  # Montant
            
            # Catégorie
            self.expenses_table.setItem(row, 3, QTableWidgetItem(expense[5]))  # category_name
            
            # Marquer visuellement les dépenses exceptionnelles
            if expense[6]:  # is_exceptional
                for col in range(self.expenses_table.columnCount()):
                    item = self.expenses_table.item(row, col)
                    if item:
                        item.setBackground(QColor(45, 35, 65))
                        font = item.font()
                        font.setItalic(True)
                        item.setFont(font)
            
            # Boutons d'action
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            edit_btn = QPushButton("Modifier")
            delete_btn = QPushButton("Supprimer")
            
            edit_btn.clicked.connect(lambda _, e=expense: self.edit_expense(e))
            delete_btn.clicked.connect(lambda _, e=expense: self.delete_expense(e))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            self.expenses_table.setCellWidget(row, 4, action_widget)

        # Ajouter une ligne de total pour la catégorie sélectionnée
        if selected_category is not None:
            total = sum(expense[2] for expense in expenses)
            self.expenses_table.add_total_row(total)

    def show_add_charge_dialog(self):
        dialog = RecurringChargeDialog(self)
        if dialog.exec():
            charge_data = dialog.get_charge_data()
            if charge_data:
                self.db.add_recurring_charge(**charge_data)
                self.update_display()
                QMessageBox.information(self, "Succès", "Charge récurrente ajoutée avec succès!")

    def edit_charge(self, charge):
        dialog = RecurringChargeDialog(self, charge)
        if dialog.exec():
            charge_data = dialog.get_charge_data()
            if charge_data:
                self.db.update_recurring_charge(charge[0], **charge_data)
                self.update_display()

    def delete_charge(self, charge):
        if self.confirm_deletion("la charge", charge[1]):
            self.db.delete_recurring_charge(charge[0])
            self.update_display()

    def show_add_income_dialog(self):
        dialog = IncomeDialog(self)
        if dialog.exec():
            income_data = dialog.get_income_data()
            if income_data:
                self.db.add_income(**income_data)
                self.update_display()
                QMessageBox.information(self, "Succès", "Revenu ajouté avec succès!")

    def show_add_expense_dialog(self):
        categories = self.db.get_categories()
        dialog = ExpenseDialog(self, categories=categories)
        if dialog.exec():
            expense_data = dialog.get_expense_data()
            if expense_data:
                self.db.add_expense(**expense_data)
                self.update_display()
                QMessageBox.information(self, "Succès", "Dépense ajoutée avec succès!")

    def edit_expense(self, expense):
        categories = self.db.get_categories()
        dialog = ExpenseDialog(self, categories=categories, expense=expense)
        if dialog.exec():
            expense_data = dialog.get_expense_data()
            if expense_data:
                self.db.update_expense(expense[0], **expense_data)
                self.update_display()

    def delete_expense(self, expense):
        if self.confirm_deletion("la dépense", expense[1]):
            self.db.delete_expense(expense[0])
            self.update_display()

    def show_overview_dialog(self):
        dialog = OverviewDialog(self, self.db)
        dialog.exec()

    def go_to_previous_period(self):
        self.current_period_start = self.period_controller.get_previous_period_start(self.current_period_start)
        self.update_display()

    def go_to_next_period(self):
        """Change la période courante à la période suivante"""
        today = date.today()
        next_period = self.period_controller.get_period_end(self.current_period_start) + timedelta(days=1)
        
        # Ne pas permettre d'aller au-delà de la période actuelle
        if next_period <= self.period_controller.get_current_period_start():
            self.current_period_start = next_period
            self.update_display()
        
        # Mettre à jour l'état du bouton suivant
        self.nav_layout.next_btn.setEnabled(
            self.period_controller.get_period_end(next_period) <= self.period_controller.get_current_period_start()
        )

    def setup_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        
        self.setPalette(palette) 

    def confirm_deletion(self, item_type: str, name: str) -> bool:
        reply = QMessageBox.question(
            self, "Confirmation",
            f"Voulez-vous vraiment supprimer {item_type} '{name}' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes 

    def create_action_buttons(self) -> QHBoxLayout:
        """Crée les boutons d'action"""
        action_layout = QHBoxLayout()
        
        # Boutons de gauche
        left_buttons = QHBoxLayout()
        add_income_btn = QPushButton("Ajouter un revenu")
        add_charge_btn = QPushButton("Ajouter une charge")
        add_expense_btn = QPushButton("Ajouter une dépense")
        
        add_income_btn.clicked.connect(self.show_add_income_dialog)
        add_charge_btn.clicked.connect(self.show_add_charge_dialog)
        add_expense_btn.clicked.connect(self.show_add_expense_dialog)
        
        left_buttons.addWidget(add_income_btn)
        left_buttons.addWidget(add_charge_btn)
        left_buttons.addWidget(add_expense_btn)
        
        # Bouton de droite
        right_buttons = QHBoxLayout()
        overview_btn = QPushButton("Vue d'ensemble")
        overview_btn.clicked.connect(self.show_overview_dialog)
        right_buttons.addWidget(overview_btn)
        
        # Assemblage
        action_layout.addLayout(left_buttons)
        action_layout.addStretch()
        action_layout.addLayout(right_buttons)
        
        return action_layout 