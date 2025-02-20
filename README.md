# EcoTrack - Gestionnaire de Budget Personnel

**EcoTrack** est une application de bureau développée en **Python** avec **PyQt6** qui permet de suivre facilement vos dépenses, revenus et charges récurrentes sur une base mensuelle.

----------

## 🚀 Fonctionnalités

### 🔄 Gestion des périodes

-   Périodes mensuelles du 25 au 24 du mois suivant
-   Navigation intuitive entre les périodes
-   Vue d'ensemble annuelle des finances

### 💸 Suivi des dépenses

-   Ajout de dépenses avec catégorisation
-   Distinction entre dépenses normales et exceptionnelles
-   Filtrage par catégorie
-   Modification et suppression des dépenses

### 💰 Gestion des revenus

-   Enregistrement des revenus avec date et description
-   Calcul automatique des soldes

### 📅 Charges récurrentes

-   Gestion des charges mensuelles fixes
-   Application automatique sur la période courante
-   Modification et suppression des charges

### 📊 Vue d'ensemble

-   Synthèse annuelle des finances
-   Visualisation des soldes mensuels
-   Suivi des dépenses exceptionnelles

----------

## 🛠️ Installation

1.  **Cloner le dépôt :**  
    `git clone https://github.com/votre-username/ecotrack.git`  
    `cd ecotrack`
    
2.  **Créer un environnement virtuel :**  
    `python -m venv venv`  
    `source venv/bin/activate # Linux/Mac`  
    `venv\Scripts\activate # Windows`
    
3.  **Installer les dépendances :**  
    `pip install -r requirements.txt`
    
4.  **Lancer l'application :**  
    `python src/main.py`
    

----------

## 📂 Structure du projet

ecotrack/  
├── src/  
│ ├── controllers/ # Logique de contrôle  
│ ├── layouts/ # Layouts PyQt  
│ ├── models/ # Modèles de données  
│ ├── utils/ # Utilitaires (BDD, etc.)  
│ ├── views/ # Interfaces utilisateur  
│ ├── widgets/ # Widgets personnalisés  
│ └── main.py # Point d'entrée  
├── data/ # Données de l'application  
└── requirements.txt # Dépendances

## 📖 Guide d'utilisation

### 🔧 Première utilisation

1.  Lancez l'application
2.  Ajoutez vos charges récurrentes mensuelles
3.  Enregistrez vos revenus
4.  Commencez à suivre vos dépenses

### 📝 Gestion quotidienne

-   Ajoutez vos dépenses au fur et à mesure
-   Catégorisez-les correctement
-   Marquez les dépenses exceptionnelles si nécessaire
-   Consultez la vue d'ensemble pour analyser vos finances

### 🌐 Navigation

-   Utilisez les boutons **"Période précédente"** et **"Période suivante"** pour naviguer
-   Filtrez les dépenses par catégorie
-   Affichez/masquez les dépenses exceptionnelles selon vos besoins

----------

## 🔍 Fonctionnalités détaillées

### 📆 Périodes

-   Chaque période va du 25 du mois au 24 du mois suivant
-   Les charges récurrentes sont automatiquement appliquées à la période courante
-   Navigation intuitive entre les périodes avec mise à jour des soldes

### 💵 Dépenses

-   Description détaillée
-   Montant
-   Catégorisation
-   Option pour marquer comme exceptionnelle
-   Filtrage par catégorie
-   Modification et suppression possibles

### 📈 Revenus

-   Enregistrement simple avec description
-   Date automatique
-   Calcul immédiat des nouveaux soldes

### 🧾 Charges récurrentes

-   Nom de la charge
-   Montant mensuel
-   Application automatique sur la période courante
-   Modification et suppression avec mise à jour des soldes

### 📊 Vue d'ensemble

-   Synthèse annuelle
-   Totaux par catégorie
-   Suivi des dépenses exceptionnelles
-   Visualisation des tendances

----------

## 💻 Développement

### ⚙️ Technologies utilisées

-   **Python 3.x**
-   **PyQt6** pour l'interface graphique
-   **SQLite** pour le stockage des données

### 🗄️ Base de données

-   Stockage local dans `data/ecotrack.db`
-   Tables pour les revenus, dépenses, charges et catégories
-   Gestion automatique des sauvegardes

----------

## 📜 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.