from __future__ import annotations
import math
import random
from dataclasses import dataclass, field
from typing import List, Optional
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# -------------------------------
# Modello dati
# -------------------------------

@dataclass
class Team:
    name: str
    rating: int
    points: int = 0
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    gf: int = 0
    ga: int = 0
    initial_rating: int = field(init=False)
    match_history: List[str] = field(default_factory=list)  # "V", "N", "P"

    def __post_init__(self):
        self.initial_rating = self.rating

    @property
    def gd(self) -> int:
        return self.gf - self.ga

    @property
    def win_percentage(self) -> float:
        return (self.wins / self.played * 100) if self.played > 0 else 0.0

    @property
    def avg_goals_for(self) -> float:
        return (self.gf / self.played) if self.played > 0 else 0.0

    @property
    def avg_goals_against(self) -> float:
        return (self.ga / self.played) if self.played > 0 else 0.0

    @property
    def last_5_form(self) -> str:
        return "".join(self.match_history[-5:])

    def reset_stats(self):
        self.points = 0
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.gf = 0
        self.ga = 0
        self.match_history.clear()

@dataclass
class Match:
    home: Team
    away: Team
    goals_home: Optional[int] = None
    goals_away: Optional[int] = None

    @property
    def played(self) -> bool:
        return self.goals_home is not None and self.goals_away is not None

    def result_text(self) -> str:
        if self.played:
            return f"{self.home.name} {self.goals_home} - {self.goals_away} {self.away.name}"
        return f"{self.home.name} vs {self.away.name}"

# -------------------------------
# Utility: generazione calendario
# -------------------------------

