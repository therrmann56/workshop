# Distributed Order System - Simulation

Dieses Projekt simuliert ein verteiltes E-Commerce-Order-System mit Kafka und MariaDB.  
Es besteht aus modularen Services, die Events erzeugen, konsumieren und transformieren.

---

## Module im Überblick

### 1. **Checkout Service**
- Simuliert Nutzer, die den Checkout durchlaufen
- Status-Übergänge: `created` -> `AddressSubmitted` -> `PaymentMethodSubmitted` -> `CheckoutSubmitted`
- Nur ca. **7 % der Checkouts** führen zum Status `CheckoutSubmitted`
- Events werden im Kafka-Topic `checkout` veröffentlicht

### 2. **Order Service**
- Konsumiert `CheckoutSubmitted` aus dem `checkout`-Topic
- Erstellt `Order`-Objekte mit Status `NEW` -> `MERCHANT_ACCEPTED` -> `SHIPPED` -> `COMPLETED`
- Simuliert auch `DISPUTED` und `CANCELLED`
- Veröffentlicht Events im Kafka-Topic `order`

### 3. **Fulfillment Service**
- Konsumiert Orders mit Status `MERCHANT_ACCEPTED` oder `SHIPPED`
- Erstellt `Fulfillment`-Einträge in der Datenbank
- Status: `SHIPPED` -> `DELIVERED`
- Veröffentlicht Events im Kafka-Topic `fulfillment`

### 4. **Analytics Service**
- Konsumiert **alle drei Topics**: `checkout`, `order`, `fulfillment` mit eigener Consumer-Group.
- Speichert jede Nachricht **append-only** in einer strukturierten MariaDB
- Ziel: Grundlage für **KPI-Analysen**, Dashboards und Reports

---

## Technologien

| Komponente     | Technologie       |
|----------------|-------------------|
| Message Queue  | Apache Kafka      |
| Datenbank      | MariaDB (IPv6)    |
| Scripts        | Python 3 + SQLAlchemy / kafka-python / confluent-kafka |
| Container      | Docker / Docker Compose |
| Speicher       | Strukturierte Datenbanktabellen (2. NF) |

---

## Zusammenarbeit ist notwendig!

> ### **Ohne Kommunikation - kein Erfolg!**
>
> Dieses Projekt lebt von Zusammenarbeit:
>
> - Stimmt **Schnittstellen, Schemata und Objektstrukturen** miteinander ab.
> - Sprecht euch ab, **wie Statuswechsel und Events simuliert werden**.
> - Teilt eure **Implementierungsideen**, um doppelte Arbeit zu vermeiden.
> - Startet im Team nicht alle mit der selben Aufgabe: **teilt euch im Team und Gruppe sinnvoll auf!**
>
> **Wenn jeder für sich allein arbeitet, ist es extrem unwahrscheinlich, dass das System als Ganzes funktioniert.**  
> Nur durch Austausch entsteht ein funktionierendes System.

---

## Ziele & Lerneffekte

- **Cross-Service-Kommunikation im verteilten Team**
- Spaß in der Gruppe, Kennenlernen neuer Kollegen
- Verständnis für Event-basierte Systemarchitekturen
- Arbeiten mit Kafka, Topics & Consumer Groups
- Modellierung und Speicherung von Domain-Objekten
- Ableitung von KPIs aus Event-Streams

---

## Best Practices

- Nutzt **saubere JSON-Objekte** mit festen Strukturen
- Achtet auf **idempotente Statusübergänge**
- Entwickelt **nicht am Topic vorbei** - lest & schreibt Events wirklich

>  Nur der erzeugende Service darf eine Entität (z. B. Order, Fulfillment, Checkout) im zugehörigen Topic veröffentlichen. Andere dürfen sie nur lesen und lokal verarbeiten nicht publizieren oder speichern.

---

## Nächste Schritte

