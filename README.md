Readme languages: ENG / ITA

## ENG

### CLI Commands

```bash
# Searches for users' birthdays (0-7 days), and notifies accordingly:
# - Notifies an happy birthday to today birthday users
# - Notifies a reminder to every not-birthday users if there's a birthday in 0,
#   1, or 7 days. It also sends an email if there's a birthday in 0 days (today)
docker compose exec taste_purchase_web python manage.py users_birthday_check
```

### Cron jobs to setup

```bash
# System should run this command everyday at 00:01 AM
docker compose exec taste_purchase_web python manage.py users_birthday_check
```

## ITA

### Comandi CLI

```bash
# Cerca compleanni (0-7 giorni) ed invia notifiche:
# - Notifica auguri di buon compleanno ai festeggiati di oggi
# - Notifica un reminder a tutti i non festeggiati se c'e' un compleanno in 0,
#   1, o 7 giorni. Invia anche una email se c'e' un compleanno in 0 giorni (oggi)
docker compose exec taste_purchase_web python manage.py users_birthday_check
```

### Cron job da impostare

```bash
# Il sistema dovrebbe eseguire questo comando ogni giorno alle ore 00:01
docker compose exec taste_purchase_web python manage.py users_birthday_check
```