def generate_double_round_robin(teams: List[Team]) -> List[List[Match]]:
    """Genera un calendario andata/ritorno con metodo "circle" (Berger).
    Ritorna una lista di giornate, ognuna con una lista di Match.
    """
    n = len(teams)
    if n % 2 != 0:
        teams = teams + [Team("Riposo", 0)]  # non usato qui, ma per completezza
        n += 1
    # Copia per non riordinare l'originale
    rotation = teams[1:]
    fixed = teams[0]

    rounds_first_leg: List[List[Match]] = []
    for r in range(n - 1):
        left = [fixed] + rotation[: (n // 2) - 1]
        right = rotation[(n // 2) - 1 :]
        right = list(reversed(right))
        pairs = list(zip(left, right))
        # Alterna casa/trasferta per bilanciare
        round_matches: List[Match] = []
        for i, (t1, t2) in enumerate(pairs):
            if r % 2 == 0:
                home, away = (t1, t2) if i % 2 == 0 else (t2, t1)
            else:
                home, away = (t2, t1) if i % 2 == 0 else (t1, t2)
            round_matches.append(Match(home=home, away=away))
        rounds_first_leg.append(round_matches)
        # Rotazione
        rotation = rotation[1:] + rotation[:1]

    # Seconda parte: inverti casa/trasferta
    rounds_second_leg: List[List[Match]] = []
    for giornata in rounds_first_leg:
        rev = [Match(home=m.away, away=m.home) for m in giornata]
        rounds_second_leg.append(rev)

    full_schedule = rounds_first_leg + rounds_second_leg
    return full_schedule

def generate_single_round_robin(teams: List[Team]) -> List[List[Match]]:
    full_schedule = generate_double_round_robin(teams)[:len(teams)-1]
    return full_schedule

# -------------------------------
# Simulazione partite
# -------------------------------

def poisson_sample(lam: float) -> int:
    """Campiona da Poisson(lam) via trasformata inversa (senza numpy)."""
    if lam <= 0:
        return 0
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def expected_goals(r_home: int, r_away: int) -> tuple[float, float]:
    """Stima xG medi per casa e trasferta in base ai rating.
    - Base ~2.6 gol totali a partita
    - Vantaggio casa ~ +10%
    - Normalizza in funzione dei rating
    """
    base_goals = 2.6
    home_adv = 1.10
    total = base_goals
    # Pesi dai rating
    r_sum = max(1, r_home + r_away)
    share_home = r_home / r_sum
    share_away = r_away / r_sum
    lam_home = total * share_home * home_adv
    lam_away = total * share_away * (2 - home_adv)  # bilanciamento
    return lam_home, lam_away

def calculate_rating_probabilities(rating_home: int, rating_away: int) -> tuple[float, float]:
    """Calcola le probabilità attese di vittoria per casa e trasferta usando sistema di rating."""
    # Formula: P = 1 / (1 + 10^((Ra - Rb) / 400))
    adjusted_home = rating_home + 1
    diff = adjusted_home - rating_away
    prob_home = 1 / (1 + 10 ** (-diff / 40))  # Scala ridotta per rating 1-99
    prob_away = 1 - prob_home
    return prob_home, prob_away

def update_ratings(home_team: Team, away_team: Team, goals_home: int, goals_away: int, k_factor: float = 2.0):
    """Aggiorna i rating delle squadre in base al risultato usando sistema di rating dinamico."""
    # Calcola probabilità attese prima della partita
    prob_home, prob_away = calculate_rating_probabilities(home_team.rating, away_team.rating)
    
    # Determina il risultato effettivo (1 = vittoria, 0.5 = pareggio, 0 = sconfitta)
    if goals_home > goals_away:
        result_home = 1.0
        result_away = 0.0
    elif goals_home < goals_away:
        result_home = 0.0
        result_away = 1.0
    else:
        result_home = 0.5
        result_away = 0.5
    
    # Calcola variazioni rating
    change_home = k_factor * (result_home - prob_home)
    change_away = k_factor * (result_away - prob_away)
    
    # Applica variazioni (mantieni range 1-99)
    home_team.rating = max(1, min(99, round(home_team.rating + change_home)))
    away_team.rating = max(1, min(99, round(away_team.rating + change_away)))

def simulate_match(match: Match):
    if match.played:
        return
    
    # Salva i rating originali per il calcolo
    original_home_rating = match.home.rating
    original_away_rating = match.away.rating
    
    lam_h, lam_a = expected_goals(original_home_rating, original_away_rating)
    gh = poisson_sample(lam_h)
    ga = poisson_sample(lam_a)
    match.goals_home = gh
    match.goals_away = ga
    
    # Aggiorna statistiche
    h, a = match.home, match.away
    h.played += 1
    a.played += 1
    h.gf += gh; h.ga += ga
    a.gf += ga; a.ga += gh
    
    # Aggiorna risultati e storico
    if gh > ga:
        h.wins += 1; a.losses += 1
        h.points += 3
        h.match_history.append("V")
        a.match_history.append("P")
    elif gh < ga:
        a.wins += 1; h.losses += 1
        a.points += 3
        h.match_history.append("P")
        a.match_history.append("V")
    else:
        h.draws += 1; a.draws += 1
        h.points += 1; a.points += 1
        h.match_history.append("N")
        a.match_history.append("N")
    
    # Aggiorna rating dinamicamente
    update_ratings(h, a, gh, ga)

# -------------------------------
# Ordinamento classifica
# -------------------------------

def standings(teams: List[Team]) -> List[Team]:
    return sorted(
        teams,
        key=lambda t: (t.points, t.gd, t.gf, t.wins, t.rating),
        reverse=True,
    )

# -------------------------------
# UI Tkinter
# -------------------------------

class TeamDetailFrame(ttk.Frame):
    def __init__(self, master, team: Team, schedule: List[List[Match]], on_back):
        super().__init__(master)
        self.team = team
        self.schedule = schedule
        self.on_back = on_back
        self._build_ui()
        self._populate_data()

    def _build_ui(self):
        # Header con nome squadra e pulsante indietro
        header = ttk.Frame(self)
        header.pack(fill="x", pady=10)
        
        ttk.Button(header, text="← Torna alla classifica", command=self.on_back).pack(side="left")
        ttk.Label(header, text=f"Dettaglio: {self.team.name}", 
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=20)

        # Frame principale con 3 colonne
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10)
        
        # Colonna 1: Info squadra
        info_frame = ttk.LabelFrame(main_frame, text="Informazioni Squadra")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0,5), pady=5)
        
        self.info_text = tk.Text(info_frame, height=12, width=30, state="disabled")
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Colonna 2: Ultime partite e forma
        form_frame = ttk.LabelFrame(main_frame, text="Forma e Ultime Partite")
        form_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self.form_text = tk.Text(form_frame, height=12, width=35, state="disabled")
        self.form_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Colonna 3: Calendario
        fixtures_frame = ttk.LabelFrame(main_frame, text="Calendario")
        fixtures_frame.grid(row=0, column=2, sticky="nsew", padx=(5,0), pady=5)
        
        self.fixtures_text = tk.Text(fixtures_frame, height=12, width=35, state="disabled")
        self.fixtures_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configura peso colonne
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def _populate_data(self):
        self._populate_info()
        self._populate_form()
        self._populate_fixtures()

    def _populate_info(self):
        self.info_text.configure(state="normal")
        self.info_text.delete(1.0, tk.END)
        
        info = f"""INFORMAZIONI GENERALI

Nome: {self.team.name}

RATING
Rating iniziale: {self.team.initial_rating}
Rating attuale: {self.team.rating}
Variazione: {self.team.rating - self.team.initial_rating:+d}

RECORD GENERALE
Partite giocate: {self.team.played}
Vittorie: {self.team.wins}
Pareggi: {self.team.draws}
Sconfitte: {self.team.losses}

STATISTICHE AVANZATE
% Vittorie: {self.team.win_percentage:.1f}%
Gol fatti (media): {self.team.avg_goals_for:.2f}
Gol subiti (media): {self.team.avg_goals_against:.2f}
Differenza reti: {self.team.gd:+d}
Punti: {self.team.points}"""

        self.info_text.insert(1.0, info)
        self.info_text.configure(state="disabled")

    def _populate_form(self):
        self.form_text.configure(state="normal")
        self.form_text.delete(1.0, tk.END)
        
        form = f"""FORMA ATTUALE

Ultime 5 partite: {self.team.last_5_form or "Nessuna"}
"""
        
        # Aggiungi statistiche forma se ha giocato
        if self.team.played > 0:
            recent_5 = self.team.match_history[-5:]
            if recent_5:
                wins_5 = recent_5.count("V")
                draws_5 = recent_5.count("N")
                losses_5 = recent_5.count("P")
                form += f"""
FORMA RECENTE (ultime {len(recent_5)})
Vittorie: {wins_5}
Pareggi: {draws_5} 
Sconfitte: {losses_5}
Punti: {wins_5*3 + draws_5}/15"""

        self.form_text.insert(1.0, form)
        self.form_text.configure(state="disabled")

    def _populate_fixtures(self):
        self.fixtures_text.configure(state="normal")
        self.fixtures_text.delete(1.0, tk.END)
        
        fixtures = "CALENDARIO\n\n"
        
        # Trova tutte le partite della squadra
        remaining_matches = []
        for round_idx, round_matches in enumerate(self.schedule):
            for match in round_matches:
                if (match.home == self.team or match.away == self.team) and not match.played:
                    is_home = match.home == self.team
                    opponent = match.away if is_home else match.home
                    location = "Casa" if is_home else "Trasferta"
                    remaining_matches.append((round_idx + 1, opponent, location))
        
        for giornata, opponent, location in remaining_matches:
            fixtures += f"Giornata {giornata}: vs {opponent.name} ({location})\n"

        self.fixtures_text.insert(1.0, fixtures)
        self.fixtures_text.configure(state="disabled")

class SetupFrame(ttk.Frame):
    def __init__(self, master, on_create_league):
        super().__init__(master)
        self.on_create_league = on_create_league

        self.num_teams_var = tk.IntVar(value=20)
        self.double_round_var = tk.BooleanVar(value=True)

        self.name_vars = []
        self.rating_vars = []

        self._build_ui()

    def _build_ui(self):
        # Configura griglia principale (25% - 75%)
        self.columnconfigure(0, weight=1, uniform="cols")
        self.columnconfigure(1, weight=3, uniform="cols")

        # ==== Colonna sinistra (configurazione) ====
        config_frame = ttk.LabelFrame(self, text="Configurazione")
        config_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(config_frame, text="Numero squadre:").grid(row=0, column=0, sticky="w", pady=4)

        # Spinbox con soli numeri pari
        self.num_spinbox = ttk.Spinbox(
            config_frame,
            from_=8,
            to=24,
            increment=2,
            textvariable=self.num_teams_var,
            width=5
        )
        self.num_spinbox.grid(row=0, column=1, sticky="w", pady=4)

        # Toggle andata e ritorno
        ttk.Checkbutton(config_frame, text="Andata e ritorno", variable=self.double_round_var).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=6
        )

        # Frame pulsanti sotto al toggle
        btn_frame = ttk.Frame(config_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=6)

        ttk.Button(btn_frame, text="Conferma", command=self._confirm_teams).grid(row=0, column=0, padx=(0,5))
        ttk.Button(btn_frame, text="Carica da file", command=self._load_from_file).grid(row=0, column=1)

        # ==== Colonna destra (squadre) ====
        self.teams_frame = ttk.Frame(self)
        self.teams_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.teams_frame.columnconfigure(0, weight=3)
        self.teams_frame.columnconfigure(1, weight=1)

    def _confirm_teams(self):
        n = int(self.num_teams_var.get())
        # protezione: assicurati che sia pari
        if n % 2 != 0:
            messagebox.showerror("Errore", "Il numero di squadre deve essere pari.")
            return
        self._show_team_entries(n)

    def _show_team_entries(self, n):
        # pulisci frame squadre
        for widget in self.teams_frame.winfo_children():
            widget.destroy()

        self.name_vars.clear()
        self.rating_vars.clear()

        # Genera righe squadre
        for i in range(n):
            nv = tk.StringVar(value=f"Squadra {i+1}")
            rv = tk.StringVar(value=str(60 + (i % 20)))
            self.name_vars.append(nv)
            self.rating_vars.append(rv)

            ttk.Entry(self.teams_frame, textvariable=nv, width=25).grid(row=i, column=0, padx=4, pady=2, sticky="we")
            ttk.Entry(self.teams_frame, textvariable=rv, width=8).grid(row=i, column=1, padx=4, pady=2, sticky="w")

        # Pulsante Crea Campionato sotto le righe
        ttk.Button(self.teams_frame, text="Crea Campionato", command=self._create).grid(
            row=n, column=0, pady=12, sticky="we"
            )


    def _load_from_file(self):
        # import locali per evitare dipendenze globali mancanti
        from tkinter import filedialog
        import csv

        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Text files", "*.txt")])
        if not filepath:
            return

        try:
            # leggi un campione per sniffing del delimitatore, gestisci BOM con utf-8-sig
            with open(filepath, "r", encoding="utf-8-sig", newline='') as f:
                sample = f.read(2048)
                f.seek(0)
                try:
                    dialect = csv.Sniffer().sniff(sample, delimiters=",;")
                    reader = csv.reader(f, dialect)
                except Exception:
                    f.seek(0)
                    reader = csv.reader(f)

                # ignora header (se presente)
                # Se il file ha header come "Nome,Rating" la next salta quella riga
                rows = list(reader)

            if not rows:
                messagebox.showerror("Errore", "File vuoto o non leggibile.")
                return

            # Se la prima riga sembra header (contiene 'nome' o 'rating' testo), scartala
            first = rows[0]
            if any(cell.strip().lower() in ("nome", "name", "rating", "valore") for cell in first):
                rows = rows[1:]

            # filtra righe vuote
            parsed = [r for r in rows if r and any(c.strip() for c in r)]
            if not parsed:
                messagebox.showerror("Errore", "Nessuna riga squadra valida trovata nel file.")
                return

            n = len(parsed)
            # coerenza: richiedi numero pari
            if n % 2 != 0:
                messagebox.showerror("Errore", f"Il file contiene {n} squadre (numero dispari). Il campionato richiede un numero pari di squadre.")
                return

            # aggiorna numero squadre e mostra righe
            self.num_teams_var.set(n)
            self._show_team_entries(n)

            # popola le entry con i valori del file (prende le prime 2 colonne)
            for i, row in enumerate(parsed):
                name = row[0].strip()
                rating_txt = row[1].strip() if len(row) > 1 else ""
                try:
                    rating = int(rating_txt)
                except Exception:
                    rating = 60
                # safety: controlla che name_vars esista per indice i
                if i < len(self.name_vars):
                    self.name_vars[i].set(name)
                    self.rating_vars[i].set(str(rating))

            # forza aggiornamento UI
            self.update_idletasks()

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile leggere il file:\n{e}")

    def _create(self):
        teams = []
        try:
            for nv, rv in zip(self.name_vars, self.rating_vars):
                name = nv.get().strip()
                rating = int(rv.get())
                rating = max(1, min(99, rating))
                if not name:
                    raise ValueError("Nome squadra vuoto")
                teams.append(Team(name=name, rating=rating))
        except Exception as e:
            messagebox.showerror("Errore", f"Dati squadre non validi: {e}")
            return

        double_round = self.double_round_var.get()
        self.on_create_league(teams, double_round)

