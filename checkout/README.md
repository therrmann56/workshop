# Aggregator Module

Dieses Modul ist Teil des verteilten Order-Systems und simuliert einen Checkout.

## Ablauf eines Checkouts

Ein Checkout besteht aus mehreren Status�berg�ngen:

1. `created` ? Kunde kommt auf die Adress-Seite.
2. `created` ? `AddressSubmitted`: Der Kunde hat seine Adressdaten eingegeben und das Formular abgeschickt.
3. `AddressSubmitted` ? `PaymentMethodSubmitted`: Der Kunde hat eine Zahlungsart ausgew�hlt.
4. `PaymentMethodSubmitted` ? `CheckoutSubmitted`: Der Kunde hat den Warenkorb best�tigt und bezahlt.

Nur Checkouts mit dem Status `CheckoutSubmitted` werden vom **Order-Modul** weiterverarbeitet.

## Konversionsrate

Das Checkout-Modul hat die Aufgabe, eine realistische Conversion-Rate abzubilden. Dabei gilt:

- **Nur 7?%** aller gestarteten Checkouts sollen in einen `CheckoutSubmitted`-Status �berf�hrt werden.
- Anders gesagt: Auf **100 gestartete Checkouts** folgen **7 erfolgreiche**, die zu einer Order konvertiert werden k�nnen.

## Empfehlungen zur Umsetzung

- **Checkout-Objekte generieren und zwischenspeichern**: Es wird empfohlen, Checkout-Daten persistent zu halten, um Statuswechsel abzubilden.
- Um vom Status `created` zu `CheckoutSubmitted` zu gelangen, m�ssen **alle Zwischenschritte** durchlaufen und jeweils im **`checkout`-Topic** ver�ffentlicht werden.
- Es ist g�ngige Praxis, dass der **CheckoutService** sein eigenes Topic konsumiert, um Status�berg�nge selbst durchzuf�hren.  
  **Achtung:** Dabei d�rfen **keine Endlos-Loops** entstehen!
- Verwende f�r den Checkout-Consumer eine **eigene Consumer-Group**, um Entkopplung und Wiederholbarkeit zu gew�hrleisten.
