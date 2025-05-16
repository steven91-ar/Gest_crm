from api.crm import get_all_users, User
from django.shortcuts import render, redirect


def index(request):
    users = get_all_users()
    return render(request, "contacts/index.html", {"users": users})

def add_contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")

        user = User(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address
        )
        user.save(validate_data=True)

    return redirect("index")

def delete_contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        user = User(first_name=first_name, last_name=last_name)
        user.delete()

    return redirect("index")