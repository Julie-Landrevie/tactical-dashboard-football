"""
name_resolver.py
Résolution des noms de maillot pour les joueurs StatsBomb open data.

Règles :
1. Dictionnaire player_id → nom maillot pour les cas particuliers
   (prénom seul, prénom+nom, surnom)
2. Fallback : dernier nom significatif (après suppression des particules
   et des prénoms composés)
"""

# ─── CAS PARTICULIERS : player_id → nom maillot ──────────────────────────────
# Uniquement les joueurs où le fallback donnerait un mauvais résultat :
# - connus par prénom seul (Neymar, Ronaldinho)
# - connus par prénom+nom (Cristiano Ronaldo, Lamine Yamal)
# - surnom différent du nom (Casemiro, Fabinho, Fred)
# - dernier nom ambigu ou trop long (Cuccittini, Aveiro, Barbosa...)

SHIRT_NAMES: dict[int, str] = {
    # ── Prénom seul ──
    4320:  "Neymar",
    3009:  "Mbappé",          # Kylian Mbappé Lottin
    # ── France / Ligue 1 ──
    2999:  "Kimpembe",        # Presnel Kimpembe
    41092: "Nuno Mendes",     # Nuno Mendes
    4353:  "Laporte",         # Aymeric Laporte
    # ── Espagne ──
    68574: "Nico Williams",   # Nicholas Williams Arthuer
    11748: "Unai Simón",      # Unai Simón Mendibil (gardien)
    5202:  "Nacho",           # José Ignacio Fernández Iglesias
    6821:  "Jesús Navas",     # Jesús Navas González
    6655:  "Fabián",          # Fabián Ruiz Peña
    15651: "Bernat",          # Juan Bernat Velasco
    4372:  "Marquinhos",      # Marcos Aoás Corrêa (PSG)
    # ── Gardiens (noms de famille uniquement) ──
    5597:  "K. Navas",        # Keylor Navas Gamboa
    # ── Belgique ──
    3077:  "Vertonghen",      # Jan Vertonghen
    20005: "Alderweireld",    # Toby Alderweireld
    3509:  "Courtois",        # Thibaut Courtois
    3621:  "Hazard",          # Eden Hazard
    5632:  "T. Hazard",       # Thorgan Hazard
    5642:  "Witsel",          # Axel Witsel
    6989:  "Castagne",        # Timothy Castagne
    2954:  "Tielemans",       # Youri Tielemans
    6331:  "Dendoncker",      # Leander Dendoncker
    3457:  "Batshuayi",       # Michy Batshuayi Tunga
    3289:  "Lukaku",          # Romelu Lukaku Menama
    5633:  "Carrasco",        # Yannick Ferreira Carrasco
    3176:  "Meunier",         # Thomas Meunier
    5630:  "Mertens",         # Dries Mertens
    3089:  "De Bruyne",       # Kevin De Bruyne
    8240:  "Casteels",        # Koen Casteels
    48347: "Onana",           # Amadou Onana
    43913: "Theate",          # Arthur Theate
    32688: "De Ketelaere",    # Charles De Ketelaere
    23650: "Doku",            # Jeremy Doku
    16559: "Trossard",        # Leandro Trossard
    16275: "Openda",          # Ikoma Loïs Openda
    8950:  "Mangala",         # Orel Mangala
    8854:  "Faes",            # Wout Faes
    114832:"Debast",          # Zeno Debast
    52218: "Bakayoko",        # Johan Bakayoko
    12306: "Lukebakio",       # Dodi Lukebakio
    # ── Gardiens nommés par prénom+nom ──
    20055: "ter Stegen",      # Marc-André ter Stegen
    # ── Divers ──
    # ── France ──
    17592: "Saliba",           # William Saliba
    8519:  "Upamecano",        # Dayotchanculle Upamecano
    3026:  "Rabiot",           # Adrien Rabiot
    3761:  "Maignan",          # Mike Maignan
    4445:  "Koundé",           # Jules Koundé
    5477:  "Dembélé",          # Ousmane Dembélé
    3961:  "Kanté",            # N'Golo Kanté
    3604:  "Giroud",           # Olivier Giroud
    5485:  "Varane",           # Raphaël Varane
    3099:  "Lloris",           # Hugo Lloris
    24778: "Camavinga",        # Eduardo Camavinga
    12509: "M. Dembélé",       # Moussa Dembélé (différent d'Ousmane)
    11392: "Arthur",          # Arthur Henrique Ramos de Oliveira Melo
    3166:  "Verratti",        # Marco Verratti (2 parts, fallback ok mais on précise)
    7036:  "Donnarumma",      # Gianluigi Donnarumma (idem)

    # ── Prénom + Nom (les deux sont nécessaires) ──
    5207:  "Cristiano Ronaldo",
    316046:"Lamine Yamal",
    12041: "João Félix",
    43565: "Min-jae Kim",

    # ── Surnom / nom d'usage différent du nom civil ──
    5539:  "Casemiro",       # Carlos Henrique Casimiro
    3247:  "Fabinho",        # Fábio Henrique Tavares
    9904:  "Fred",           # Frederico Rodrigues Santos
    3202:  "Gabriel Jesus",  # Gabriel Fernando de Jesus
    3280:  "Richarlison",    # Richarlison de Andrade
    25363: "Antony",         # Antony Matheus dos Santos
    29976: "Martinelli",     # Gabriel Teodoro Martinelli Silva
    10595: "Raphinha",       # Raphael Dias Belloli
    3745:  "Lucas Moura",    # Lucas Rodrigues Moura da Silva
    22600: "Paquetá",        # Lucas Tolentino Coelho de Lima
    5552:  "Marcelo",        # Marcelo Vieira da Silva Júnior
    18395: "Vinicius Jr",    # Vinícius José Paixão de Oliveira Júnior
    25104: "Rodrygo",        # Rodrygo Silva de Goes
    4355:  "Emerson",        # Emerson Palmieri dos Santos
    3063:  "Danilo",         # Danilo Luiz da Silva
    6945:  "Alex Sandro",    # Alex Sandro Lobo Silva
    5547:  "Alisson",        # Alisson Ramsés Becker
    3193:  "Bernardo Silva", # Bernardo Mota Veiga de Carvalho e Silva
    3295:  "Thiago Silva",   # Thiago Emiliano da Silva
    3535:  "Firmino",        # Roberto Firmino Barbosa de Oliveira
    9927:  "Rúben Neves",    # Rúben Diogo Da Silva Neves
    5206:  "Rúben Dias",     # Rúben Santos Gato Alves Dias
    18360: "Rafael Leão",    # Rafael Alexandre Conceição Leão
    13621: "Danilo Pereira", # Danilo Luís Hélio Pereira
    34639: "Vitinha",        # Vitor Machado Ferreira
    3154:  "Miguel",         # Miguel Ângelo da Silva Rocha
    5204:  "Bruno Fernandes",# Bruno Miguel Borges Fernandes
    7005:  "Cancelo",        # João Pedro Cavaco Cancelo
    12169: "Palhinha",       # João Maria Lobo Alves Palhinha Gonçalves
    3193:  "Bernardo",       # Bernardo Mota Veiga de Carvalho e Silva
    3593:  "Renato Sanches", # Renato Júnior Luz Sanches
    32478: "Darwin Núñez",   # Darwin Gabriel Núñez Ribeiro
    25142: "Bruno Guimarães",# Bruno Guimarães Rodriguez Moura
    40874: "Matheus Nunes",  # Matheus Luiz Nunes

    # ── Dernier nom ambigu (trop générique ou mal connu) ──
    5503:  "Messi",          # Lionel Andrés Messi Cuccittini
    6909:  "E. Martínez",    # Damián Emiliano Martínez (Dibu)
    11456: "L. Martínez",    # Lautaro Javier Martínez
    7797:  "De Paul",        # Rodrigo Javier De Paul
    2995:  "Di María",       # Ángel Fabián Di María Hernández
    27886: "Mac Allister",   # Alexis Mac Allister
    19597: "Acuña",          # Marcos Javier Acuña
    28263: "Montiel",        # Gonzalo Ariel Montiel
    20572: "Romero",         # Cristian Gabriel Romero
    29201: "Molina",         # Nahuel Molina Lucero
    38718: "E. Fernández",   # Enzo Fernandez
    28268: "Palacios",       # Exequiel Alejandro Palacios
    16308: "Paredes",        # Leandro Daniel Paredes
    5260:  "Bentancur",      # Rodrigo Bentancur Colmán
    6773:  "Valverde",       # Federico Santiago Valverde Dipetta
    5255:  "Vecino",         # Matías Vecino Falero
    4319:  "Cavani",         # Edinson Roberto Cavani Gómez
    5249:  "Godín",          # Diego Roberto Godín Leal
    3385:  "A. Sánchez",     # Alexis Alejandro Sánchez Sánchez
    7006:  "Papu Gómez",     # Alejandro Darío Gómez
    6765:  "Rodri",          # Rodrigo Hernández Cascante
    5201:  "Ramos",          # Sergio Ramos García
    5203:  "Busquets",       # Sergio Busquets i Burgos
    5213:  "Piqué",          # Gerard Piqué Bernabéu
    5211:  "Jordi Alba",     # Jordi Alba Ramos
    5719:  "Asensio",        # Marco Asensio Willemsen
    6685:  "Oyarzabal",      # Mikel Oyarzabal Ugarte
    6655:  "Fabián",         # Fabián Ruiz Peña
    16532: "Dani Olmo",      # Daniel Olmo Carvajal
    3477:  "Morata",         # Álvaro Borja Morata Martín
    3042:  "Merino",         # Mikel Merino Zazón
    4926:  "Isco",           # Francisco Román Alarcón Suárez
    5721:  "Carvajal",       # Daniel Carvajal Ramos
    6821:  "Jesús Navas",    # Jesús Navas González
    6748:  "Ferran Torres",  # Ferrán Torres García
    6892:  "Pau Torres",     # Pau Francisco Torres
    24921: "Zubimendi",      # Martín Zubimendi Ibáñez
    3606:  "Ander Herrera",  # Ander Herrera Agüera
    6583:  "Carlos Soler",   # Carlos Soler Barragán
    8206:  "Vidal",          # Arturo Erasmo Vidal Pardo
    5487:  "Griezmann",      # Antoine Griezmann (2 parts, ok mais on le garde)
    10481: "Tchouaméni",     # Aurélien Djani Tchouaméni
    6704:  "T. Hernández",   # Theo Bernard François Hernández
    22097: "Kolo Muani",     # Randal Kolo Muani
    22128: "Le Normand",     # Robin Aime Robert Le Normand
    3436:  "Gana Gueye",     # Idrissa Gana Gueye
    5597:  "Keylor Navas",   # Keylor Navas Gamboa
    6987:  "Icardi",         # Mauro Emanuel Icardi Rivero
    7345:  "Guendouzi",      # Mattéo Guendouzi Olié
    3007:  "Ikoné",          # Nanitamo Jonathan Ikoné
    3019:  "Sambia",         # Salomon Junior Sambia
    3199:  "Lees-Melou",     # Pierre Lees Melou
    2935:  "Mukiele",        # Nordi Mukiele Mulere
    3229:  "Le Marchand",    # Maxime Le Marchand
    45172: "Le Douaron",     # Jérémy Le Douaron
    5245:  "Hakimi",         # Achraf Hakimi Mouh
    3551:  "Toko Ekambi",    # Karl Brillant Toko Ekambi
    3141:  "Anguissa",       # André-Frank Zambo Anguissa
    5246:  "Suárez",         # Luis Alberto Suárez Díaz
    3090:  "Otamendi",       # Nicolás Hernán Otamendi
    5507:  "Tagliafico",     # Nicolás Alejandro Tagliafico
    20750: "Gakpo",          # Cody Mathès Gakpo
    8118:  "F. de Jong",     # Frenkie de Jong
    20033: "L. de Jong",     # Luuk de Jong
    3669:  "Van Dijk",       # Virgil van Dijk
    7787:  "De Vrij",        # Stefan de Vrij
    32547: "Van de Ven",     # Micky van de Ven
    21809: "Timber",         # Jurriën David Norman Timber
    51672: "Højlund",        # Rasmus Winther Højlund
    3043:  "Eriksen",        # Christian Dannemann Eriksen
    5732:  "Cornelius",      # Andreas Evald Cornelius
    4447:  "Braithwaite",    # Martin Braithwaite Christensen
    5537:  "Schär",          # Fabian Lukas Schär
    5544:  "R. Rodríguez",   # Ricardo Iván Rodríguez Araya
    5549:  "Akanji",         # Manuel Obafemi Akanji
    5538:  "Zakaria",        # Denis Lemi Zakaria Lako Lado
    3532:  "Henderson",      # Jordan Brian Henderson
    3473:  "Milner",         # James Philip Milner
    4090:  "Lallana",        # Adam David Lallana
    3502:  "Matip",          # Joël Andre Job Matip
    4747:  "Origi",          # Divock Okoth Origi
    3822:  "Konsa",          # Ezri Konsa Ngoyo
    5492:  "Umtiti",         # Samuel Yves Umtiti
    6374:  "Semedo",         # Nélson Cabral Semedo
    7030:  "Albiol",         # Raúl Albiol i Tortajada
    5217:  "Aspas",          # Iago Aspas Juncal
    6379:  "Sergi Roberto",  # Sergi Roberto Carnicer
    6766:  "G. Moreno",      # Gerard Moreno Balaguero
    6399:  "Bale",           # Gareth Frank Bale
    10802: "André Gomes",    # André Filipe Tavares Gomes
    3960:  "Fonte",          # José Miguel da Rocha Fonte
    15651: "Bernat",         # Juan Bernat Velasco
    17620: "Cucurella",      # Marc Cucurella Saseta
    6994:  "Rafinha",        # Rafael Alcântara do Nascimento
    20016: "Kléber",         # Kléper Laveran Lima Ferreira
    144059:"W. Zaïre-Emery", # Warren Zaire Emery
    132019:"Bitshiabu",      # El Chadaille Bitshiabu
    181010:"Kumbedi",        # Sael Kumbedi Nseke
    40185: "Lukeba",         # Junior Castello Lukeba
    35705: "Kalimuendo",     # Arnaud Kalimuendo Muinga
    32649: "Cherki",         # Mathis Rayan Cherki
    44738: "Ugochukwu",      # Lesley Chimuanya Ugochukwu
    39624: "F. Conceição",   # Francisco Fernandes Conceição
    34396: "Estrada",        # Michael Steveen Estrada Martínez
    37945: "A. Franco",      # Alan Steven Franco Palma
    36148: "Cifuentes",      # José Adoni Cifuentes Charcopa
    91090: "Reasco",         # Djorkaeff Neicer Reasco González
    40211: "Sarmiento",      # Jeremy Leonel Sarmiento Morante
    24085: "Estupiñán",      # Pervis Josué Estupiñán Tenorio
    37737: "Preciado",       # Angelo Smit Preciado Quiñónez
    31152: "G. Plata",       # Gonzalo Jordy Plata Jiménez
    33151: "Da Cunha",       # Lucas Da Cunha
    7104:  "M. Olivera",     # Mathías Olivera Miramontes
    5264:  "G. Varela",      # Guillermo Varela Olivera
    34476: "Viña",           # Matías Nicolás Viña Susperreguy
    7161:  "Pezzella",       # Germán Alejandro Pezzella
    33233: "Balerdi",        # Leonardo Julián Balerdi Rossa
    37522: "Galíndez",       # Hernán Ismael Galíndez
    36710: "Rochet",         # Sergio Rochet Álvarez
    5259:  "Giménez",        # José María Giménez de Vargas
    30415: "F. Medina",      # Facundo Axel Medina
    36288: "Pellistri",      # Facundo Pellistri Rebollo
    38004: "Hincapié",       # Piero Martín Hincapié Reyna
    28729: "De La Cruz",     # Diego Nicolás De La Cruz Arcosa
    30111: "F. Torres",      # Felix Eduardo Torres Caicedo (Équateur)
    37726: "M. Caicedo",     # Moisés Isaac Caicedo Corozo
    28559: "E. Valencia",    # Enner Remberto Valencia Lastra
    24909: "Cassamã",        # Moreto Moro Cassamã
    31751: "Pathé Ciss",     # Pathé Ismaël Ciss
    15970: "Pape Cissé",     # Pape Abou Cissé
    13851: "Doucoure",       # Cheick Oumar Doucoure
    88123: "Dieng",          # Cheikh Ahmadou Bamba Mbacke Dieng
    3767:  "Skhiri",         # Ellyes Joris Skhiri
    5655:  "Bronn",          # Dylan Daniel Mahmoud Bronn
    44955: "Laïdouni",       # Aïssa Bilal Laïdouni
    128793:"Khenissi",       # Taha Yassine Khenissi
    32450: "Talbi",          # Montassar Omar Talbi
    48335: "Amdouni",        # Mohamed Zeki Amdouni
    34865: "El Bilal Touré", # El Bilal Toure
    3324:  "Bailly",         # Eric Bertrand Bailly
    6408:  "Oyongo",         # Ambroise Oyongo Bitolo
    16335: "Chukwueze",      # Samuel Chimerenka Chukwueze
    3139:  "Awaziem",        # Chidozie Collins Awaziem
    3257:  "Mounié",         # Steve Michel Mounié
    26063: "Cajuste",        # Jens-Lys Michel Cajuste
    24547: "A. Bah",         # Alexander Hartmann Bah
    60343: "V. Kristiansen", # Victor Bernth Kristansen
    16190: "R. Kristensen",  # Rasmus Nissen Kristensen
    17042: "Skov Olsen",     # Andreas Skov Olsen
    10349: "Zeki Çelik",     # Mehmet Zeki Çelik
    49689: "Aktürkoğlu",     # Muhammed Kerem Aktürkoğlu
    30438: "Kadıoğlu",       # Ferdi Erenay Kadıoğlu
    30310: "Günok",          # Fehmi Mert Günok
    134209:"B. Yılmaz",      # Barış Alper Yılmaz
    133168:"Yıldırım",       # Bertuğ Özgür Yıldırım
    20879: "El Idrissy",     # Mounaim El Idrissy
    32481: "Saracevic",      # Muhammed Cham Saracevic
    33492: "Duke",           # Mitchell Thomas Duke
    8088:  "Van Bergen",     # Mitchell van Bergen
    23826: "De Smet",        # Thibault De Smet
    21261: "Wind",           # Jonas Older Wind
    29992: "Djaló",          # Tiago Emanuel Embaló Djaló
    10848: "Mandava",        # Reinildo Isnard Mandava
    4121:  "Mavididi",       # Stephy Alvaro Mavididi
    19019: "Mendy",          # Arial Benabent Mendy
    63413: "Vitor Oliveira", # Vítor Manuel Carvalho Oliveira
    25153: "Thuler",         # Matheus Soares Thuler
    31308: "Munetsi",        # Marshall Nyasha Munetsi
    51969: "Porozo",         # Jackson Gabriel Porozo Vernaza
    12583: "Gruezo",         # Carlos Armando Gruezo Arboleda
    4476:  "Cozza",          # Nicolas Louis Marcel Cozza
    3680:  "Thiago Mendes",  # Thiago Henrique Mendes Ribeiro
    24665: "V. Borges",      # Vivaldo Borges dos Santos Neto
}

