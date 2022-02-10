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
