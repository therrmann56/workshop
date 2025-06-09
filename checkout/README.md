# Aggregator Module

Dieses Modul ist Teil des verteilten Order-Systems und simuliert einen Checkout.

## Ablauf eines Checkouts

Ein Checkout besteht aus mehreren Statusübergängen:

1. `created` ? Kunde kommt auf die Adress-Seite.
2. `created` ? `AddressSubmitted`: Der Kunde hat seine Adressdaten eingegeben und das Formular abgeschickt.
3. `AddressSubmitted` ? `PaymentMethodSubmitted`: Der Kunde hat eine Zahlungsart ausgewählt.
4. `PaymentMethodSubmitted` ? `CheckoutSubmitted`: Der Kunde hat den Warenkorb bestätigt und bezahlt.

Nur Checkouts mit dem Status `CheckoutSubmitted` werden vom **Order-Modul** weiterverarbeitet.

## Konversionsrate

Das Checkout-Modul hat die Aufgabe, eine realistische Conversion-Rate abzubilden. Dabei gilt:

- **Nur 7?%** aller gestarteten Checkouts sollen in einen `CheckoutSubmitted`-Status überführt werden.
- Anders gesagt: Auf **100 gestartete Checkouts** folgen **7 erfolgreiche**, die zu einer Order konvertiert werden können.

## Empfehlungen zur Umsetzung

- **Checkout-Objekte generieren und zwischenspeichern**: Es wird empfohlen, Checkout-Daten persistent zu halten, um Statuswechsel abzubilden.
- Um vom Status `created` zu `CheckoutSubmitted` zu gelangen, müssen **alle Zwischenschritte** durchlaufen und jeweils im **`checkout`-Topic** veröffentlicht werden.
- Es ist gängige Praxis, dass der **CheckoutService** sein eigenes Topic konsumiert, um Statusübergänge selbst durchzuführen.  
  **Achtung:** Dabei dürfen **keine Endlos-Loops** entstehen!
- Verwende für den Checkout-Consumer eine **eigene Consumer-Group**, um Entkopplung und Wiederholbarkeit zu gewährleisten.