# ─── PARTICULES ET MOTS À IGNORER DANS LE FALLBACK ───────────────────────────
_PARTICLES = {
    "da", "de", "di", "do", "dos", "du", "das",
    "van", "von", "der", "den", "ter",
    "del", "delle", "degli", "della",
    "el", "al", "le", "la", "les",
    "i",        # catalan (Busquets i Burgos)
}

_SUFFIXES = {
    "junior", "júnior", "jr", "jr.",
    "senior", "sr", "sr.",
    "filho", "neto", "neta",
}


# ─── FALLBACK : extraction du nom de famille ─────────────────────────────────
def _algo_short_name(full_name: str) -> str:
    """
    Règle : retourner UNIQUEMENT le nom de famille (dernier mot significatif).
    - Supprime les particules (da, de, van...) et les suffixes (Junior, Jr...)
    - Retourne toujours 1 seul élément : le dernier nom
    - Exception : particules inséparables comme De Bruyne, Van Dijk
      → gérées dans le dictionnaire SHIRT_NAMES, pas ici
    """
    parts = full_name.split()

    if len(parts) == 1:
        return full_name

    # Filtrer particules et suffixes
    filtered = [p for p in parts if p.lower() not in _PARTICLES and p.lower() not in _SUFFIXES]

    if not filtered:
        return parts[-1]

    # Toujours retourner uniquement le dernier élément
    return filtered[-1]


