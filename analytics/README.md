# Analytics Service des Order Systems

Dieses Modul ist Teil des **verteilten Order Systems**.  
Ziel des Analytics Service ist es, Daten aus den Topics `order`, `fulfillment` und `checkout` zu konsumieren und strukturiert in einer Datenbank abzulegen ? **additiv und unverändert**.

---

## Funktionen

- Der Service konsumiert **alle drei Kafka-Topics** (`order`, `fulfillment`, `checkout`).
- Es wird **eine eigene Consumer-Group** verwendet, damit andere Services weiterhin alle Nachrichten erhalten.
- Jede konsumierte Nachricht wird **als neue Zeile in der Datenbank gespeichert**.
- **Keine Felder werden aktualisiert** ? es erfolgt ausschließlich **append-only Logging**.

---

## Ziel

Das Ziel ist, möglichst viele **Rohdaten strukturiert** abzulegen, um Product Manager:innen eine fundierte Analyse der Performance von Checkout- und Order-Prozessen zu ermöglichen.

---

## Anforderungen

1. ? **Kafka-Consumer** für alle Topics mit **eigener Consumer-Group**  
2. ? **Tabellenstruktur**, die erlaubt, jedes Objekt als **eigene Zeile** in entsprechender Tabellen-Struktur zu speichern, wenn notwendig in tiefer Normalform.  
3. ? Felder müssen **filter- und gruppierbar** sein (keine Blobs oder Textfelder mit vollständigem JSON)

---

## KPI-Ausgabe

- Die **Product Owner** werden **KPIs definieren**, die Entwickler auf der Konsole ausgeben sollen.
- Das Zeitfenster für KPIs soll **10 Minuten oder kleiner** betragen, um die Datenmenge überschaubar zu halten.
- Typische KPIs könnten sein:
  - Anzahl an `CheckoutSubmitted` im Vergleich zu `created`
  - Ratio von `NEW` zu `COMPLETED` Orders
  - Prozentzahl an Bestellungen im Status 'DISPUTED'
  - Prozentuale Verteilung der Checkout-Status, Funnel-Abbildung, wo bouncen die meisten Kunden?

---

## Hinweis

Dieses Modul dient **nicht zur Verarbeitung** der Daten, sondern ausschließlich zur **strukturierten Speicherung und Analysevorbereitung**. Es ist die **Datenquelle für alle Auswertungen und Dashboards** rund um Checkout & Order. Eine Ausgabe auf der Konsole kann ein Dashboard simulieren. Es kann auch eine CSV exportiert werden, um in EXCEL ein Dashboard zu bauen.
