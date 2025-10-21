import random
import matplotlib.pyplot as plt

# CONFIGURAZIONE
saldo_iniziale = 20.00
puntata_base = 0.10
max_mani = 200  # quante mani vuoi simulare

# PROBABILITÀ (approssimate): Player: 44.6%, Banker: 45.9%, Tie: 9.5%
prob_player = 0.446
prob_tie = 0.095
prob_banker = 1 - prob_player - prob_tie

# VARIABILI
saldo = saldo_iniziale
puntata_attuale = puntata_base
vittorie = 0
sconfitte = 0
pareggi = 0
perdite_consecutive = 0
max_perdite_consecutive = 0
storico_saldo = [saldo]
storico_puntate = [puntata_attuale]

# FUNZIONE PER SIMULARE UN RISULTATO
def simula_baccara():
    r = random.random()
    if r < prob_player:
        return "giocatore"
    elif r < prob_player + prob_tie:
        return "pareggio"
    else:
        return "banco"

# SIMULAZIONE
mano = 0
while mano < max_mani and saldo >= puntata_attuale:
    mano += 1
    esito = simula_baccara()

    if esito == "giocatore":
        saldo += puntata_attuale
        vittorie += 1
        puntata_attuale = puntata_base
        perdite_consecutive = 0
    elif esito == "banco":
        saldo -= puntata_attuale
        sconfitte += 1
        perdite_consecutive += 1
        puntata_attuale *= 2
    elif esito == "pareggio":
        pareggi += 1
        # puntata non cambia

    max_perdite_consecutive = max(max_perdite_consecutive, perdite_consecutive)
    storico_saldo.append(saldo)
    storico_puntate.append(puntata_attuale)

    if saldo < puntata_attuale:
        print(f"👉 Fermato: saldo ({saldo:.2f}€) insufficiente per puntare {puntata_attuale:.2f}€")
        break

# RISULTATI
print("\n📈 Verifica raccolta dati:")
print(f"Punti raccolti: {len(storico_saldo)}")
print(f"Saldo iniziale: {storico_saldo[0]}")
print(f"Saldo finale: {storico_saldo[-1]}")
print(f"Ultimi 10 saldi: {storico_saldo[-10:]}")
print("\n📊 RISULTATI SIMULAZIONE:")
print(f"Mani giocate: {mano}")
print(f"Vittorie: {vittorie}")
print(f"Sconfitte: {sconfitte}")
print(f"Pareggi: {pareggi}")
print(f"Saldo finale: {saldo:.2f} €")
print(f"Max perdite consecutive: {max_perdite_consecutive}")
print(f"Puntata massima eseguita: {max(storico_puntate):.2f} €")
print(f"📈 Dati raccolti: {len(storico_saldo)} punti")
print("Ultimi 5 saldi:", storico_saldo[-5:])


# GRAFICO SALDO
plt.figure(figsize=(10, 5))
plt.plot(storico_saldo, label="Saldo (€)")
plt.title("Andamento del Saldo nel Tempo")
plt.xlabel("Numero di mani")
plt.ylabel("Saldo (€)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
