"""Tactical Dashboard — Julie Landrevie (français / anglais, clair / sombre).

Réseau de passes, xG et tirs, pressing, cartes de chaleur pour n'importe quel match StatsBomb Open Data.
Charte commune : jl_ui.py et .streamlit/config.toml.
"""
import warnings

import streamlit as st

warnings.filterwarnings("ignore")

from jl_ui import C, SEQ, footer, fr_num, header, is_dark, kpi, mpl_style, pitch_kwargs, plotly_style, rgba, setup, t  # noqa: E402

setup("Tactical Dashboard — Julie Landrevie", "Tactical Dashboard — Julie Landrevie", icon="⚽")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from mplsoccer import Pitch, VerticalPitch  # noqa: E402
from statsbombpy import sb  # noqa: E402

from name_resolver import build_name_map  # noqa: E402

mpl_style()
HOME, AWAY = C["teal"], C["rust"]                       # domicile vert d'eau, extérieur rouille
TEAL_MAP = LinearSegmentedColormap.from_list("jl_teal", [C["bg"], SEQ[1], C["teal"], SEQ[4]])

header("Tactical Dashboard",
       t("Réseau de passes, tirs et xG, pressing et zones d’activité, pour n’importe quel match des données ouvertes StatsBomb.",
         "Pass network, shots and xG, pressing and activity zones, for any match in the StatsBomb open data."))

# ─── DONNÉES ──────────────────────────────────────────────────────────────────
COMPETITIONS = {
    # ── Football féminin ──
    "🏆 UEFA Women's Euro 2025": (53, 315),
    "🏆 UEFA Women's Euro 2022": (53, 106),
    "🌍 Women's World Cup 2023": (72, 107),
    "🌍 Women's World Cup 2019": (72, 30),
    "🏴 FA Women's Super League 2023/2024": (37, 281),
    "🏴 FA Women's Super League 2020/2021": (37, 90),
    "🇩🇪 Frauen-Bundesliga 2023/2024": (135, 281),
    "🇪🇸 Liga F 2023/2024": (182, 281),
    "🇮🇹 Serie A Women 2023/2024": (131, 281),
    "🇺🇸 NWSL 2023": (49, 107),
    # ── Compétitions internationales ──
    "🌍 FIFA World Cup 2022": (43, 106),
    "🌍 FIFA World Cup 2018": (43, 3),
    "🌍 FIFA World Cup 1990": (43, 55),
    "🌍 FIFA World Cup 1986": (43, 54),
    "🏆 UEFA Euro 2024": (55, 282),
    "🏆 UEFA Euro 2020": (55, 43),
    "🏆 Copa America 2024": (223, 282),
    "🏆 African Cup of Nations 2023": (1267, 107),
    # ── Champions League ──
    "⭐ Champions League 2018/2019": (16, 4),
    "⭐ Champions League 2017/2018": (16, 1),
    "⭐ Champions League 2016/2017": (16, 2),
    "⭐ Champions League 2015/2016": (16, 27),
    "⭐ Champions League 2014/2015": (16, 26),
    "⭐ Champions League 2013/2014": (16, 25),
    "⭐ Champions League 2012/2013": (16, 24),
    "⭐ Champions League 2011/2012": (16, 23),
    "⭐ Champions League 2010/2011": (16, 22),
    "⭐ Champions League 2009/2010": (16, 21),
    "⭐ Champions League 2008/2009": (16, 41),
    # ── Ligues nationales ──
    "🇪🇸 La Liga 2020/2021": (11, 90),
    "🇪🇸 La Liga 2019/2020": (11, 42),
    "🇪🇸 La Liga 2018/2019": (11, 4),
    "🇪🇸 La Liga 2017/2018": (11, 1),
    "🇪🇸 La Liga 2016/2017": (11, 2),
    "🇪🇸 La Liga 2015/2016": (11, 27),
    "🇫🇷 Ligue 1 2022/2023": (7, 235),
    "🇫🇷 Ligue 1 2021/2022": (7, 108),
    "🇫🇷 Ligue 1 2015/2016": (7, 27),
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League 2015/2016": (2, 27),
    "🇩🇪 Bundesliga 2023/2024": (9, 281),
    "🇩🇪 Bundesliga 2015/2016": (9, 27),
    "🇮🇹 Serie A 2015/2016": (12, 27),
    "🇺🇸 MLS 2023": (44, 107),
}
EVENT_NAMES = {"Pass": ("Passe", "Pass"), "Carry": ("Conduite", "Carry"), "Pressure": ("Pression", "Pressure"),
               "Shot": ("Tir", "Shot"), "Dribble": ("Dribble", "Dribble"),
               "Ball Recovery": ("Récupération", "Ball recovery")}


