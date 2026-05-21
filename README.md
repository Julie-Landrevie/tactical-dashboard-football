# ⚽ Tactical Dashboard — Football Analysis

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square&logo=streamlit)
![StatsBomb](https://img.shields.io/badge/Data-StatsBomb_Open_Data-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)

> Interactive tactical football analysis dashboard built with StatsBomb open data.  
> Part of Julie Landrevie's football data analysis portfolio.

🔗 **[Live App → julie-landrevie-tactical-dashboard-football.streamlit.app](https://julie-landrevie-tactical-dashboard-football.streamlit.app)**

---

## 📊 Features

### 🕸️ Pass Network
Visualisation du réseau de passes des 11 titulaires. Les nœuds représentent les positions moyennes des joueurs, l'épaisseur des connexions la fréquence des combinaisons.

### 🎯 xG & Shot Analysis
Carte des tirs avec Expected Goals (xG) — taille des bulles proportionnelle à la dangerosité. Timeline xG cumulé des deux équipes sur l'ensemble du match.

### 🛡️ Pressing & Defensive Block
Heatmap KDE des zones de pressing et positionnement des récupérations de balle. Approximation du PPDA et distribution temporelle en miroir.

### 🔥 Heatmaps & Activity Zones
Densité d'activité par équipe ou par joueur individuel. Filtrage par type d'événement (passes, portés, pressions, tirs...). Répartition par tiers du terrain.

---

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/Julie-Landrevie/tactical-dashboard-football.git
cd tactical-dashboard-football
pip install -r requirements.txt
```

### Launch

```bash
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`. Aucune clé API nécessaire — les données StatsBomb se chargent automatiquement.

---

## 🗂️ Project Structure

```
tactical-dashboard-football/
├── app.py              # Main Streamlit application
├── name_resolver.py    # Player name → shirt name mapping (+250 players)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 📦 Data

Données issues de [StatsBomb Open Data](https://github.com/statsbomb/open-data) — accès libre, aucune authentification requise.

**33 compétitions disponibles :**

| Catégorie | Compétitions |
|---|---|
| Coupes du Monde | 2022, 2018, 1990, 1986 |
| Euros & Copa | UEFA Euro 2024 & 2020, Copa America 2024 |
| CAN | African Cup of Nations 2023 |
| Champions League | 11 saisons (2008/09 → 2018/19) |
| La Liga | 6 saisons (2015/16 → 2020/21) |
| Ligue 1 | 3 saisons (2015/16, 2021/22, 2022/23) |
| Autres | Premier League, Bundesliga, Serie A, MLS |

---

## 🛠️ Stack

| Outil | Usage |
|---|---|
| `streamlit` | Interface web interactive |
| `mplsoccer` | Visualisations terrain (pitch) |
| `statsbombpy` | Accès aux données StatsBomb |
| `plotly` | Graphiques interactifs |
| `pandas` / `numpy` | Traitement des données |
| `matplotlib` | Rendus statiques |

---

## 🗺️ Roadmap

- [ ] Pizza chart joueur (radar mplsoccer)
- [ ] Analyse des coups de pied arrêtés
- [ ] Comparaison multi-matchs sur la saison
- [ ] Export PDF des analyses

---

## 🔧 Changelog

### v1.2.0
- 33 compétitions disponibles (toutes les données StatsBomb open data)
- Déploiement Streamlit Cloud

### v1.1.0
- Résolution intelligente des noms de maillot (`name_resolver.py`) — dictionnaire de +250 joueurs + fallback algorithmique
- Correction des noms tronqués (suppression limite 12 caractères)
- Sélection match par équipe ou toutes compétitions confondues
- Timeline xG étendue jusqu'à la fin du match (90min+)
- Correction couleurs tirs : Bloqué (bleu) et Poteau/Barre (violet)
- Correction artefacts lors du changement de match

### v1.0.0
- Pass Network, xG & Shots, Pressing, Heatmaps
- StatsBomb open data intégré

---

## 👤 Author

**Julie Landrevie** — Football Data & Video Analyst  
Certifiée Sports Analytics (University of Michigan) · Analyse Vidéo et Data (Université de Lorraine)

📧 julie.landrevie@free.fr

---

## 📁 Portfolio

| Projet | Description | Status |
|---|---|---|
| [MPG Optimizer](https://github.com/Julie-Landrevie/mpg-optimizer) | Fantasy football analytics | ✅ Live |
| [World Cup 2026 Predictor](https://github.com/Julie-Landrevie/world-cup-predictor) | Prédictions Poisson | 🔨 In progress |
| **Tactical Dashboard** | Ce projet | ✅ [Live](https://julie-landrevie-tactical-dashboard-football.streamlit.app) |
| xG & Shooting Profile | StatsBomb shot analysis | 🔜 Coming soon |
| Physical & Tracking | SkillCorner player load | 🔜 Coming soon |
| Pass Network Analysis | Team structure deep dive | 🔜 Coming soon |

---

*Data provided by [StatsBomb](https://statsbomb.com/what-we-do/hub/free-data/) under their open data licence.*
