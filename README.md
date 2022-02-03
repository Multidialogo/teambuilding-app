Readme languages: ENG / ITA

## ENG

### Team building app
Teambuilding app is a platform thought to help working groups to create stronger relationships among members by means of various engaging and fun activities to do together.

Each activity can be managed and organized by the team, and an efficient notification system will remind to members when\where participate, and helps them within the organization.

#### Supported activities

##### Taste and purchase

Help team members to organize food tasting and eventual group purchase of propoused products.
Each team member can insert a productor and a product in the list, and create an event that will send a participiation invite to any team member.

Team members can place orders for particular products within any productor, and then orders will be grouped by productor and optimized to be placed in order to save expedition costs and time.

### Installation and usage

##### CLI Commands

```bash
# Searches for users' birthdays (0-7 days), and notifies accordingly:
# - Notifies an happy birthday to today birthday users
# - Notifies a reminder to every not-birthday users if there's a birthday in 0,
#   1, or 7 days. It also sends an email if there's a birthday in 0 days (today)
docker compose exec taste_purchase_web python manage.py users_birthday_check
```

#### Cron jobs to setup

```bash
# System should run this command everyday at 00:01 AM
docker compose exec taste_purchase_web python manage.py users_birthday_check
```

## ITA

### Applicazione per il team building
E'una piattaforma progettata per aiutare i gruppi di lavoro a costruire relazioni più forti tra i membri attraverso varie attività coinvolgenti e divertenti da fare insieme.

#### Attività supportate

##### Degustazione e acquisto

Aiuta i membri del team a organizzare degustazioni di cibo e l'eventuale acquisto di gruppo dei prodotti proposti.
Ogni membro del team può inserire un produttore e un prodotto nell'elenco e creare un evento che invierà un invito alla partecipazione a qualsiasi membro del team.

I membri del team possono effettuare ordini per prodotti particolari all'interno di qualsiasi produttore, quindi gli ordini verranno raggruppati per produttore e ottimizzati per essere inseriti al fine di risparmiare tempo e costi di spedizione.

### Installazione ed utilizzo

#### Comandi CLI

```bash
# Cerca compleanni (0-7 giorni) ed invia notifiche:
# - Notifica auguri di buon compleanno ai festeggiati di oggi
# - Notifica un reminder a tutti i non festeggiati se c'e' un compleanno in 0,
#   1, o 7 giorni. Invia anche una email se c'e' un compleanno in 0 giorni (oggi)
docker compose exec taste_purchase_web python manage.py users_birthday_check
```

#### Cron job da impostare

```bash
# Il sistema dovrebbe eseguire questo comando ogni giorno alle ore 00:01
docker compose exec taste_purchase_web python manage.py users_birthday_check
```