@st.cache_data(show_spinner=False)
def load_matches(cid, sid):
    return sb.matches(competition_id=cid, season_id=sid)


@st.cache_data(show_spinner=False)
def load_events(mid):
    return sb.events(match_id=mid)


@st.cache_data(show_spinner=False)
def get_name_map(mid):
    return build_name_map(load_events(mid))


with st.sidebar:
    st.markdown(f"### {t('Paramètres', 'Settings')}")
    comp_choice = st.selectbox(t("Compétition", "Competition"), list(COMPETITIONS.keys()))
    comp_id, season_id = COMPETITIONS[comp_choice]
    with st.spinner(t("Chargement des matchs…", "Loading matches…")):
        matches_df = load_matches(comp_id, season_id)
    teams = sorted(set(matches_df["home_team"].tolist() + matches_df["away_team"].tolist()))

    filter_mode = st.radio(t("Filtrer par", "Filter by"), ["one", "all"], horizontal=True,
                           format_func=lambda k: t("Une équipe", "One team") if k == "one" else t("Toutes les équipes", "All teams"))
    if filter_mode == "one":
        team = st.selectbox(t("Équipe", "Team"), teams)
        filtered_matches = matches_df[(matches_df["home_team"] == team) | (matches_df["away_team"] == team)].copy()
    else:
        filtered_matches = matches_df.copy()

    filtered_matches = filtered_matches.sort_values(["home_team", "away_team"])
    filtered_matches["label"] = filtered_matches.apply(
        lambda r: f"{r['home_team']} {r['home_score']}-{r['away_score']} {r['away_team']}", axis=1)
    match_label = st.selectbox(t("Match", "Match"), filtered_matches["label"].tolist())
    match_row = filtered_matches[filtered_matches["label"] == match_label].iloc[0]
    match_id = int(match_row["match_id"])

    with st.spinner(t("Chargement des événements…", "Loading events…")):
        events = load_events(match_id)
    name_map = get_name_map(match_id)

    home_team, away_team = match_row["home_team"], match_row["away_team"]
    home_score, away_score = match_row["home_score"], match_row["away_score"]

    st.divider()
    st.markdown(f"**{home_team} {home_score} – {away_score} {away_team}**")
    st.caption(t(f"{int(len(events))} événements chargés · domicile en vert d’eau, extérieur en rouille",
                 f"{int(len(events))} events loaded · home in teal, away in rust"))


def xy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["x"] = df["location"].apply(lambda l: l[0] if isinstance(l, list) else np.nan)
    df["y"] = df["location"].apply(lambda l: l[1] if isinstance(l, list) else np.nan)
    return df


def short(team: str) -> str:
    return team.replace(" Women's", "")


tab1, tab2, tab3, tab4 = st.tabs([
    t("🕸️ Réseau de passes", "🕸️ Pass network"), t("🎯 Tirs et xG", "🎯 Shots and xG"),
    t("🛡️ Pressing", "🛡️ Pressing"), t("🔥 Zones d’activité", "🔥 Heatmaps")])

