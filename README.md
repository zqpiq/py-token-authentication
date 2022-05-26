# Token Authentication API

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start
- Download [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en)

### In this task you will add the functionality of token authentication

At this part of the task, we will do authorization by using tokens. The functionality of regular users will be limited so that they cannot add, delete or update other data on the sites, besides their orders.  Moreover, only authenticated users will be able to create an order.  Deletion will be prohibited even for the administrator, if only through the admin panel. That's because of  when we're deleting, for example, a genre, the other relationships from other tables won't deleted

1. Create serializers and views to support the following endpoints:
   * `POST api/register/` - You can create here a user
   * `POST api/login/` - You can get a token, if you write the correct data
   * `PATCH api/me/` - Information about user and possibility to update information about user


Example:
```python
HTTP 200 OK
Allow: GET, PUT, PATCH, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "username": "admin1",
    "email": "",
    "is_staff": true
}
```

2. By default, all endpoints in API must have the following action limitations depending on the user role:

 * Implement such custom permission class `IsAdminOrIfAuthenticatedReadOnly`.


3. Add `authentication_classes` & `permission_classes` for all view classes.


4. Make **only** such actions available for views:
   * `GenreViewSet` - list and create
   * `CinemaHallViewSet` - list and create
   * `ActorViewSet` - list and create 
   * `MovieViewSet` - list, create and retrieve
   * `MovieSessionViewSet` - list, retrieve, create, update, partial_update, delete
   * `OrderViewSet` - list and create


5. `OrderViewSet` - We should give the ability for authenticated users to create order