1. Stellt sicher, dass Kafka und MariaDB laufen
2. Startet eure Consumer & Producer
3. Beginnt mit einfachen Events und testet Statusübergänge
4. Dokumentiert eure Schnittstellen
5. Redet miteinander!

---

> Wenn du Unterstützung brauchst: **Fragen, Fragen und nochmals Fragen und zwar deine Kollegen**

---

# SETUP

## ? Windows: WSL 2 + Ubuntu installieren

1. **WSL 2 aktivieren:**
   ```powershell
   wsl --install

2. `wsl --install Ubuntu-24.04`

3. Neustart durchführen und Ubuntu einrichten


## Docker unter Ubuntu in WSL 2 installieren

1. Docker installieren 
```
sudo apt update
sudo apt install -y docker.io
```

2. Docker IPv6 aktivieren
- `sudo nano /etc/docker/daemon.json`

Dann Inhalt einfügen

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "fd00:dead:beef::/64"
}
```

3. Docker starten
```
sudo systemctl enable docker
sudo systemctl start docker
```

4. Docker ohne sudo nutzen
- `sudo usermod -aG docker $USER`
- danach einmal abmelden und neu anmelden
- exit <ENTER>
- auf powershell dann
- wsl -d Ubuntu-24.04
- im Linux-System `docker ps` sollte ohne sudo funktionieren

Docker Daemon neustarten
- `sudo systemctl restart docker`

## Git auf Linux-Host installieren
- `sudo apt-get install git`

## GIT-Repository
```
git clone https://github.com/therrmann56/workshop.git
```

## Python & Virtual Environments

1. install venv
- `sudo apt install python3-venv`

2. Pro App Einrichten
```
cd order  # oder checkout, fulfillment, analytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Docker Images laden und container bauen
Im Hauptverzeichnis <workshop> folgenden Befehl aufrufen:
- `sudo apt  install docker-compose`
- danach
- `docker-compose up -d`
Danach unbedingt die Container wieder stoppen und die restliche Konfiguration abschließen
- `docker-compose stop`


## IPv6-Routing für Kafka & MariaDB testen

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
- Das hier gezeigte Interface br-xxxxxx dient als Beispiel. Bitte mit dem eigenen aus dem 1. Schritt ersetzen
- `sudo ip -6 route add fd00:dead:cafe::/64 dev br-c010aaac3737`

3. Testen

```
ping6 fd00:dead:cafe::10  # Kafka
ping6 fd00:dead:cafe::100  # MariaDB
```

## **(Optional)** Falls Container trotz Route nicht erreichbar oder keine Route gesetzt werden konnte
1. Route kontrollieren mit:
   - `ip -6 route | grep cafe`
2. Falsche Route löschen
   - `sudo ip -6 route del fd00:dead:cafe::/64 dev <falsches-interface>`
3. Neue Route setzen
   - `sudo ip -6 route add fd00:dead:cafe::/64 dev <richtiges Interface br-xxxxxxxx>`
4. Testen der neuen Route
   ```
   ping6 fd00:dead:cafe::100 #MariaDB
   ping6 fd00:dead:cafe::10  #Kafka
   ```

## MariaDB Zugriff

Zugriff auf die DB vom Linux aus.

1. MySQL Client installieren

- `sudo apt install mariadb-client-core mariadb-client`

2. Mit IPv6 verbinden

- `mysql -h 'fd00:dead:cafe::100' -P 3306 -u user -p`

3. Tabellen prüfen
```
USE analytics;
SHOW TABLES;
DESC checkout;
```



## Zugriff vom Windows-Host aus (z.?B. DBeaver, MySQL Workbench)

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

# Happy Coding - Empfehlung Visual Studio Code mit Python und Docker Extension :)
Ihr könnt gezielt einzelne Services mit docker-compose im Hintergrund starten
- `docker-compose up -d kafka init-kafka`
- startet Kafka und initialisiert die Topics.
- Vergesst nicht eure venv zusetzen in den jeweiligen Applikations-Verzeichnissen.