# ─── 1. RÉSEAU DE PASSES ──────────────────────────────────────────────────────
with tab1:
    st.markdown(f"### {t('Réseau de passes et structure d’équipe', 'Pass network and team structure')}")
    st.caption(t("Connexions entre joueuses ou joueurs du onze de départ, à partir des passes réussies (au moins 3 entre deux "
                 "personnes). Taille des cercles : volume de passes ; épaisseur des traits : fréquence de la combinaison.",
                 "Links between starting players, from completed passes (at least 3 between two players). Circle size: "
                 "number of passes; line width: how often the combination occurs."))

    def build_pass_network(events, team_name, fig_title, color):
        passes = events[(events["type"] == "Pass") & (events["team"] == team_name) &
                        (events["pass_outcome"].isna()) & (events["period"].isin([1, 2]))].copy()
        tactics = events[(events["type"] == "Starting XI") & (events["team"] == team_name)]
        xi_players = None
        if not tactics.empty and isinstance(tactics.iloc[0]["tactics"], dict):
            xi_players = [p["player"]["name"] for p in tactics.iloc[0]["tactics"].get("lineup", [])]
        if not xi_players:
            xi_players = passes["player"].unique().tolist()[:11]
        passes = passes[passes["player"].isin(xi_players) & passes["pass_recipient"].isin(xi_players)]
        if passes.empty:
            return None
        passes = xy(passes)
        avg_pos = passes.groupby("player")[["x", "y"]].mean().join(passes.groupby("player").size().rename("n_passes"))
        pairs = passes.groupby(["player", "pass_recipient"]).size().reset_index(name="count")
        pairs = pairs[pairs["count"] >= 3]

        fig, ax = plt.subplots(figsize=(8, 5.5))
        pitch = Pitch(pitch_type="statsbomb", **pitch_kwargs())
        pitch.draw(ax=ax)
        max_count = pairs["count"].max() if not pairs.empty else 1
        for _, row in pairs.iterrows():
            if row["player"] in avg_pos.index and row["pass_recipient"] in avg_pos.index:
                a, b = avg_pos.loc[row["player"]], avg_pos.loc[row["pass_recipient"]]
                ax.plot([a["x"], b["x"]], [a["y"], b["y"]], color=color, alpha=0.2 + 0.6 * row["count"] / max_count,
                        linewidth=0.5 + 3.5 * row["count"] / max_count, zorder=1)
        max_passes = avg_pos["n_passes"].max()
        for player, row in avg_pos.iterrows():
            if pd.notna(row["x"]) and pd.notna(row["y"]):
                ax.scatter(row["x"], row["y"], s=200 + 600 * row["n_passes"] / max_passes, color=color,
                           edgecolors=C["bg"], linewidths=1.5, zorder=3)
                ax.text(row["x"], row["y"] - 4.5, name_map.get(player, player.split()[-1]), fontsize=7,
                        color=C["ink"], ha="center", va="top", fontweight="bold", zorder=4)
        ax.set_title(fig_title, color=C["ink"], fontsize=12, pad=10)
        fig.tight_layout()
        return fig

    col_team1, col_team2 = st.columns(2)
    for col, team_name, tag, color in [(col_team1, home_team, t("Domicile", "Home"), HOME),
                                       (col_team2, away_team, t("Extérieur", "Away"), AWAY)]:
        with col:
            fig = build_pass_network(events, team_name, f"{tag} · {team_name}", color)
            if fig:
                st.pyplot(fig, width="stretch")
                plt.close(fig)
            else:
                st.info(t("Données insuffisantes pour ce match.", "Not enough data for this match."))

    st.markdown(f"### {t('Statistiques de passes', 'Passing statistics')}")
    cols = st.columns(4)
    for i, team_name in enumerate([home_team, away_team]):
        t_passes = events[(events["type"] == "Pass") & (events["team"] == team_name)]
        total = len(t_passes)
        completed = int(t_passes["pass_outcome"].isna().sum())
        pct = round(100 * completed / total, 1) if total > 0 else 0
        avg_len = round(t_passes["pass_length"].mean(), 1) if "pass_length" in t_passes.columns else 0
        kpi(cols[2 * i], str(completed), t(f"{short(team_name)} — passes réussies", f"{short(team_name)} — completed passes"))
        kpi(cols[2 * i + 1], fr_num(pct, 1, pct=True),
            t(f"précision · {fr_num(avg_len, 1)} m en moyenne", f"accuracy · {fr_num(avg_len, 1)} m on average"))

