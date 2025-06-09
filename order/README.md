# Order Service
# Order Modul

Das **Order Modul** filtert Nachrichten aus dem `checkout`-Topic des Kafka-Messaging-Systems nach Checkouts mit dem Status **`CheckoutSubmitted`**. Diese Checkout-Objekte werden in Order-Objekte konvertiert und mit dem Status **`NEW`** in der Datenbank gespeichert.

## Statusübergänge einer Order

Die Order durchläuft im Verlauf ihres Lebenszyklus mehrere Status:

- **`NEW`**  
  Das Checkout-Objekt wurde erfolgreich in ein Order-Objekt konvertiert.  
  Die Order wurde im `order`-Topic veröffentlicht.

- **`NEW ? MERCHANT_ACCEPTED`**  
  Ein Händler hat über die API bestätigt, dass er die Order bearbeitet.  
  Die Order erhält den Status `MERCHANT_ACCEPTED` und wird erneut im `order`-Topic publiziert.

- **`MERCHANT_ACCEPTED ? SHIPPED`**  
  Der Order-Service empfängt ein Fulfillment-Objekt aus dem `fulfillment`-Topic.  
  Dieses enthält die entsprechende `ORDER_ID` und den Status `SHIPPED`.

- **`SHIPPED ? COMPLETED`**  
  Die Order gilt als abgeschlossen, wenn ein weiteres Fulfillment-Objekt mit der `ORDER_ID` und dem Status `DELIVERED` empfangen wird.

- **`NEW ? DISPUTED`**  
  Der Händler meldet über die API, dass die Order nicht angenommen werden kann oder Daten fehlen.  
  Die Order erhält den Status `DISPUTED` und wird im `order`-Topic veröffentlicht.

- **`DISPUTED ? CANCELLED`**  
  Der Konflikt konnte nicht gelöst werden.  
  Die Order erhält den finalen Status `CANCELLED`.  
  Keine weiteren Aktionen sind möglich.

## Wichtige Hinweise zur Verarbeitung

- **5?%** aller Orders werden vom Händler **nicht akzeptiert** und landen im Status `DISPUTED`. Diese Orders werden anschließend in den Status `CANCELLED` überführt.
- Eine Order muss **alle Statusübergänge durchlaufen**, um entweder in den Status `COMPLETED` oder `CANCELLED` zu gelangen.
- Der Startstatus jeder Order ist **`NEW`**.
- **Achtung bei der Nutzung des `order`-Topics:**  
  Vermeide **Endlos-Loops**, indem du den Statuswechsel klar steuerst.
- Der **Order-Service** ist die **Single Source of Truth (SSOT)**  
  und **einzige Komponente**, die berechtigt ist, Nachrichten im `order`-Topic zu veröffentlichen.
- Fun-Fact es ist möglich den Order-Topic als Persistence-Layer zu benutzen, um die Anforderungen umzusetzen (nicht zwingend)
