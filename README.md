# 🗺️ Tactical Dashboard Football

> Dashboards d'analyse tactique interactifs — Pass Network, xG, Pressing, Heatmaps  
> à partir des données **StatsBomb Open Data**

**Julie Landrevie — Football Data Analyst**  
*Certifiée Sports Analytics (University of Michigan) · Analyse Vidéo & Data dans le Sport (Université de Lorraine)*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tactical-dashboard-football.streamlit.app)

---

## 📌 Présentation du projet

Ce projet propose des dashboards tactiques interactifs permettant d'analyser :
- Les **réseaux de passes** d'une équipe — qui joue avec qui, les joueurs pivots
- Le **xG (expected goals)** — qualité des occasions créées et concédées
- Le **pressing** — intensité défensive, zones de récupération
- Les **heatmaps** — zones d'activité des joueurs sur le terrain

---

## 🎯 Fonctionnalités

| Dashboard | Description |
|-----------|-------------|
| **Pass Network** | Réseau de passes de l'équipe — nœuds = joueurs, liens = passes |
| **xG Map** | Carte des occasions avec valeur xG — taille = dangerosité |
| **Pressing Map** | Zones de pressing et récupération de balle |
| **Player Heatmap** | Zones d'activité d'un joueur sur le terrain |

**Filtres disponibles :** Compétition → Match → Équipe → Joueur

---

## 🗂️ Structure du projet

```
tactical-dashboard-football/
│
├── src/
│   ├── data_loader.py    # Chargement données StatsBomb
│   ├── metrics.py        # Calcul des métriques tactiques
│   └── viz.py            # Visualisations mplsoccer
│
├── app.py                # Dashboard Streamlit
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Lancement

```bash
git clone https://github.com/Julie-Landrevie/tactical-dashboard-football.git
cd tactical-dashboard-football
pip install -r requirements.txt
streamlit run app.py
```

🌐 **App en ligne :** [tactical-dashboard-football.streamlit.app](https://tactical-dashboard-football.streamlit.app)

---

## ⚠️ Données StatsBomb Open Data

StatsBomb publie gratuitement une **sélection de matchs** par compétition.  
Les classements et analyses reflètent cet échantillon, pas une saison entière.

---

## 📦 Stack technique

| Catégorie | Outils |
|-----------|--------|
| **Données** | statsbombpy — StatsBomb Open Data |
| **Visualisation terrain** | mplsoccer · matplotlib |
| **Graphiques** | Plotly |
| **Dashboard** | Streamlit |

---

## 🚀 Extensions prévues

- [ ] Intégration des données de tracking (SkillCorner)
- [ ] Analyse comparative multi-matchs
- [ ] Export PDF des rapports tactiques
- [ ] Analyse du bloc défensif

---

## 📁 Projets liés

| Projet | Description | Lien |
|--------|-------------|------|
| **xG & Shooting Profile Analysis** | Shot quality analysis — StatsBomb | [→ Repo](https://github.com/Julie-Landrevie/xg-shooting-analysis) · [→ App](https://xg-shooting-analysis.streamlit.app) |
| **MPG Optimizer** | Fantasy football analytics | [→ Repo](https://github.com/Julie-Landrevie/mpg-optimizer) · [→ App](https://mpg-optimizer.streamlit.app) |

---

## 📧 Contact

**Julie Landrevie**  
📩 julie.landrevie@free.fr  
🎓 Sports Analytics — University of Michigan (Coursera)  
🎓 Analyse Vidéo & Data dans le Sport — Université de Lorraine  
🎓 Dartfish Certified Analyst

---

*Données : [StatsBomb Open Data](https://github.com/statsbomb/open-data) — utilisées conformément à la licence open data StatsBomb.*
