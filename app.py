import streamlit as st
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Tactical Dashboard — Julie Landrevie",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d0f14;
    color: #e8eaf0;
}

.stApp {
    background-color: #0d0f14;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #f0f2f8;
    margin-bottom: 0px;
    line-height: 1;
}

.sub-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #4ade80;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

.metric-card {
    background: #161a24;
    border: 1px solid #252a38;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #4ade80;
    line-height: 1;
}

.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 2px;
}

.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #a5b4fc;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border-left: 3px solid #4ade80;
    padding-left: 0.7rem;
    margin: 1.5rem 0 1rem 0;
}

.stSelectbox > div > div {
    background-color: #161a24 !important;
    border: 1px solid #252a38 !important;
    color: #e8eaf0 !important;
    font-family: 'Inter', sans-serif !important;
}

.stButton > button {
    background: #4ade80 !important;
    color: #0d0f14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    letter-spacing: 0.05em !important;
}

.stButton > button:hover {
    background: #22c55e !important;
    transform: translateY(-1px);
}

[data-testid="stSidebar"] {
    background-color: #0a0c11 !important;
    border-right: 1px solid #1c2030 !important;
}

.tab-description {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: #6b7280;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.3rem;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    color: #6b7280 !important;
    background: #161a24 !important;
    border-radius: 6px !important;
    border: 1px solid #252a38 !important;
    padding: 0.4rem 0.9rem !important;
}

.stTabs [aria-selected="true"] {
    color: #4ade80 !important;
    border-color: #4ade80 !important;
}

