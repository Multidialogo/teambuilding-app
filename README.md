# Team building app
* [Overview](#overview)
  * [Supported activities](#supported-activities)
* [Provisioning and containerized environment](#provisioning-and-containerized-environment)
* [Language/Framework](#language--framework)
* [Exposed CLI commands](#exposed-cli-commands)
* [Additional setup steps](#additional-setup-steps)
  * [Cron jobs](#cron-jobs)
* [Contributing](#contributing)

## Overview
![teambuilding-screen](static/teambuilding/docs/img/teambuilding-screen.png)

Teambuilding app is a platform thought to help working groups to create stronger relationships among members by means of various engaging and fun activities to do together.

Each activity can be managed and organized by the team, and an efficient notification system will remind to members when\where participate, and helps them within the organization.

### Supported activities
#### Taste and purchase
![tasting-screen](static/teambuilding/docs/img/tasting-screen.png)
Help team members to organize food tasting and eventual group purchase of propoused products.
Each team member can insert a producer and a product in the list, and create an event that will send a participiation invite to any team member.

Team members can place orders for particular products within any productor, and then orders will be grouped by productor and optimized to be placed in order to save expedition costs and time.

## Provisioning and containerized environment
Provisioning ([?](https://github.com/Multidialogo/teambuilding-app/wiki/Glossary#provisioning)) repository with Docker can be found [here](https://github.com/Multidialogo/teambuilding-app-provisioning).

## Language / Framework
Python [ [Docs](https://docs.python.org/3/) ] / Django [ [Docs](https://docs.djangoproject.com/en/4.0/) ]

## Exposed CLI Commands
```bash
# 'users_birthday_check'
# Searches for users' birthdays (0-7 days), and notifies accordingly:
# - Notifies an happy birthday to today birthday users
# - Notifies a reminder to every not-birthday users if there's a birthday in 0,
#   1, or 7 days. It also sends an email if there's a birthday in 0 days (today)
docker compose exec teambuilding_web python manage.py users_birthday_check
```

## Additional setup steps
There is a series of operations to execute in order to configure the project.

### Cron jobs
Is required to set a recurrent job to execute the following commands:

* Everyday at 00:01 AM the system should execute the *users_birthday_check* 
CLI command.

## Contributing
Contributing guidelines can be found [here](https://github.com/Multidialogo/teambuilding-app/blob/develop/docs/CONTRIBUTING.md).