# ─── 2. TIRS ET xG ────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f"### {t('Tirs et buts attendus (xG)', 'Shots and expected goals (xG)')}")
    st.caption(t("Taille du point : valeur xG du tir. Rouille : but ; vert d’eau plein : arrêté ; cercle vert d’eau : contré ; "
                 "gris : hors cadre (poteau compris). Séance de tirs au but exclue.",
                 "Dot size: shot xG. Rust: goal; solid teal: saved; teal ring: blocked; grey: off target (woodwork "
                 "included). Penalty shoot-out excluded."))
    shots = xy(events[(events["type"] == "Shot") & (events["period"] < 5)])
    shots["xg"] = pd.to_numeric(shots["shot_statsbomb_xg"], errors="coerce").fillna(0.05)

    def shot_style(outcome):
        if outcome == "Goal":
            return dict(color=C["rust"], edgecolors=C["bg"])
        if outcome == "Saved":
            return dict(color=C["teal"], edgecolors=C["bg"])
        if outcome == "Blocked":
            return dict(color="none", edgecolors=C["teal"])
        return dict(color=C["compare"], edgecolors=C["bg"])

    fig_shot, axes = plt.subplots(1, 2, figsize=(14, 5))
    for idx, team_name in enumerate([home_team, away_team]):
        ax = axes[idx]
        pitch = VerticalPitch(pitch_type="statsbomb", half=True, **pitch_kwargs())
        pitch.draw(ax=ax)
        team_shots = shots[shots["team"] == team_name]
        for _, s in team_shots.iterrows():
            if pd.notna(s["x"]) and pd.notna(s["y"]):
                pitch.scatter(s["x"], s["y"], s=max(50, s["xg"] * 1200), linewidths=1.6, alpha=0.9, ax=ax, zorder=3,
                              **shot_style(s["shot_outcome"]))
        goals = int((team_shots["shot_outcome"] == "Goal").sum())
        ax.set_title(t(f"{short(team_name)}\n{len(team_shots)} tirs · {goals} but(s) · xG {team_shots['xg'].sum():.2f}".replace(".", ","),
                       f"{short(team_name)}\n{len(team_shots)} shots · {goals} goal(s) · xG {team_shots['xg'].sum():.2f}"),
                     color=C["ink"], fontsize=11, pad=8)
    legend_items = [Line2D([0], [0], marker="o", ls="", markerfacecolor=C["rust"], markeredgecolor=C["rust"], markersize=9, label=t("But", "Goal")),
                    Line2D([0], [0], marker="o", ls="", markerfacecolor=C["teal"], markeredgecolor=C["teal"], markersize=9, label=t("Arrêté", "Saved")),
                    Line2D([0], [0], marker="o", ls="", markerfacecolor="none", markeredgecolor=C["teal"], markersize=9, label=t("Contré", "Blocked")),
                    Line2D([0], [0], marker="o", ls="", markerfacecolor=C["compare"], markeredgecolor=C["compare"], markersize=9, label=t("Hors cadre", "Off target"))]
    fig_shot.legend(handles=legend_items, loc="lower center", ncol=4, fontsize=9)
    fig_shot.tight_layout(rect=(0, 0.06, 1, 1))
    st.pyplot(fig_shot, width="stretch")
    plt.close(fig_shot)

    st.markdown(f"### {t('xG cumulé au fil du match', 'Cumulative xG through the match')}")
    shots_sorted = shots.sort_values("minute")
    fig_xg = go.Figure()
    match_end = max(int(events["minute"].max()), 90)
    for team_name, color, fill in [(home_team, HOME, rgba(HOME, 0.14)), (away_team, AWAY, rgba(AWAY, 0.14))]:
        tm = shots_sorted[shots_sorted["team"] == team_name].copy()
        tm["cum_xg"] = tm["xg"].cumsum()
        final_xg = tm["cum_xg"].iloc[-1] if len(tm) else 0
        tm = pd.concat([pd.DataFrame({"minute": [0], "cum_xg": [0]}), tm[["minute", "cum_xg"]],
                        pd.DataFrame({"minute": [match_end], "cum_xg": [final_xg]})])
        fig_xg.add_trace(go.Scatter(x=tm["minute"], y=tm["cum_xg"], mode="lines", name=short(team_name),
                                    line=dict(color=color, width=3, shape="hv"), fill="tozeroy", fillcolor=fill))
    fig_xg.update_layout(xaxis_title="Minute", yaxis_title=t("xG cumulé", "Cumulative xG"))
    st.plotly_chart(plotly_style(fig_xg, height=300), width="stretch", theme="streamlit")

    st.markdown(f"### {t('Statistiques de tirs', 'Shooting statistics')}")
    cols_xg = st.columns(6)
    metrics = []
    for team_name in [home_team, away_team]:
        tm = shots[shots["team"] == team_name]
        xg_txt = f"{tm['xg'].sum():.2f}"
        metrics += [(t(f"tirs · {short(team_name)}", f"shots · {short(team_name)}"), len(tm)),
                    (t("cadrés", "on target"), int(tm["shot_outcome"].isin(["Goal", "Saved"]).sum())),
                    ("xG", t(xg_txt.replace(".", ","), xg_txt))]
    for i, (label, val) in enumerate(metrics):
        kpi(cols_xg[i], str(val), label)