class LeagueFrame(ttk.Frame):
    def __init__(self, master, teams: List[Team], double_round: bool = True, on_show_team_detail=None):
        super().__init__(master)
        self.teams = teams
        self.on_show_team_detail = on_show_team_detail
        if double_round:
            self.schedule = generate_double_round_robin(self.teams)
        else:
            self.schedule = generate_single_round_robin(self.teams)
        self.current_round = 0
        self._build()
        self._refresh_all()

    # ---------- UI ----------
    def _build(self):
        # Header con navigazione giornate
        header = ttk.Frame(self)
        header.pack(fill="x", pady=6)
        self.round_label = ttk.Label(header, text="Giornata 1", font=("Segoe UI", 14, "bold"))
        self.round_label.pack(side="left", padx=8)

        ttk.Button(header, text="⟵ Giornata prec.", command=self._prev_round).pack(side="left", padx=4)
        ttk.Button(header, text="Giornata succ. ⟶", command=self._next_round).pack(side="left", padx=4)
        ttk.Button(header, text="Simula partita selezionata", command=self._simulate_selected).pack(side="right", padx=4)
        ttk.Button(header, text="Simula giornata", command=self._simulate_round).pack(side="right", padx=4)
        ttk.Button(header, text="Simula tutto", command=self._simulate_all).pack(side="right", padx=4)

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        # Colonna sinistra: calendario giornata
        left = ttk.Frame(body)
        left.pack(side="left", fill="both", expand=True, padx=(8, 4))
        ttk.Label(left, text="Partite della giornata").pack(anchor="w")

        self.matches_tv = ttk.Treeview(left, columns=("Casa", "Ris", "Trasferta", "Stato"), show="headings", selectmode="browse")
        for col, w in zip(("Casa", "Ris", "Trasferta", "Stato"), (160, 80, 160, 100)):
            self.matches_tv.heading(col, text=col)
            self.matches_tv.column(col, width=w, anchor="center")
        self.matches_tv.pack(fill="both", expand=True, pady=4)

        # Colonna destra: classifica
        right = ttk.Frame(body)
        right.pack(side="right", fill="both", expand=True, padx=(4, 8))
        ttk.Label(right, text="Classifica").pack(anchor="w")

        self.table_tv = ttk.Treeview(
            right,
            columns=("Pos", "Squadra", "Pts", "PG", "V", "N", "P", "GF", "GA", "DR", "Rating", "team_obj"),
            show="headings",
            selectmode="browse",
            displaycolumns=("Pos", "Squadra", "Pts", "PG", "V", "N", "P", "GF", "GA", "DR", "Rating"),  # hides 'team_obj'
        )

        widths = (50, 140, 50, 40, 40, 40, 40, 50, 50, 50, 60)
        headers = ("Pos", "Squadra", "Pts", "PG", "V", "N", "P", "GF", "GA", "DR", "Rating")

        for col, w in zip(headers, widths):
            self.table_tv.heading(col, text=col)
            anchor = "w" if col == "Squadra" else "center"
            self.table_tv.column(col, width=w, anchor=anchor)
        self.table_tv.pack(fill="both", expand=True, pady=4)
        # Aggiungi evento doppio click per aprire dettaglio squadra
        self.table_tv.bind("<Double-1>", self._on_team_double_click)

    # ---------- Logica UI ----------
    def _refresh_all(self):
        self._refresh_round_label()
        self._populate_matches()
        self._populate_table()

    def _refresh_round_label(self):
        tot = len(self.schedule)
        self.round_label.configure(text=f"Giornata {self.current_round + 1} / {tot}")

    def _populate_matches(self):
        self.matches_tv.delete(*self.matches_tv.get_children())
        giornata = self.schedule[self.current_round]
        for idx, m in enumerate(giornata):
            stato = "Giocata" if m.played else "Da giocare"
            ris = f"{m.goals_home}-{m.goals_away}" if m.played else "-"
            self.matches_tv.insert("", "end", iid=str(idx), values=(m.home.name, ris, m.away.name, stato))

    def _populate_table(self):
        self.table_tv.delete(*self.table_tv.get_children())
        sorted_teams = standings(self.teams)
        for pos, t in enumerate(sorted_teams, start=1):
            # Memorizza la squadra nell'item per il click
            item_id = self.table_tv.insert(
                "",
                "end",
                values=(pos, t.name, t.points, t.played, t.wins, t.draws, t.losses, t.gf, t.ga, t.gd, t.rating),
            )
            # Associa la squadra all'ID dell'item
            self.table_tv.set(item_id, "team_obj", t)

    def _on_team_double_click(self, event):
        """Gestisce il doppio click su una squadra nella classifica."""
        selection = self.table_tv.selection()
        if not selection or not self.on_show_team_detail:
            return
        
        item_id = selection[0]
        # Trova la squadra dall'indice nella classifica
        sorted_teams = standings(self.teams)
        try:
            # L'item_id corrisponde alla posizione nella classifica (partendo da 0)
            team_index = int(item_id.replace("I", ""), 16) - 1  # Tkinter usa hex per gli ID
            # Metodo più robusto: cerca per nome
            team_name = self.table_tv.item(item_id)["values"][1]  # Nome è la colonna 1
            selected_team = next(t for t in self.teams if t.name == team_name)
            self.on_show_team_detail(selected_team)
        except (ValueError, IndexError, StopIteration):
            pass

    def _prev_round(self):
        if self.current_round > 0:
            self.current_round -= 1
            self._refresh_all()

    def _next_round(self):
        if self.current_round < len(self.schedule) - 1:
            self.current_round += 1
            self._refresh_all()

    def _simulate_selected(self):
        sel = self.matches_tv.selection()
        if not sel:
            messagebox.showinfo("Info", "Seleziona una partita dalla lista.")
            return
        idx = int(sel[0])
        match = self.schedule[self.current_round][idx]
        if match.played:
            messagebox.showinfo("Info", "Questa partita è già stata simulata.")
            return
        simulate_match(match)
        self._populate_matches()
        self._populate_table()

        # Seleziona automaticamente la prossima partita non giocata
        giornata = self.schedule[self.current_round]
        for i, m in enumerate(giornata):
            if not m.played:
                self.matches_tv.selection_set(str(i))
                self.matches_tv.see(str(i))
                break

    def _simulate_round(self):
        tot_rounds = len(self.schedule)
        
        # Trova la prossima giornata con partite da giocare
        while self.current_round < tot_rounds:
            giornata = self.schedule[self.current_round]
            to_play = [m for m in giornata if not m.played]
            if not to_play:
                self.current_round += 1
                continue
            # Simula tutte le partite della giornata corrente
            for m in to_play:
                simulate_match(m)
            self._refresh_all()  # aggiorna calendario + classifica

            # Dopo aver simulato, spostati automaticamente alla prossima giornata da giocare
            next_round = self.current_round + 1
            while next_round < tot_rounds and all(m.played for m in self.schedule[next_round]):
                next_round += 1
            if next_round < tot_rounds:
                self.current_round = next_round
            else:
                # Se non ci sono più giornate da giocare, resta sull'ultima
                self.current_round = tot_rounds - 1
            self._refresh_all()
            break  # Simulata una giornata, esci


    def _simulate_all(self):
        for giornata in self.schedule:
            for m in giornata:
                if not m.played:
                    simulate_match(m)
        self._refresh_all()
        messagebox.showinfo("Fine", "Campionato simulato completamente!")

