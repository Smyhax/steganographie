# Stéganographie

## Description
Une application en ligne de commande (CLI) permettant de **cacher** et **révéler** des messages secrets dans des images PNG grâce à la méthode **LSB** (*Least Significant Bit*).

---

## Fonctionnalités
- **Interface CLI intuitive** : Guide l'utilisateur à travers les différentes options.
- **Validation des entrées** :  
  - Prise en charge des fichiers au format `.png` uniquement.  
  - Conversion automatique des images en mode `RGB`.  
  - Gestion des messages dépassant la capacité maximale de l'image.
- **Feedback clair** : Fournit des messages d'erreur et des notifications explicites pour l'utilisateur.

---

## Installation

### Prérequis
- **Python** >= 3.8  
- **Pillow** (librairie pour l'imagerie)

### Installation de Pillow
Exécutez la commande suivante pour installer Pillow :  
```bash
pip install pillow
```

---

## Utilisation

### Lancer le programme
Pour utiliser l'application, exécutez la commande suivante :  
```bash
python stegano.py
```

---

## Structure du projet

Voici l'organisation des fichiers du projet :  
```plaintext
stegano/
├── input/        # Dossier contenant les images d'entrée
├── output/       # Dossier pour stocker les images modifiées
└── stegano.py    # Code source principal