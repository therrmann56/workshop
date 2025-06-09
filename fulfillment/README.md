# Fulfillment Service

Der **Fulfillment Service** simuliert die Versand- bzw. Lieferbenachrichtigung durch den H�ndler.  
Er konsumiert Nachrichten aus dem **`order`-Topic** und filtert dabei nach Orders mit dem Status:

- `MERCHANT_ACCEPTED`
- `SHIPPED`

Alle anderen Orders werden vom Service **ignoriert**.

---

## Verarbeitungsschritte

### 1. Status: `MERCHANT_ACCEPTED`

Wird eine Order mit dem Status `MERCHANT_ACCEPTED` konsumiert:

- Der Fulfillment Service legt ein **Fulfillment-Objekt** in der Datenbank an.
- Das Objekt enth�lt folgende Felder:
  - `fulfillment_id`
  - `order_id`
  - `status` (initial: `SHIPPED`)
- Das Fulfillment-Objekt wird anschlie�end im **`fulfillment`-Topic** ver�ffentlicht.

---

### 2. Status: `SHIPPED`

Wird eine Order mit dem Status `SHIPPED` konsumiert:

- Der Service l�dt das zugeh�rige Fulfillment-Objekt aus der Datenbank.
- Der Status wird auf **`DELIVERED`** gesetzt.
- Das Fulfillment-Objekt wird gespeichert in der DB.
- Das aktualisierte Fulfillment-Objekt wird erneut im **`fulfillment`-Topic** ver�ffentlicht.

---

## Abschluss

Nach Ver�ffentlichung des Fulfillment-Objekts mit dem Status `DELIVERED` ist die Aufgabe des Fulfillment Services **abgeschlossen**.