# -------------------------------
# App principale
# -------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulatore Campionato di Calcio")
        self.geometry("1000x640")
        self.current_teams = None
        self.current_double_round = True
        try:
            self.iconbitmap(default="")  # ignorato su molte piattaforme, placeholder
        except Exception:
            pass
        self._show_setup()

    def _show_setup(self):
        for w in self.winfo_children():
            w.destroy()
        SetupFrame(self, self._create_league).pack(fill="both", expand=True, padx=8, pady=8)

    def _create_league(self, teams: List[Team], double_round: bool):
        self.current_teams = teams
        self.current_double_round = double_round
        for t in teams:
            t.reset_stats()
        for w in self.winfo_children():
            w.destroy()
        LeagueFrame(
            self, 
            teams, 
            double_round=double_round, 
            on_show_team_detail=self._show_team_detail
        ).pack(fill="both", expand=True)

    def _show_team_detail(self, team: Team):
        """Mostra la schermata dettaglio per una squadra specifica."""
        for w in self.winfo_children():
            w.destroy()
        
        # Ricostruisci il calendario per passarlo al dettaglio
        if self.current_double_round:
            schedule = generate_double_round_robin(self.current_teams)
        else:
            schedule = generate_single_round_robin(self.current_teams)
            
        TeamDetailFrame(
            self, 
            team, 
            schedule, 
            on_back=self._return_to_league
        ).pack(fill="both", expand=True)

    def _return_to_league(self):
        """Torna alla schermata principale del campionato."""
        for w in self.winfo_children():
            w.destroy()
        LeagueFrame(
            self, 
            self.current_teams, 
            double_round=self.current_double_round, 
            on_show_team_detail=self._show_team_detail
        ).pack(fill="both", expand=True)

if __name__ == "__main__":
    random.seed()  # inizializza da sistema
    App().mainloop()