.stSpinner > div {
    border-top-color: #4ade80 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 8])
with col_title:
    st.markdown('<div class="main-title">⚽ TACTICAL DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">StatsBomb Open Data · Julie Landrevie · Football Analysis</div>', unsafe_allow_html=True)

st.markdown("---")

# ─── IMPORTS ─────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mplsoccer import Pitch, VerticalPitch, PyPizza
from statsbombpy import sb
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from name_resolver import build_name_map

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
COMPETITIONS = {
    # ── Compétitions internationales ──────────────────────────────
    "🌍 FIFA World Cup 2022":           (43, 106),
    "🌍 FIFA World Cup 2018":           (43, 3),
    "🌍 FIFA World Cup 1990":           (43, 55),
    "🌍 FIFA World Cup 1986":           (43, 54),
    "🏆 UEFA Euro 2024":                (55, 282),
    "🏆 UEFA Euro 2020":                (55, 43),
    "🏆 Copa America 2024":             (223, 282),
    "🏆 African Cup of Nations 2023":   (1267, 107),
    # ── Champions League ──────────────────────────────────────────
    "⭐ Champions League 2018/2019":    (16, 4),
    "⭐ Champions League 2017/2018":    (16, 1),
    "⭐ Champions League 2016/2017":    (16, 2),
    "⭐ Champions League 2015/2016":    (16, 27),
    "⭐ Champions League 2014/2015":    (16, 26),
    "⭐ Champions League 2013/2014":    (16, 25),
    "⭐ Champions League 2012/2013":    (16, 24),
    "⭐ Champions League 2011/2012":    (16, 23),
    "⭐ Champions League 2010/2011":    (16, 22),
    "⭐ Champions League 2009/2010":    (16, 21),
    "⭐ Champions League 2008/2009":    (16, 41),
    # ── Ligues nationales ─────────────────────────────────────────
    "🇪🇸 La Liga 2020/2021":            (11, 90),
    "🇪🇸 La Liga 2019/2020":            (11, 42),
    "🇪🇸 La Liga 2018/2019":            (11, 4),
    "🇪🇸 La Liga 2017/2018":            (11, 1),
    "🇪🇸 La Liga 2016/2017":            (11, 2),
    "🇪🇸 La Liga 2015/2016":            (11, 27),
    "🇫🇷 Ligue 1 2022/2023":            (7, 235),
    "🇫🇷 Ligue 1 2021/2022":            (7, 108),
    "🇫🇷 Ligue 1 2015/2016":            (7, 27),
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League 2015/2016":    (2, 27),
    "🇩🇪 Bundesliga 2023/2024":         (9, 281),
    "🇩🇪 Bundesliga 2015/2016":         (9, 27),
    "🇮🇹 Serie A 2015/2016":            (12, 27),
    "🇺🇸 MLS 2023":                     (44, 107),
}

with st.sidebar:
    st.markdown('<div class="section-header">⚙️ Paramètres</div>', unsafe_allow_html=True)
    comp_choice = st.selectbox("Compétition", list(COMPETITIONS.keys()))
    comp_id, season_id = COMPETITIONS[comp_choice]

    @st.cache_data(show_spinner=False)
    def load_matches(cid, sid):
        return sb.matches(competition_id=cid, season_id=sid)

    with st.spinner("Chargement des matchs..."):
        matches_df = load_matches(comp_id, season_id)

    teams = sorted(set(matches_df["home_team"].tolist() + matches_df["away_team"].tolist()))

    filter_mode = st.radio("Filtrer par", ["Une équipe", "Toutes les équipes"], horizontal=True)
    if filter_mode == "Une équipe":
        team = st.selectbox("Équipe", teams)
        filtered_matches = matches_df[
            (matches_df["home_team"] == team) | (matches_df["away_team"] == team)
        ].copy()
    else:
        filtered_matches = matches_df.copy()

    filtered_matches = filtered_matches.sort_values(["home_team","away_team"])
    filtered_matches["label"] = filtered_matches.apply(
        lambda r: f"{r['home_team']} {r['home_score']}-{r['away_score']} {r['away_team']}", axis=1
    )
    match_label = st.selectbox("Match", filtered_matches["label"].tolist())
    match_row = filtered_matches[filtered_matches["label"] == match_label].iloc[0]
    match_id = int(match_row["match_id"])

    @st.cache_data(show_spinner=False)
    def load_events(mid):
        return sb.events(match_id=mid)

    with st.spinner("Chargement des événements..."):
        events = load_events(match_id)

    @st.cache_data(show_spinner=False)
    def get_name_map(mid):
        ev = load_events(mid)
        return build_name_map(ev)

    name_map = get_name_map(match_id)

    home_team = match_row["home_team"]
    away_team = match_row["away_team"]
    home_score = match_row["home_score"]
    away_score = match_row["away_score"]

    st.markdown("---")
    st.markdown(f'<div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:#4ade80;text-align:center;">{home_team} {home_score} — {away_score} {away_team}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-family:\'Inter\',sans-serif;font-size:0.65rem;color:#6b7280;text-align:center;margin-top:4px;">{int(len(events))} événements chargés</div>', unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🕸️ Pass Network",
    "🎯 xG & Shots",
    "🛡️ Pressing",
    "🔥 Heatmaps"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — PASS NETWORK
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">Réseau de passes & Structure d\'équipe</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-description">Visualisation des connexions entre joueurs via les passes complétées. La taille des nœuds représente le volume de passes, l\'épaisseur des arêtes la fréquence des combinaisons.</div>', unsafe_allow_html=True)

    col_team1, col_team2 = st.columns(2)

    def build_pass_network(events, team_name, fig_title):
        passes = events[
            (events["type"] == "Pass") &
            (events["team"] == team_name) &
            (events["pass_outcome"].isna()) &
            (events["period"].isin([1, 2]))
        ].copy()

        # Get starting XI from tactics
        tactics = events[events["type"] == "Starting XI"]
        team_tactics = tactics[tactics["team"] == team_name]
        if not team_tactics.empty:
            lineup = team_tactics.iloc[0]["tactics"]
            if isinstance(lineup, dict):
                xi_players = [p["player"]["name"] for p in lineup.get("lineup", [])]
            else:
                xi_players = passes["player"].unique().tolist()[:11]
        else:
            xi_players = passes["player"].unique().tolist()[:11]

        passes = passes[passes["player"].isin(xi_players) & passes["pass_recipient"].isin(xi_players)]

        if passes.empty:
            return None

        # Average positions
        passes["x"] = passes["location"].apply(lambda l: l[0] if isinstance(l, list) else np.nan)
        passes["y"] = passes["location"].apply(lambda l: l[1] if isinstance(l, list) else np.nan)
        avg_pos = passes.groupby("player")[["x","y"]].mean()

        # Pass counts per player
        pass_count = passes.groupby("player").size().rename("n_passes")
        avg_pos = avg_pos.join(pass_count)

        # Pair connections
        pairs = passes.groupby(["player","pass_recipient"]).size().reset_index(name="count")
        pairs = pairs[pairs["count"] >= 3]

        # Draw
        fig, ax = plt.subplots(figsize=(8, 5.5))
        fig.patch.set_facecolor("#0d0f14")
        ax.set_facecolor("#0d0f14")

        pitch = Pitch(pitch_type="statsbomb", pitch_color="#0d0f14",
                      line_color="#252a38", linewidth=1)
        pitch.draw(ax=ax)

        # Edges
        max_count = pairs["count"].max() if not pairs.empty else 1
        for _, row in pairs.iterrows():
            if row["player"] in avg_pos.index and row["pass_recipient"] in avg_pos.index:
                x_start = avg_pos.loc[row["player"], "x"]
                y_start = avg_pos.loc[row["player"], "y"]
                x_end = avg_pos.loc[row["pass_recipient"], "x"]
                y_end = avg_pos.loc[row["pass_recipient"], "y"]
                alpha = 0.2 + 0.6 * (row["count"] / max_count)
                lw = 0.5 + 3.5 * (row["count"] / max_count)
                ax.plot([x_start, x_end], [y_start, y_end],
                        color="#4ade80", alpha=alpha, linewidth=lw, zorder=1)

        # Nodes
        max_passes = avg_pos["n_passes"].max() if "n_passes" in avg_pos else 1
        for player, row in avg_pos.iterrows():
            if pd.notna(row["x"]) and pd.notna(row["y"]):
                size = 200 + 600 * (row.get("n_passes", 1) / max_passes)
                ax.scatter(row["x"], row["y"], s=size, color="#4ade80",
                           edgecolors="#0d0f14", linewidths=1.5, zorder=3)
                short_name = name_map.get(player, player.split()[-1])
                ax.text(row["x"], row["y"] - 4.5, short_name,
                        fontsize=6.5, color="#e8eaf0", ha="center", va="top",
                        fontfamily="monospace", fontweight="bold", zorder=4)

        ax.set_title(fig_title, color="#e8eaf0", fontsize=11,
                     fontfamily="sans-serif", fontweight="bold", pad=10)
        plt.tight_layout()
        return fig

    with col_team1:
        fig1 = build_pass_network(events, home_team, f"[DOM] {home_team}")
        if fig1:
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)
        else:
            st.info("Données insuffisantes pour ce match.")

    with col_team2:
        fig2 = build_pass_network(events, away_team, f"[EXT] {away_team}")
        if fig2:
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)
        else:
            st.info("Données insuffisantes pour ce match.")

    # Pass stats
    st.markdown('<div class="section-header">Statistiques de passes</div>', unsafe_allow_html=True)
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    for team_name, cols in [(home_team, [col_s1, col_s2]), (away_team, [col_s3, col_s4])]:
        t_passes = events[(events["type"] == "Pass") & (events["team"] == team_name)]
        total = len(t_passes)
        completed = t_passes["pass_outcome"].isna().sum()
        pct = round(100 * completed / total, 1) if total > 0 else 0
        avg_len = round(t_passes["pass_length"].mean(), 1) if "pass_length" in t_passes.columns else 0

        with cols[0]:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{completed}</div><div class="metric-label">{team_name[:12]} — Passes réussies</div></div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{pct}%</div><div class="metric-label">Précision · {avg_len}m moy.</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — xG & SHOTS
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Analyse xG & Profil de tir</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-description">Carte des tirs avec Expected Goals (xG). La taille des bulles représente la valeur xG du tir. Vert = but, orange = arrêté, rouge = non cadré, bleu = bloqué, violet = poteau/barre.</div>', unsafe_allow_html=True)

    # Clé unique par match pour éviter les artefacts
    _match_key = str(match_id)
    shots = events[events["type"] == "Shot"].copy()
    shots["x"] = shots["location"].apply(lambda l: l[0] if isinstance(l, list) else np.nan)
    shots["y"] = shots["location"].apply(lambda l: l[1] if isinstance(l, list) else np.nan)
    shots["xg"] = pd.to_numeric(shots["shot_statsbomb_xg"], errors="coerce").fillna(0.05)

    def shot_color(outcome):
        if outcome == "Goal":     return "#4ade80"   # vert
        if outcome == "Saved":    return "#f59e0b"   # orange
        if outcome == "Off T":    return "#ef4444"   # rouge
        if outcome == "Blocked":  return "#60a5fa"   # bleu
        if outcome == "Post":     return "#c084fc"   # violet
        if outcome == "Wayward":  return "#ef4444"   # rouge (très loin du cadre)
        return "#6b7280"                              # gris (autre)

    shots["color"] = shots["shot_outcome"].apply(shot_color)

    fig_shot, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig_shot.patch.set_facecolor("#0d0f14")

    for idx, team_name in enumerate([home_team, away_team]):
        ax = axes[idx]
        ax.set_facecolor("#0d0f14")
        pitch = VerticalPitch(pitch_type="statsbomb", pitch_color="#0d0f14",
                              line_color="#252a38", linewidth=1, half=True)
        pitch.draw(ax=ax)

        team_shots = shots[shots["team"] == team_name]
        for _, s in team_shots.iterrows():
            if pd.notna(s["x"]) and pd.notna(s["y"]):
                size = max(50, s["xg"] * 1200)
                pitch.scatter(s["x"], s["y"], s=size, color=s["color"],
                              edgecolors="#0d0f14", linewidths=1, alpha=0.85,
                              ax=ax, zorder=3)

        xg_total = team_shots["xg"].sum()
        goals = (team_shots["shot_outcome"] == "Goal").sum()
        ax.set_title(f"{team_name}\n{goals} buts · xG {xg_total:.2f}",
                     color="#e8eaf0", fontsize=10, fontfamily="sans-serif",
                     fontweight="bold", pad=8)

    legend_items = [
        mpatches.Patch(color="#4ade80", label="But"),
        mpatches.Patch(color="#f59e0b", label="Arrêté"),
        mpatches.Patch(color="#ef4444", label="Non cadré"),
        mpatches.Patch(color="#60a5fa", label="Bloqué"),
        mpatches.Patch(color="#c084fc", label="Poteau/Barre"),
    ]
    fig_shot.legend(handles=legend_items, loc="lower center", ncol=5,
                    facecolor="#161a24", edgecolor="#252a38",
                    labelcolor="#e8eaf0", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig_shot, use_container_width=True)
    plt.close(fig_shot)

    # xG timeline
    st.markdown('<div class="section-header">Timeline xG cumulé</div>', unsafe_allow_html=True)
    shots_sorted = shots.sort_values("minute").copy()

    fig_xg = go.Figure()
    fill_colors = {"#4ade80": "rgba(74,222,128,0.08)", "#a5b4fc": "rgba(165,180,252,0.08)"}
    # Fin du match = dernière minute enregistrée, minimum 90
    match_end = max(int(events["minute"].max()), 90)
    for team_name, color in [(home_team, "#4ade80"), (away_team, "#a5b4fc")]:
        t = shots_sorted[shots_sorted["team"] == team_name].copy()
        t["cum_xg"] = t["xg"].cumsum()
        # Point de départ à 0, point final à match_end pour que les deux courbes aillent jusqu'au bout
        final_xg = t["cum_xg"].iloc[-1] if len(t) > 0 else 0
        t = pd.concat([
            pd.DataFrame({"minute": [0], "cum_xg": [0]}),
            t[["minute","cum_xg"]],
            pd.DataFrame({"minute": [match_end], "cum_xg": [final_xg]})
        ])

        fig_xg.add_trace(go.Scatter(
            x=t["minute"], y=t["cum_xg"],
            mode="lines", name=team_name,
            line=dict(color=color, width=2.5),
            fill="tozeroy", fillcolor=fill_colors[color]
        ))

    fig_xg.update_layout(
        plot_bgcolor="#0d0f14", paper_bgcolor="#0d0f14",
        font=dict(color="#e8eaf0", family="Inter"),
        xaxis=dict(title="Minute", gridcolor="#1c2030", color="#6b7280"),
        yaxis=dict(title="xG cumulé", gridcolor="#1c2030", color="#6b7280"),
        legend=dict(bgcolor="#161a24", bordercolor="#252a38"),
        height=280, margin=dict(t=20, b=40, l=50, r=20)
    )
    st.plotly_chart(fig_xg, use_container_width=True)

    # Shot stats
    st.markdown('<div class="section-header">Statistiques détaillées</div>', unsafe_allow_html=True)
    cols_xg = st.columns(6)
    metrics = []
    for team_name in [home_team, away_team]:
        t = shots[shots["team"] == team_name]
        metrics += [
            (f"Tirs ({team_name[:10]})", len(t)),
            (f"Cadrés", t["shot_outcome"].isin(["Goal","Saved"]).sum()),
            (f"xG total", f"{t['xg'].sum():.2f}"),
        ]
    for i, (label, val) in enumerate(metrics):
        with cols_xg[i]:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — PRESSING
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Intensité de pressing & Bloc défensif</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-description">Zones de pressing (actions de pression) et récupérations de balle. La densité révèle le bloc défensif et l\'intensité du contre-pressing.</div>', unsafe_allow_html=True)

    pressures = events[events["type"] == "Pressure"].copy()
    recoveries = events[events["type"] == "Ball Recovery"].copy()

    pressures["x"] = pressures["location"].apply(lambda l: l[0] if isinstance(l, list) else np.nan)
    pressures["y"] = pressures["location"].apply(lambda l: l[1] if isinstance(l, list) else np.nan)
    recoveries["x"] = recoveries["location"].apply(lambda l: l[0] if isinstance(l, list) else np.nan)
    recoveries["y"] = recoveries["location"].apply(lambda l: l[1] if isinstance(l, list) else np.nan)

    fig_press, axes2 = plt.subplots(1, 2, figsize=(14, 5.5))
    fig_press.patch.set_facecolor("#0d0f14")

    for idx, team_name in enumerate([home_team, away_team]):
        ax = axes2[idx]
        ax.set_facecolor("#0d0f14")

        pitch = Pitch(pitch_type="statsbomb", pitch_color="#0d0f14",
                      line_color="#252a38", linewidth=1)
        pitch.draw(ax=ax)

        t_press = pressures[pressures["team"] == team_name].dropna(subset=["x","y"])
        t_recov = recoveries[recoveries["team"] == team_name].dropna(subset=["x","y"])

        if len(t_press) > 3:
            pitch.kdeplot(t_press["x"], t_press["y"],
                         ax=ax, cmap="Greens", fill=True,
                         levels=12, alpha=0.6, bw_adjust=0.8)

        if len(t_recov) > 0:
            pitch.scatter(t_recov["x"], t_recov["y"],
                         s=60, color="#f59e0b", edgecolors="#0d0f14",
                         linewidths=0.8, alpha=0.7, ax=ax, zorder=4,
                         marker="D")

        n_press = len(t_press)
        n_recov = len(t_recov)
        ppda_approx = round(n_press / max(n_recov, 1), 1)

        ax.set_title(f"{team_name}\n{n_press} pressions · {n_recov} récup. · PPDA≈{ppda_approx}",
                     color="#e8eaf0", fontsize=9.5, fontfamily="sans-serif",
                     fontweight="bold", pad=8)

    legend2 = [
        mpatches.Patch(color="#4ade80", alpha=0.6, label="Zone de pressing (densité)"),
        mpatches.Patch(color="#f59e0b", label="Récupération de balle"),
    ]
    fig_press.legend(handles=legend2, loc="lower center", ncol=2,
                     facecolor="#161a24", edgecolor="#252a38",
                     labelcolor="#e8eaf0", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig_press, use_container_width=True)
    plt.close(fig_press)

    # Pressing timeline by period
    st.markdown('<div class="section-header">Pressing par tranche de jeu</div>', unsafe_allow_html=True)

    press_home = pressures[pressures["team"] == home_team]
    press_away = pressures[pressures["team"] == away_team]

    bins = list(range(0, 100, 10))
    labels = [f"{b}-{b+10}'" for b in bins[:-1]]

    h_counts, _ = np.histogram(press_home["minute"].dropna(), bins=bins)
    a_counts, _ = np.histogram(press_away["minute"].dropna(), bins=bins)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=labels, y=h_counts, name=home_team, marker_color="#4ade80"))
    fig_bar.add_trace(go.Bar(x=labels, y=-a_counts, name=away_team, marker_color="#a5b4fc"))

    fig_bar.update_layout(
        barmode="relative",
        plot_bgcolor="#0d0f14", paper_bgcolor="#0d0f14",
        font=dict(color="#e8eaf0", family="Inter"),
        xaxis=dict(title="Tranche de temps", gridcolor="#1c2030", color="#6b7280"),
        yaxis=dict(title="Pressions", gridcolor="#1c2030", color="#6b7280"),
        legend=dict(bgcolor="#161a24", bordercolor="#252a38"),
        height=270, margin=dict(t=10, b=40, l=50, r=20),
        title=dict(text="Distribution des pressions (miroir)", font=dict(color="#6b7280", size=11))
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — HEATMAPS
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">Heatmaps & Zones d\'activité</div>', unsafe_allow_html=True)
    st.markdown('<div class="tab-description">Densité d\'activité par joueur ou par équipe. Identifie les zones d\'influence, les couloirs préférentiels et les espaces exploités.</div>', unsafe_allow_html=True)

    col_hm1, col_hm2 = st.columns([1, 2])

    with col_hm1:
        hm_team = st.selectbox("Équipe", [home_team, away_team], key="hm_team")
        hm_mode = st.radio("Mode", ["Équipe complète", "Joueur spécifique"], key="hm_mode")

        team_events = events[events["team"] == hm_team].copy()
        if hm_mode == "Joueur spécifique":
            players = sorted(team_events["player"].dropna().unique().tolist())
            selected_player = st.selectbox("Joueur", players, key="hm_player")

        event_types = st.multiselect(
            "Types d'événements",
            ["Pass", "Carry", "Pressure", "Shot", "Dribble", "Ball Recovery"],
            default=["Pass", "Carry"],
            key="hm_events"
        )

    with col_hm2:
        if event_types:
            filtered = team_events[team_events["type"].isin(event_types)]
            if hm_mode == "Joueur spécifique" and selected_player:
                filtered = filtered[filtered["player"] == selected_player]

            filtered = filtered.copy()
            filtered["x"] = filtered["location"].apply(lambda l: l[0] if isinstance(l, list) else np.nan)
            filtered["y"] = filtered["location"].apply(lambda l: l[1] if isinstance(l, list) else np.nan)
            filtered = filtered.dropna(subset=["x","y"])

            fig_hm, ax_hm = plt.subplots(figsize=(9, 6))
            fig_hm.patch.set_facecolor("#0d0f14")
            ax_hm.set_facecolor("#0d0f14")

            pitch_hm = Pitch(pitch_type="statsbomb", pitch_color="#0d0f14",
                             line_color="#333a4d", linewidth=1)
            pitch_hm.draw(ax=ax_hm)

            if len(filtered) > 5:
                pitch_hm.kdeplot(filtered["x"], filtered["y"],
                                ax=ax_hm, cmap="RdYlGn", fill=True,
                                levels=20, alpha=0.75, bw_adjust=0.65)
            else:
                pitch_hm.scatter(filtered["x"], filtered["y"],
                                s=80, color="#4ade80", alpha=0.6, ax=ax_hm)

            title_str = selected_player if hm_mode == "Joueur spécifique" else hm_team
            ax_hm.set_title(f"{title_str} · {', '.join(event_types)}\n{len(filtered)} actions",
                           color="#e8eaf0", fontsize=10, fontfamily="sans-serif",
                           fontweight="bold", pad=10)

            plt.tight_layout()
            st.pyplot(fig_hm, use_container_width=True)
            plt.close(fig_hm)
        else:
            st.info("Sélectionne au moins un type d'événement.")

    # Zone breakdown
    st.markdown('<div class="section-header">Répartition par tiers du terrain</div>', unsafe_allow_html=True)

    def zone_breakdown(team_name):
        t_ev = events[(events["team"] == team_name) & (events["type"].isin(["Pass","Carry","Pressure"]))].copy()
        t_ev["x"] = t_ev["location"].apply(lambda l: l[0] if isinstance(l, list) else np.nan)
        t_ev = t_ev.dropna(subset=["x"])
        def zone(x):
            if x < 40: return "Tiers défensif"
            elif x < 80: return "Tiers médian"
            else: return "Tiers offensif"
        t_ev["zone"] = t_ev["x"].apply(zone)
        return t_ev["zone"].value_counts().reindex(["Tiers défensif","Tiers médian","Tiers offensif"], fill_value=0)

    zones_h = zone_breakdown(home_team)
    zones_a = zone_breakdown(away_team)

    fig_zones = go.Figure()
    zones_order = ["Tiers défensif", "Tiers médian", "Tiers offensif"]
    colors_z = ["#ef4444", "#f59e0b", "#4ade80"]

    for z, c in zip(zones_order, colors_z):
        fig_zones.add_trace(go.Bar(
            name=z, x=[home_team, away_team],
            y=[zones_h[z], zones_a[z]],
            marker_color=c
        ))

    fig_zones.update_layout(
        barmode="stack",
        plot_bgcolor="#0d0f14", paper_bgcolor="#0d0f14",
        font=dict(color="#e8eaf0", family="Inter"),
        xaxis=dict(gridcolor="#1c2030", color="#6b7280"),
        yaxis=dict(title="Nb d'actions", gridcolor="#1c2030", color="#6b7280"),
        legend=dict(bgcolor="#161a24", bordercolor="#252a38"),
        height=280, margin=dict(t=10, b=40, l=50, r=20)
    )
    st.plotly_chart(fig_zones, use_container_width=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-family:\'DM Mono\',monospace;font-size:0.65rem;color:#374151;">'
    '⚽ Tactical Dashboard · Julie Landrevie · Data : StatsBomb Open Data'
    '</div>',
    unsafe_allow_html=True
)
