description = """
____
# Dynamic responses:
* if you are female with graphql you can send a query optoin called `query` where you define the json responses that you need.
#### Example: `/users/?query={id,username,location}` this will return
        ```
        {
        id: 1,
        username: "Bruce Willis",
        location: 3, 
        }
        ```
#### Example2: `/users/?query={id,username,location{country,city}}` this will return
        ```
        {
        id: 1,
        username: "Bruce Willis",
        location: {"country":"USA", city:"Manhattan"}, 
        }
        ```
# [lookups](https://docs.djangoproject.com/en/3.2/ref/models/lookups/)
### **LookUp**: are methods you can add to the query strings options preceded by `__`.
    - example: the lookup `contains` can be used like this.
    ```
    http://domain.com/users?first_name__contains=john
    ```

1. `gt` = greater than
2. `lt` = less than
3. `e` = or equal 'this can be used `__gte` which mean greater than or equal to' or you can say `lte` which mean less than or equal to  
4. `contains` = this can be used for list like '?groups__contains=providers' in which groups=['doctors','providers']
4. `in` = this check if one value is in many values just the opposite way of contains,
    - example
     1. `user__in=[1,2,3]`
     2. `user__username__in=AliJesusNikolina` you can also check if string is part of a bigger string  

5. `fieldname__sumfielname` = this used for subfields like you can say `column__name=anyname` to get all columns with subobjs that have name = anyname 
    - example
    ```
    {
    "column":{
        "name":"anyname","value":"anyvalue"
    }
    }
    ```
6. `name__icontains` i stand for "case insensitive"
6. `?search=anything` case insensitive search in all fiddles.
6. `ordering`
    - example1 `?ordering=-id` you will get the order object flipped
    - example2 `?ordering=name` you will get the objects order alphabetically A-Z by the filed called `name`
    - example3 `?ordering=-name` you will get the objects order alphabetically Z-A by the filed called `name`
6. you can add `latest=true`, `earliest=true` to get the latest or earliest object in case it have a field `date_created`
7. `abs_earliest` and `abs_latest`: 
    - example: `/users/?abs_latest=true&username__contains=c` if the latest created user's username doesnt have c  you wil get `[]`
    - example2: `/users/?latest=true&username__contains=c` this will get all users with username contains `c` then it will get the relative latest create user from them 
_____________________________________________________
- `"fieldname=F('modelname__fieldname')"`: this called F expression in django and I return dynamic value.
- example:
    if you have data like this
    ```
    {
    "field_value":"22"
    "column":{min:'22', max:'33'}
    },
    {
    "field_value":"300"
    "column":{min:'22', max:'33'}
    }
    ```
- `url/?field_value__lte=F('column__min')` this will return only 
    ```
    {
    "field_value":"22"
    "column":{min:'22', max:'33'}
    }
_____________________________________________________
# Dynamic import.
### To understand dynamic import let's imagine that we have a school website and each student (`User`) has parents (mother, father) A location (where they live). 
___
#### 1. Let's say you you want to assent a parent profile to a student profile but You don't know the id of the students and you need to use the name instead of the id.
To achieve that you can try
#### `client.put('users/1/', {'parent.name':'John'})`
#### instead of
#### `client.put('users/1/', {'parent':3})`
___
#### 2. Let's say the student with user id of `1` live with his/her parents. Hence, you need to following these steps to set the location of ther user with id 1
```javascript
// first get the parent id
data = client.get('/users/1/')
parent_id = data.parent
// then get the location of the parent
data = client.get(`/users/${parent_id}/`)
location_id = data.location

// finally set the location to the user 1
client.put(`/users/1/`, {'location':location_id})
```
___
### instead of all of these steps you can do the following. in this example the BE will get the parent object with id==`parent_id` then it will get the location of the parent object.
```javascript
data = client.get('/users/1/')
parent_id = data.parent
client.put(`/users/1/`, {'location__parent.id':parent_id})
```

___
### Or you can make it even shorter. here the BE will get the user_object with id==1 then  it will get `user_object.parent.location` and assign it to the locatoin of user with id 1  
```javascript
client.put(`/users/1/`, {'location__parent__user.id':1})
```
_____________________________       
# Final production steps
1. Change the environment variable `DEBUG` to `False`
"""
