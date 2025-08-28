
riscrivi il setup frame, in generale direi un 25% di spazio a sinistra per la colonna dei parametri di configurazione e 75% per le righe delle squadre. Inoltre, il numero di squadre dovrebbe essere selezionato in modo che ci siano solo numeri pari, e il pulsante conferma dovrebbe essere messo vicino a quello di carica da file, sotto il toggle andata e ritorno

Alcune cose che vorrei aggiungere:
- Aggiungere uno o due colori per ogni squadra
- Possibilità di usare club elo ranking come valori delle squadre
- aggiungere parametri di simulazione
- aggiungere la schermata dettaglio squadra con calendario e forma
- In futuro, altre due cose da provare (ti dirò io quando farle): utilizzare magari streamlit invece di tktinker e aggiungere la possibilità di vedere la simulazione di una partita, ovvero quando clicco su inizia simulazione viene fatto vedere il cronometro e le varie azioni, ad esempio tiro squadra x - gol al minuto x, o altre azioni così

3. Club Elo Ranking

- Scaricare da clubelo.com i valori aggiornati.
- Inserire un’opzione per importare automaticamente i rating da lì (via web scraping o csv).
- In alternativa, permettere di incollare un file .csv/json con i valori.

5. Parametri di configurazione

- Numero di squadre (8–20).
- Tipo campionato: solo andata / andata+ritorno.
- Vantaggio casa (%) e media gol totali.

6. Parametri di simulazione

- Fattore “casualità” (più o meno imprevedibile).
- Variazione del vantaggio casa.
- Possibilità di scegliere distribuzione gol (Poisson, Gaussian, custom).

7. Schermata dettaglio squadra

- Tab “Dettaglio squadra” con:
- Info squadra (nome, colori, rating, record).
- Ultime 5 partite (forma: V/N/P).
- Calendario rimanente della squadra.
- Statistiche avanzate (GF media, GA media, % vittorie).

8. Futuro

- Streamlit: UI web più moderna e portabile.
- Simulazione in tempo reale: cronometro + eventi random (tiro, gol, fallo, cartellino).
    - Ogni evento estratto da una probabilità condizionata.
    - Timeline mostrata durante la partita.

- un'altra cosa che vorrei aggiungere è il fatto che i valori delle squadre possano cambiare nel corso del campionato in base ai risultati ottenuti, ovviamente questi valori dovranno cambiare non di troppo

🔹 Aggiornamento dinamico dei rating

Dopo ogni partita, i rating delle squadre devono cambiare leggermente:
    - Vittoria → aumenta un po’ il rating (più se contro avversario forte).
    - Sconfitta → diminuisce.
    - Pareggio → piccola variazione in base alla forza avversaria.

Questo ricorda molto il sistema Elo (come nel tennis o negli scacchi), quindi possiamo implementare una versione semplificata:
    - Calcoliamo la probabilità attesa di vittoria P_home e P_away in base ai rating.

Applichiamo:

    - new_rating = old_rating + K * (risultato - atteso)

Dove:

    - risultato = 1 se vittoria, 0.5 pareggio, 0 sconfitta.
    - atteso = probabilità attesa (da formula Elo).
    - K = fattore di variazione (es. 5 → variazioni lente, 30 → variazioni rapide).

In questo modo i valori non cambiano troppo, ma diventano dinamici in base ai risultati.
