# eMenu-REST-API

Design and implementation of an independent eMenu service, serving as an online restaurant menu card.

## Assumptions for the project:

#### Private API:

1.REST API for menu management.
2.Ability to create multiple versions of menu cards with a unique name.
3.Each card can contain any number of dishes.
4.Each dish should be characterized by: name, description, price, preparation time, date of create, date of update, information whether the dish is vegetarian and image of the dish.
5.Each card is characterized by: name (unique), description, date of create, date of update.
6.The API must be protected against unauthorized access (after user authorization).

#### Public API:

1.Rest API for viewing non-empty menu tabs.
2.Ability to sort the list by name and number of dishes using GET parameters.
3.Filtering the list by name and the period of addition and recent updates.
4.Card detail presenting all data concerning the card and the dishes in the card.