# ─── 3. PRESSING ──────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"### {t('Intensité de pressing et bloc défensif', 'Pressing intensity and defensive block')}")
    st.caption(t("Zones de pression (densité, vert d’eau) et récupérations de balle (losanges rouille). La densité révèle le bloc "
                 "défensif et l’intensité du contre-pressing.",
                 "Pressure zones (density, teal) and ball recoveries (rust diamonds). The density shows the defensive block "
                 "and counter-pressing intensity."))
    pressures = xy(events[events["type"] == "Pressure"])
    recoveries = xy(events[events["type"] == "Ball Recovery"])

    fig_press, axes2 = plt.subplots(1, 2, figsize=(14, 5.5))
    for idx, team_name in enumerate([home_team, away_team]):
        ax = axes2[idx]
        pitch = Pitch(pitch_type="statsbomb", **pitch_kwargs())
        pitch.draw(ax=ax)
        t_press = pressures[pressures["team"] == team_name].dropna(subset=["x", "y"])
        t_recov = recoveries[recoveries["team"] == team_name].dropna(subset=["x", "y"])
        if len(t_press) > 3:
            pitch.kdeplot(t_press["x"], t_press["y"], ax=ax, cmap=TEAL_MAP, fill=True, levels=12, alpha=0.75, bw_adjust=0.8)
        if len(t_recov):
            pitch.scatter(t_recov["x"], t_recov["y"], s=55, color=C["rust"], edgecolors=C["bg"], linewidths=0.8,
                          alpha=0.85, ax=ax, zorder=4, marker="D")
        ratio = round(len(t_press) / max(len(t_recov), 1), 1)
        ax.set_title(t(f"{short(team_name)}\n{len(t_press)} pressions · {len(t_recov)} récupérations · ratio {str(ratio).replace('.', ',')}",
                       f"{short(team_name)}\n{len(t_press)} pressures · {len(t_recov)} recoveries · ratio {ratio}"),
                     color=C["ink"], fontsize=10.5, pad=8)
    fig_press.tight_layout()
    st.pyplot(fig_press, width="stretch")
    plt.close(fig_press)

    st.markdown(f"### {t('Pressions par tranche de 10 minutes', 'Pressures per 10-minute period')}")
    bins = list(range(0, 100, 10))
    labels = [f"{b}-{b + 10}'" for b in bins[:-1]]
    h_counts, _ = np.histogram(pressures[pressures["team"] == home_team]["minute"].dropna(), bins=bins)
    a_counts, _ = np.histogram(pressures[pressures["team"] == away_team]["minute"].dropna(), bins=bins)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=labels, y=h_counts, name=short(home_team), marker_color=HOME))
    fig_bar.add_trace(go.Bar(x=labels, y=-a_counts, name=short(away_team), marker_color=AWAY,
                             customdata=a_counts, hovertemplate="%{x}" + t(" : ", ": ") + "%{customdata}<extra></extra>"))
    fig_bar.update_layout(barmode="relative", xaxis_title=t("Tranche de temps", "Time period"),
                          yaxis_title=t("Pressions (extérieur vers le bas)", "Pressures (away shown downwards)"))
    st.plotly_chart(plotly_style(fig_bar, height=300), width="stretch", theme="streamlit")