# ─── FONCTION PRINCIPALE ─────────────────────────────────────────────────────
def resolve_shirt_name(full_name: str, player_id=None) -> str:
    """
    Retourne le nom maillot d'un joueur.
    Priorité : dictionnaire manuel → fallback algorithmique.
    """
    if player_id is not None:
        try:
            pid = int(player_id)
            if pid in SHIRT_NAMES:
                return SHIRT_NAMES[pid]
        except (ValueError, TypeError):
            pass
    return _algo_short_name(full_name)


def build_name_map(events_df) -> dict[str, str]:
    """
    Construit un dict {full_name: shirt_name} pour tous les joueurs d'un match.
    """
    players = (
        events_df[["player", "player_id"]]
        .dropna(subset=["player"])
        .drop_duplicates("player")
    )
    result = {}
    for _, row in players.iterrows():
        raw = row.get("player_id")
        try:
            pid = int(raw) if raw is not None and raw == raw else None
        except (ValueError, TypeError):
            pid = None
        result[row["player"]] = resolve_shirt_name(row["player"], pid)
    return result


if __name__ == "__main__":
    test = [
        ("Marco Verratti", 3166),
        ("Gianluigi Donnarumma", 7036),
        ("Kylian Mbappé Lottin", 3009),
        ("Lionel Andrés Messi Cuccittini", 5503),
        ("Neymar da Silva Santos Junior", 4320),
        ("Cristiano Ronaldo dos Santos Aveiro", 5207),
        ("Rodrigo Javier De Paul", 7797),
        ("Aurélien Djani Tchouaméni", 10481),
        ("Theo Bernard François Hernández", 6704),
        ("Antoine Griezmann", 5487),
        ("Alexis Mac Allister", 27886),
        ("Vinícius José Paixão de Oliveira Júnior", 18395),
        ("Roberto Firmino Barbosa de Oliveira", 3535),
        ("Thiago Emiliano da Silva", 3295),
        ("Frenkie de Jong", 8118),
        ("Virgil van Dijk", 3669),
        ("Arthur Henrique Ramos de Oliveira Melo", 11392),
        ("Joueur Inconnu Avec Nom Long", None),
        ("Sergio Ramos García", 5201),
        ("Damián Emiliano Martínez", 6909),
    ]
    for name, pid in test:
        result = resolve_shirt_name(name, pid)
        print(f"{name:45} → {result}")
