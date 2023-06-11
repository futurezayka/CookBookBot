from django.http import HttpResponse
from test_task.context_procesors import user_is_authenticated
from .forms import RecipeForm
from .models import Recipe
from django.shortcuts import render, redirect
from .models import CurrentUser


def admin_panel(request):
    if not user_is_authenticated(request)['user_is_authenticated']:
        return redirect('/admin/login/')
    return render(request, 'custom_adminka/base.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin' and password == 'admin':
            request.session['is_admin_logged_in'] = True
            return redirect('/admin/')
        else:
            error_message = 'Пароль не правильний!'
            return render(request, 'custom_adminka/login.html', {'error_message': error_message})
    else:
        return render(request, 'custom_adminka/login.html')


def admin_logout(request):
    request.session['is_admin_logged_in'] = False
    return redirect('/admin/login/')


def user_list(request):
    if not user_is_authenticated(request)['user_is_authenticated']:
        return redirect('/admin/login/')
    users = CurrentUser.objects.all()
    return render(request, 'custom_adminka/user_list.html', {'users': users})


def recipe_list(request):
    if not user_is_authenticated(request)['user_is_authenticated']:
        return redirect('/admin/login/')
    recipes = Recipe.objects.all()
    return render(request, 'custom_adminka/recipe_list.html', {'recipes': recipes})


def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'custom_adminka/recipe_create.html', {'form': form})


def recipe_edit(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'custom_adminka/recipe_update.html', {'form': form, 'recipe': recipe})


def recipe_delete(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return HttpResponse(request, "Сталася помилка.")