# ─── 4. ZONES D'ACTIVITÉ ──────────────────────────────────────────────────────
with tab4:
    st.markdown(f"### {t('Zones d’activité', 'Activity zones')}")
    st.caption(t("Densité des actions d’une équipe ou d’une joueuse ou d’un joueur : zones d’influence, couloirs préférés, "
                 "espaces exploités.",
                 "Density of a team’s or a player’s actions: areas of influence, preferred channels, spaces exploited."))
    col_hm1, col_hm2 = st.columns([1, 2])
    with col_hm1:
        hm_team = st.selectbox(t("Équipe", "Team"), [home_team, away_team], key="hm_team")
        hm_mode = st.radio(t("Mode", "Mode"), ["team", "player"], key="hm_mode",
                           format_func=lambda k: t("Équipe complète", "Whole team") if k == "team" else t("Une joueuse / un joueur", "One player"))
        team_events = events[events["team"] == hm_team].copy()
        selected_player = None
        if hm_mode == "player":
            selected_player = st.selectbox(t("Joueuse / joueur", "Player"), sorted(team_events["player"].dropna().unique().tolist()),
                                           key="hm_player")
        event_types = st.multiselect(t("Types d’actions", "Action types"), list(EVENT_NAMES), default=["Pass", "Carry"],
                                     format_func=lambda k: t(*EVENT_NAMES[k]), key="hm_events")
    with col_hm2:
        if event_types:
            filtered = team_events[team_events["type"].isin(event_types)]
            if selected_player:
                filtered = filtered[filtered["player"] == selected_player]
            filtered = xy(filtered).dropna(subset=["x", "y"])
            fig_hm, ax_hm = plt.subplots(figsize=(9, 6))
            pitch_hm = Pitch(pitch_type="statsbomb", **pitch_kwargs())
            pitch_hm.draw(ax=ax_hm)
            if len(filtered) > 5:
                pitch_hm.kdeplot(filtered["x"], filtered["y"], ax=ax_hm, cmap=TEAL_MAP, fill=True, levels=20,
                                 alpha=0.8, bw_adjust=0.65)
            else:
                pitch_hm.scatter(filtered["x"], filtered["y"], s=80, color=C["teal"], alpha=0.7, ax=ax_hm)
            title_str = selected_player or hm_team
            names = ", ".join(t(*EVENT_NAMES[e]).lower() for e in event_types)
            ax_hm.set_title(f"{title_str} · {names}\n{len(filtered)} actions", color=C["ink"], fontsize=11, pad=10)
            fig_hm.tight_layout()
            st.pyplot(fig_hm, width="stretch")
            plt.close(fig_hm)
        else:
            st.info(t("Choisis au moins un type d’action.", "Choose at least one action type."))

    st.markdown(f"### {t('Répartition par tiers du terrain', 'Split by thirds of the pitch')}")
    zones = [("def", t("Tiers défensif", "Defensive third"), C["compare"]),
             ("mid", t("Tiers médian", "Middle third"), SEQ[1]),
             ("att", t("Tiers offensif", "Attacking third"), C["teal"])]

    def zone_breakdown(team_name):
        t_ev = xy(events[(events["team"] == team_name) & (events["type"].isin(["Pass", "Carry", "Pressure"]))]).dropna(subset=["x"])
        z = np.where(t_ev["x"] < 40, "def", np.where(t_ev["x"] < 80, "mid", "att"))
        return pd.Series(z).value_counts().reindex(["def", "mid", "att"], fill_value=0)

    zh, za = zone_breakdown(home_team), zone_breakdown(away_team)
    fig_zones = go.Figure()
    for key, label, color in zones:
        fig_zones.add_trace(go.Bar(name=label, x=[short(home_team), short(away_team)], y=[zh[key], za[key]], marker_color=color))
    fig_zones.update_layout(barmode="stack", yaxis_title=t("Nombre d’actions (passes, conduites, pressions)",
                                                            "Number of actions (passes, carries, pressures)"))
    st.plotly_chart(plotly_style(fig_zones, height=320), width="stretch", theme="streamlit")

footer("Data: StatsBomb (Open Data)")
