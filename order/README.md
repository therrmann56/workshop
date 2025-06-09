# Order Service
# Order Modul

Das **Order Modul** filtert Nachrichten aus dem `checkout`-Topic des Kafka-Messaging-Systems nach Checkouts mit dem Status **`CheckoutSubmitted`**. Diese Checkout-Objekte werden in Order-Objekte konvertiert und mit dem Status **`NEW`** in der Datenbank gespeichert.

## Status�berg�nge einer Order

Die Order durchl�uft im Verlauf ihres Lebenszyklus mehrere Status:

- **`NEW`**  
  Das Checkout-Objekt wurde erfolgreich in ein Order-Objekt konvertiert.  
  Die Order wurde im `order`-Topic ver�ffentlicht.

- **`NEW ? MERCHANT_ACCEPTED`**  
  Ein H�ndler hat �ber die API best�tigt, dass er die Order bearbeitet.  
  Die Order erh�lt den Status `MERCHANT_ACCEPTED` und wird erneut im `order`-Topic publiziert.

- **`MERCHANT_ACCEPTED ? SHIPPED`**  
  Der Order-Service empf�ngt ein Fulfillment-Objekt aus dem `fulfillment`-Topic.  
  Dieses enth�lt die entsprechende `ORDER_ID` und den Status `SHIPPED`.

- **`SHIPPED ? COMPLETED`**  
  Die Order gilt als abgeschlossen, wenn ein weiteres Fulfillment-Objekt mit der `ORDER_ID` und dem Status `DELIVERED` empfangen wird.

- **`NEW ? DISPUTED`**  
  Der H�ndler meldet �ber die API, dass die Order nicht angenommen werden kann oder Daten fehlen.  
  Die Order erh�lt den Status `DISPUTED` und wird im `order`-Topic ver�ffentlicht.

- **`DISPUTED ? CANCELLED`**  
  Der Konflikt konnte nicht gel�st werden.  
  Die Order erh�lt den finalen Status `CANCELLED`.  
  Keine weiteren Aktionen sind m�glich.

## Wichtige Hinweise zur Verarbeitung

- **5?%** aller Orders werden vom H�ndler **nicht akzeptiert** und landen im Status `DISPUTED`. Diese Orders werden anschlie�end in den Status `CANCELLED` �berf�hrt.
- Eine Order muss **alle Status�berg�nge durchlaufen**, um entweder in den Status `COMPLETED` oder `CANCELLED` zu gelangen.
- Der Startstatus jeder Order ist **`NEW`**.
- **Achtung bei der Nutzung des `order`-Topics:**  
  Vermeide **Endlos-Loops**, indem du den Statuswechsel klar steuerst.
- Der **Order-Service** ist die **Single Source of Truth (SSOT)**  
  und **einzige Komponente**, die berechtigt ist, Nachrichten im `order`-Topic zu ver�ffentlichen.
- Fun-Fact es ist m�glich den Order-Topic als Persistence-Layer zu benutzen, um die Anforderungen umzusetzen (nicht zwingend)
