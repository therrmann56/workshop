# ?? Distributed Order System ? Workshop & Simulation

Dieses Projekt simuliert ein verteiltes E-Commerce-Order-System mit Kafka und MariaDB.  
Es besteht aus modularen Services, die Events erzeugen, konsumieren und transformieren ? realit�tsnah und skalierbar.

---

## ?? Module im �berblick

### 1. **Checkout Service**
- Simuliert Nutzer, die den Checkout durchlaufen
- Status-�berg�nge: `created` ? `AddressSubmitted` ? `PaymentMethodSubmitted` ? `CheckoutSubmitted`
- Nur ca. **7 % der Checkouts** f�hren zum Status `CheckoutSubmitted`
- Events werden im Kafka-Topic `checkout` ver�ffentlicht

### 2. **Order Service**
- Konsumiert `CheckoutSubmitted` aus dem `checkout`-Topic
- Erstellt `Order`-Objekte mit Status `NEW` ? `MERCHANT_ACCEPTED` ? `SHIPPED` ? `COMPLETED`
- Simuliert auch `DISPUTED` und `CANCELLED`
- Ver�ffentlicht Events im Kafka-Topic `order`

### 3. **Fulfillment Service**
- Konsumiert Orders mit Status `MERCHANT_ACCEPTED` oder `SHIPPED`
- Erstellt `Fulfillment`-Eintr�ge in der Datenbank
- Status: `SHIPPED` ? `DELIVERED`
- Ver�ffentlicht Events im Kafka-Topic `fulfillment`

### 4. **Analytics Service**
- Konsumiert **alle drei Topics**: `checkout`, `order`, `fulfillment`
- Speichert jede Nachricht **append-only** in einer strukturierten MariaDB
- Ziel: Grundlage f�r **KPI-Analysen**, Dashboards und Reports

---

## ??? Technologien

| Komponente     | Technologie       |
|----------------|-------------------|
| Message Queue  | Apache Kafka      |
| Datenbank      | MariaDB (IPv6)    |
| Scripts        | Python 3 + SQLAlchemy / kafka-python / confluent-kafka |
| Container      | Docker / Docker Compose |
| Speicher       | Strukturierte Datenbanktabellen (2. NF) |

---

## ?? Zusammenarbeit ist Pflicht!

> ### ?? **Ohne Kommunikation ? kein Erfolg!**
>
> Dieses Projekt lebt von Zusammenarbeit:
>
> - Stimmt **Schnittstellen, Schemata und Objektstrukturen** miteinander ab.
> - Sprecht euch ab, **wie Statuswechsel und Events simuliert werden**.
> - Teilt eure **Implementierungsideen**, um doppelte Arbeit zu vermeiden.
> - Startet im Team nicht alle mit der selben Aufgabe ? **teilt euch sinnvoll auf!**
>
> ? **Wenn jeder f�r sich allein arbeitet, ist es extrem unwahrscheinlich, dass das System als Ganzes funktioniert.**  
> Nur durch Austausch entsteht ein funktionierendes System.

---

## ?? Ziele & Lerneffekte

- **Cross-Service-Kommunikation im verteilten Team**
- Spa� in der Gruppe, Kennenlernen neuer Kollegen
- Verst�ndnis f�r Event-basierte Systemarchitekturen
- Arbeiten mit Kafka, Topics & Consumer Groups
- Modellierung und Speicherung von Domain-Objekten
- Ableitung von KPIs aus Event-Streams

---

## ? Best Practices

- Nutzt **saubere JSON-Objekte** mit festen Strukturen
- Achtet auf **idempotente Status�berg�nge**
- Entwickelt **nicht am Topic vorbei** ? lest & schreibt Events wirklich
- **Dokumentiert** eure Services & Statuswechsel

---

## ?? N�chste Schritte

1. Stellt sicher, dass Kafka und MariaDB laufen
2. Startet eure Consumer & Producer
3. Beginnt mit einfachen Events und testet Status�berg�nge
4. Dokumentiert eure Schnittstellen
5. Redet miteinander! ??

---

> Wenn du Unterst�tzung brauchst: **Fragen stellen ist kein Schw�chezeichen, sondern Teamkompetenz.**

---

# ?? SETUP

## ? Windows: WSL 2 + Ubuntu installieren

1. **WSL 2 aktivieren:**
   ```powershell
   wsl --install
   wsl --set-default-version 2

2. Ubuntu 22.04 �ber Microsoft Store installieren

3. Neustart durchf�hren und Ubuntu einrichten



## Docker unter Ubuntu in WSL 2 installieren

1. Docker installieren 
```
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
```
2. Docker ohne sudo nutzen
- `sudo usermod -aG docker $USER`
danach einmal abmelden und neu anmelden



## Docker IPv6 aktivieren
- `sudo nano /etc/docker/daemon.json`

Dann Inhalt einf�gen

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "fd00:dead:beef::/64"
}
```

Docker Daemon neustarten
- `sudo systemctl restart docker`



## Python & Virtual Environments

1. install venv
- `sudo apt install python3.10-venv`

2. Pro App Einrichten
```
cd order  # oder checkout, fulfillment, analytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```



## IPv6-Routing f�r Kafka & MariaDB testen

1. Docker-Netzwerk-Interface finden:

- `ip -6 addr show | grep -B2 "fd00:dead:cafe"`

Ergebnis
```
 ip -6 addr show | grep -B2 "fd00:dead:cafe"
       valid_lft forever preferred_lft forever
4: br-c010aaac3737: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 state DOWN
    inet6 fd00:dead:cafe::1/64 scope global nodad
```

2. Route setzen

- `sudo ip -6 route add fd00:dead:cafe::/64 dev br-c010aaac3737`

3. Testen

```
ping6 fd00:dead:cafe::10  # Kafka
ping6 fd00:dead:cafe::100  # MariaDB
```



## MariaDB Zugriff

1. MySQL Client installieren

- `sudo apt install mariadb-client-core-10.6`

2. Mit IPv6 verbinden

- `mysql -h 'fd00:dead:cafe::100' -P 3306 -u user -p`

3. Tabellen pr�fen
```
USE analytics;
SHOW TABLES;
DESC checkout;
```



## Zugriff von Windows aus (z.?B. DBeaver, MySQL Workbench)

1. IPv4-Adresse des WSL2-Netzwerks finden (Powershell, Windows-Terminal):

- `ip addr show eth0 | grep 'inet '`

2. Client einrichten mit den entsprechenden Daten
- HOST: WSL-IP
- User: user
- Password: userpw
- Port: 3306



## Encoding-Probleme mit Python-Skripten beheben
```
sudo apt install dos2unix
dos2unix path/to/script.sh
```



