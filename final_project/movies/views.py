from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib import messages

from .forms import UserRegistrationForm, UserProfileForm, MovieForm, ReviewForm, CustomAuthenticationForm
from .models import Movie, Review, UserProfile

@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('movies:profile')
    else:
        user_form = UserRegistrationForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'register/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('movies:movie_list')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'register/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('movies:login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            # Check if the user already has a profile
            if not hasattr(user, 'userprofile'):
                profile = UserProfile.objects.create(user=user)
            else:
                profile = user.userprofile

            profile_form = UserProfileForm(request.POST, instance=profile)
            profile_form.full_clean()  # Ensure all fields are valid
            profile_form.save()

            login(request, user)

            # Send welcome email
            send_mail(
                'Welcome to Movie Platform!',
                'Thank you for registering on our platform.',
                'aiswarya@example.com',  # From email
                [user.email],  # To email
                fail_silently=False,
            )

            # Add a success message
            messages.success(request, 'You have successfully registered!')

            return redirect('movies:movie_list')
    else:
        form = UserRegistrationForm()
        profile_form = UserProfileForm()
    return render(request, 'register/register.html', {'form': form, 'profile_form': profile_form})
@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movies:movie_list')
    else:
        form = MovieForm()

    return render(request, 'movie/add_movie.html', {'form': form})

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this movie.")

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_list')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movie/edit_movie.html', {'form': form})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this movie.")

    if request.method == 'POST':
        movie.delete()
        return redirect('movies:movie_list')

    return render(request, 'movie/delete_movie.html', {'movie': movie})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie/movie_list.html', {'movies': movies})

def search_movies(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movie/add_review.html', {'movies': movies})

def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})

def base(request):
    movies = Movie.objects.all()
    return render(request, 'base.html', {'movies': movies})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:movie_list')
    else:
        form = ReviewForm()

    return render(request, 'movie/add_review.html', {'form': form, 'movie': movie})
