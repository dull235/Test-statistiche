import streamlit as st
import random
import matplotlib.pyplot as plt
import time

# CONFIGURAZIONE
saldo_iniziale = 20.00
puntata_base = 0.10
max_mani = 200  # quante mani vuoi simulare

# PROBABILITÀ (approssimate): Player: 44.6%, Banker: 45.9%, Tie: 9.5%
prob_player = 0.446
prob_tie = 0.095
prob_banker = 1 - prob_player - prob_tie

st.title("🎰 Simulatore Bacarà - Strategia Martingala")
st.markdown("Simulazione automatizzata di puntate su 'giocatore'. Strategia: raddoppio dopo ogni perdita.")

if st.button("▶️ Avvia Simulazione"):

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
    log = ""

    output_box = st.empty()  # contenitore per output dinamico

    def simula_baccara():
        r = random.random()
        if r < prob_player:
            return "giocatore"
        elif r < prob_player + prob_tie:
            return "pareggio"
        else:
            return "banco"

    mano = 0
    while mano < max_mani and saldo >= puntata_attuale:
        mano += 1
        esito = simula_baccara()

        if esito == "giocatore":
            saldo += puntata_attuale
            vittorie += 1
            log += f"✅ Mano {mano}: Vinto! +{puntata_attuale:.2f}€ → saldo: {saldo:.2f}€\n"
            puntata_attuale = puntata_base
            perdite_consecutive = 0

        elif esito == "banco":
            saldo -= puntata_attuale
            sconfitte += 1
            log += f"❌ Mano {mano}: Perso! -{puntata_attuale:.2f}€ → saldo: {saldo:.2f}€\n"
            perdite_consecutive += 1
            puntata_attuale *= 2

        elif esito == "pareggio":
            pareggi += 1
            log += f"➖ Mano {mano}: Pareggio. Puntata rimane a {puntata_attuale:.2f}€\n"

        max_perdite_consecutive = max(max_perdite_consecutive, perdite_consecutive)
        storico_saldo.append(saldo)
        storico_puntate.append(puntata_attuale)

        output_box.code(log)  # aggiorna l'output live
        time.sleep(0.05)

        if saldo < puntata_attuale:
            log += f"\n🛑 Fermato: saldo ({saldo:.2f}€) insufficiente per puntare {puntata_attuale:.2f}€\n"
            output_box.code(log)
            break

    # RIEPILOGO FINALE
    st.success("✅ Simulazione completata!")

    riepilogo = f"""
📈 **Verifica raccolta dati:**
- Punti raccolti: {len(storico_saldo)}
- Saldo iniziale: {saldo_iniziale:.2f}
- Saldo finale: {saldo:.2f}
- Ultimi 10 saldi: {[round(s, 2) for s in storico_saldo[-10:]]}

📊 **RISULTATI SIMULAZIONE:**
- Mani giocate: {mano}
- Vittorie: {vittorie}
- Sconfitte: {sconfitte}
- Pareggi: {pareggi}
- Max perdite consecutive: {max_perdite_consecutive}
- Puntata massima eseguita: {max(storico_puntate):.2f} €
- Ultimi 5 saldi: {[round(s, 2) for s in storico_saldo[-5:]]}
"""
    st.code(riepilogo)

    # GRAFICO SALDO
    st.subheader("📉 Andamento del Saldo")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(storico_saldo, label="Saldo (€)", color='blue')
    ax.axhline(saldo_iniziale, color='gray', linestyle='--', label="Saldo iniziale")
    ax.set_xlabel("Numero di mani")
    ax.set_ylabel("Saldo (€)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


