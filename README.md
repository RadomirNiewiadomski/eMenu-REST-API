# eMenu-REST-API

Design and implementation of an independent eMenu service, serving as an online restaurant menu card.


## Assumptions for the project:

#### Private API:

1. REST API for menu management.
2. Ability to create multiple versions of menu cards with a unique name.
3. Each card can contain any number of dishes.
4. Each dish should be characterized by: name, description, price, preparation time, date of create, date of update, information whether the dish is vegetarian and image of the dish.
5. Each card is characterized by: name (unique), description, date of create, date of update.
6. The API must be protected against unauthorized access (after user authorization).

#### Public API:

1. Rest API for viewing non-empty menu tabs.
2. Ability to sort the list by name and number of dishes using GET parameters.
3. Filtering the list by name and the period of addition and recent updates.
4. Card detail presenting all data concerning the card and the dishes in the card.

#### Reporting:

1. A mechanism that will send an e-mail to all users of the application once a day at 10:00.
2. The e-mail contains information about dishes that were added or modified yesterday.

### Additional information:

1. The application was made according to the TDD methodology.
2. E-mail account used to send e-mail notifications updates: emenu.newdish.noreply@gmail.com
3. Project was integrated with Github Actions.

### Technologies:
- Python version: 3.9
- Django version: 4.0.1
- Django REST framework version: 3.12.4
- Docker version: 20.10.22
- Others: see "requirements.txt

## Setup instruction:
After installing docker and cloning git repository,
build backend locally by entering:

```
docker-compose up --build
```

API root:
```
http://localhost:8000/api/menu/
```

API documentation (swagger):
```
http://localhost:8000/api/docs/
```

Admin site:
```
http://localhost:8000/admin/
```

Default created admin account:
```
email: admin@menu.com
password: pass1234
```

## Created by:
Radomir Niewiadomski
