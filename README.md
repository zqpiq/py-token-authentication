# User Permissions API

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start
- Download [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en)

### In this task you will add the functionality of user permissions

1. Create serializers and views to support the following endpoints:
   * `POST api/register/` - You can create here a user
   * `POST api/login/` - You can get a token, if you write the correct data
   * `POST api/me/` - Information about user and possibility to update information about user


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

2. Create `cinema/permissions.py` with next API access:

 * Anon: None.
 * IsAuthenticated: list, retrieve.
 * IsAdmin: create, update, partial_update, destroy.

3. Add `authentication_classes` & `permission_classes` for all view classes.
4. Use mixins for `views.py` with next access:
   * `GenreViewSet` - list and create
   * `CinemaHallViewSet` - list and create
   * `ActorViewSet` - list and create 
   * `MovieViewSet` - list, create and retrieve
   * `MovieSessionViewSet` - without changes
   * `OrderViewSet` - list and create
5. `OrderViewSet` - implements `get_permissions`. This function allows to create an order.