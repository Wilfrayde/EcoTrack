import sqlite3
from datetime import datetime, date
from pathlib import Path

class Database:
    def __init__(self):
        # Crée le dossier data s'il n'existe pas
        Path("data").mkdir(exist_ok=True)
        self.conn = sqlite3.connect('data/ecotrack.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Table des revenus existante
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT,
            date DATE NOT NULL
        )
        ''')

        # Table simplifiée pour les charges récurrentes
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS recurring_charges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL
        )
        ''')

        # Table des catégories de dépenses
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS expense_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')

        # Table des dépenses
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE NOT NULL,
            category_id INTEGER,
            is_exceptional BOOLEAN DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES expense_categories (id)
        )
        ''')

        # Insertion des catégories par défaut si la table est vide
        self.cursor.execute('SELECT COUNT(*) FROM expense_categories')
        if self.cursor.fetchone()[0] == 0:
            default_categories = [
                "Alimentation",
                "Transport",
                "Loisirs",
                "Shopping",
                "Santé",
                "Restaurant",
                "Autres"
            ]
            self.cursor.executemany(
                'INSERT INTO expense_categories (name) VALUES (?)',
                [(cat,) for cat in default_categories]
            )
        
        self.conn.commit()

    def add_income(self, amount: float, description: str, date: datetime) -> int:
        self.cursor.execute('''
        INSERT INTO incomes (amount, description, date)
        VALUES (?, ?, ?)
        ''', (amount, description, date.strftime('%Y-%m-%d')))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_incomes(self):
        self.cursor.execute('SELECT * FROM incomes ORDER BY date DESC')
        return self.cursor.fetchall()

    def get_total_income(self):
        self.cursor.execute('SELECT SUM(amount) FROM incomes')
        return self.cursor.fetchone()[0] or 0.0

    def add_recurring_charge(self, name: str, amount: float) -> int:
        self.cursor.execute('''
        INSERT INTO recurring_charges (name, amount)
        VALUES (?, ?)
        ''', (name, amount))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_recurring_charges(self):
        self.cursor.execute('SELECT * FROM recurring_charges ORDER BY name')
        return self.cursor.fetchall()

    def update_recurring_charge(self, id: int, name: str, amount: float):
        self.cursor.execute('''
        UPDATE recurring_charges 
        SET name = ?, amount = ?
        WHERE id = ?
        ''', (name, amount, id))
        self.conn.commit()

    def delete_recurring_charge(self, id: int):
        self.cursor.execute('DELETE FROM recurring_charges WHERE id = ?', (id,))
        self.conn.commit()

    def add_expense(self, description: str, amount: float, date: datetime, category_id: int, is_exceptional: bool = False) -> int:
        self.cursor.execute('''
        INSERT INTO expenses (description, amount, date, category_id, is_exceptional)
        VALUES (?, ?, ?, ?, ?)
        ''', (description, amount, date.strftime('%Y-%m-%d'), category_id, is_exceptional))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_categories(self):
        self.cursor.execute('SELECT * FROM expense_categories ORDER BY name')
        return self.cursor.fetchall()

    def get_period_expenses(self, start_date: date, end_date: date, include_exceptional: bool = True):
        query = '''
        SELECT e.id, e.description, e.amount, e.date, e.category_id, c.name as category_name, e.is_exceptional
        FROM expenses e 
        LEFT JOIN expense_categories c ON e.category_id = c.id
        WHERE e.date BETWEEN ? AND ?
        '''
        if not include_exceptional:
            query += ' AND e.is_exceptional = 0'
        query += ' ORDER BY e.date DESC'
        
        self.cursor.execute(query, (start_date.isoformat(), end_date.isoformat()))
        return self.cursor.fetchall()

    def update_expense(self, id: int, description: str, amount: float, date: datetime, category_id: int, is_exceptional: bool):
        self.cursor.execute('''
        UPDATE expenses 
        SET description = ?, amount = ?, date = ?, category_id = ?, is_exceptional = ?
        WHERE id = ?
        ''', (description, amount, date.strftime('%Y-%m-%d'), category_id, is_exceptional, id))
        self.conn.commit()

    def delete_expense(self, id: int):
        self.cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
        self.conn.commit()

    def get_period_balance(self, start_date: date, end_date: date) -> float:
        """Calcule le solde pour une période"""
        # Calcul des revenus
        self.cursor.execute('''
        SELECT SUM(amount) FROM incomes 
        WHERE date BETWEEN ? AND ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        total_income = self.cursor.fetchone()[0] or 0.0

        # Calcul des charges récurrentes
        total_charges = 0.0
        current_period = self.get_current_period_start()
        
        # On applique les charges uniquement pour la période courante
        if start_date == current_period:
            self.cursor.execute('SELECT SUM(amount) FROM recurring_charges')
            total_charges = self.cursor.fetchone()[0] or 0.0

        # Calcul des dépenses de la période (non exceptionnelles)
        self.cursor.execute('''
        SELECT SUM(amount) FROM expenses
        WHERE date BETWEEN ? AND ? AND is_exceptional = 0
        ''', (start_date.isoformat(), end_date.isoformat()))
        total_expenses = self.cursor.fetchone()[0] or 0.0

        return total_income - total_charges - total_expenses

    def get_current_period_start(self) -> date:
        """Retourne le début de la période courante"""
        today = date.today()
        if today.day >= 25:
            return date(today.year, today.month, 25)
        if today.month == 1:
            return date(today.year - 1, 12, 25)
        return date(today.year, today.month - 1, 25)

    def get_period_end(self, start_date: date) -> date:
        """Retourne la fin d'une période"""
        if start_date.month == 12:
            return date(start_date.year + 1, 1, 24)
        return date(start_date.year, start_date.month + 1, 24)

    def get_annual_income(self, start_date: date, end_date: date) -> float:
        """Calcule le total des revenus pour une année"""
        self.cursor.execute('''
        SELECT SUM(amount) FROM incomes 
        WHERE date BETWEEN ? AND ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        return self.cursor.fetchone()[0] or 0.0

    def get_annual_expenses(self, start_date: date, end_date: date) -> float:
        """Calcule le total des dépenses pour une année"""
        # Calcul des dépenses ponctuelles (non exceptionnelles)
        self.cursor.execute('''
        SELECT SUM(amount) FROM expenses
        WHERE date BETWEEN ? AND ? AND is_exceptional = 0
        ''', (start_date.isoformat(), end_date.isoformat()))
        expenses = self.cursor.fetchone()[0] or 0.0
        
        # Calcul des charges récurrentes
        total_charges = 0.0
        current_period = self.get_current_period_start()
        
        if start_date.year == date.today().year:
            # Pour la période courante, on applique les charges une seule fois
            if start_date <= current_period <= end_date:
                self.cursor.execute('SELECT SUM(amount) FROM recurring_charges')
                charges = self.cursor.fetchone()[0] or 0.0
                total_charges = charges
        
        return expenses + total_charges

    def get_exceptional_expenses(self, start_date: date, end_date: date):
        self.cursor.execute('''
        SELECT e.id, e.description, e.amount, e.date, e.category_id, c.name as category_name, e.is_exceptional
        FROM expenses e 
        LEFT JOIN expense_categories c ON e.category_id = c.id
        WHERE e.date BETWEEN ? AND ? AND e.is_exceptional = 1
        ORDER BY e.date DESC
        ''', (start_date.isoformat(), end_date.isoformat()))
        return self.cursor.fetchall()

    def has_period_data(self, start_date: date, end_date: date) -> bool:
        """Vérifie s'il existe des données (revenus ou dépenses) pour une période donnée"""
        # Vérifier les revenus
        self.cursor.execute('''
        SELECT EXISTS(
            SELECT 1 FROM incomes 
            WHERE date BETWEEN ? AND ?
            LIMIT 1
        )
        ''', (start_date.isoformat(), end_date.isoformat()))
        has_incomes = bool(self.cursor.fetchone()[0])

        # Vérifier les dépenses
        self.cursor.execute('''
        SELECT EXISTS(
            SELECT 1 FROM expenses 
            WHERE date BETWEEN ? AND ?
            LIMIT 1
        )
        ''', (start_date.isoformat(), end_date.isoformat()))
        has_expenses = bool(self.cursor.fetchone()[0])

        return has_incomes or has_expenses

    def format_amount(self, amount: float) -> str:
        """Formate un montant en chaîne de caractères"""
        return f"{amount:+.2f} €"

    def parse_amount(self, amount_str: str) -> float:
        """Convertit une chaîne de caractères en montant"""
        amount_str = amount_str.replace('€', '').strip()
        amount_str = amount_str.replace(',', '.')
        return float(amount_str)

    def __del__(self):
        self.conn.close() 