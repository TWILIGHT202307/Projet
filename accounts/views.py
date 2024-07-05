from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render,redirect


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clinique:index")
    else:
        form = UserCreationForm()
        # Traitez les données soumises par l'utilisateur ici (vérification, redirection, etc.)

    return render(request,"accounts/register.html",{"form":form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect("clinique:index")
        else:
            messages.info(request,"Identifiant ou mot de passe incorrect")
    form = AuthenticationForm ()
    return render(request,"accounts/login.html",{"form":form})
            

def logout_user(request):
    logout(request)
    return redirect("clinique:index")

"""def register_page(request):
    form = CustomLoginForm()

    if request.method == 'POST':
        # Traitez les données soumises par l'utilisateur ici (validation, enregistrement, etc.)

    return render(request, 'register.html', {'form': form})"""

"""def register_user(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("CRUD_A:index")
    else:
        form=UserCreationForm()
        
    return render(request,"accounts/register.html",{"form":form})"""
        
    