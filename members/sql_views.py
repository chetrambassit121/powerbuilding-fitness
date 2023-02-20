from django.db import connection
from django.db.models import Q
from django.shortcuts import render

from .models import User, UserProfile



def users_list_(request):  
    users = User.objects.all()  
    print(users)  
    print(users.query)  
    print(
        connection.queries
    )  
    return render(
        request, "registration/users_list.html", {"users": users}
    ) 


def users_list_(request):
    users = User.objects.filter(first_name__startswith="chetram") | User.objects.filter(
        first_name__startswith="john"
    )
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.filter(
        ~Q(first_name__startswith="chetram") | Q(first_name__startswith="john")
    )                                               
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.filter(city_id=1) & User.objects.filter(state_id=1)
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.filter(
        Q(first_name__startswith="chetram") & Q(last_name__startswith="bassit")
    )
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.exclude(
        Q(first_name__startswith="chetram") & Q(last_name__startswith="bassit")
    )
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = (
        User.objects.all()
        .values_list("first_name")
        .union(UserProfile.objects.all().values_list("first_name"))
    )
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = (
        User.objects.all()
        .values("first_name")
        .union(UserProfile.objects.all().values("first_name"))
    )
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.exclude(first_name__startswith="chetram")
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.exclude(
        first_name__startswith="chetram"
    ) & User.objects.exclude(last_name__startswith="doe")
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.exclude(age__gt=19)
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.exclude(~Q(age__gt=19))
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.exclude(~Q(age__gt=19) & ~Q(first_name__Startswith="chetram"))
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.filter(city_id=1).only("first_name")
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    sql = "SELECT * FROM members_user"
    users = User.objects.raw(sql)  
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.raw("SELECT * FROM members_user WHERE last_name='doe'")
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    users = User.objects.all()
    for u in User.objects.raw("SELECT * FROM members_user"):
        print(u)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM members_user")
    users = cursor.fetchone()
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def users_list_(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM members_user")
    users = cursor.fetchall()
    print(users)
    print(connection.queries)
    return render(request, "registration/users_list.html", {"users": users})


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def users_list(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM members_user WHERE last_name='doe'")
    users = dictfetchall(cursor)
    print(users)
    print(connection.queries)

    return render(request, "registration/users_list.html", {"users": users})
