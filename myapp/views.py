from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm, UserForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # This will create the user in the database
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')  # Redirect to home after successful signup
    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page
    return render(request, 'login.html')

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page


def home_view(request):
    todos = Todo.objects.filter(user=request.user)  # Fetch todos for the logged-in user
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)  # Create a Todo object without saving it yet
            todo.user = request.user  # Associate the Todo with the logged-in user
            todo.save()  # Save the Todo to the database
            return redirect('home')  # Reload the home page
    else:
        form = TodoForm()  # Empty form for adding a new todo
    return render(request, 'home.html', {'todos': todos, 'form': form})

@require_POST
def toggle_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
        todo.completed = not todo.completed
        todo.save()
        return JsonResponse({'status': 'success'})
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

