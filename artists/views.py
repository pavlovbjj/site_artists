from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.response import Response

from .forms import *
from .models import *
from .utils import *
from .serializers import *

# def index(request):
#     posts = Artists.objects.all().order_by('title')
#     context = {'title': 'Список статей', 'posts': posts, 'cat_selected': 0}
#     return render(request, 'artists/index.html', context)

class ArtistsHome(DataMixin, ListView):
    model = Artists
    template_name = 'artists/index.html'
    context_object_name = 'posts'
    #extra_context = {'title': 'Главная страница'}
    allow_empty = False
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")#Данные формируются с помощью DataMixin (находится в файле utils.py
        return dict(list(context.items())+ list(c_def.items()))

    def get_queryset(self): #Выводим на главную страницу только опубликованные статьи
        return Artists.objects.filter(is_published=True).select_related('cat') #select_related('cat') добавили, чтобы избежать повторного обращения к базе данных при загрузке надписей категорий


# def categories(request, cat_slug):
#     if cat_slug == 'muzhchiny':
#         cat_id = 1
#     elif cat_slug == 'zhenshiny':
#         cat_id = 2
#     posts = Artists.objects.filter(cat=cat_id)
#     if len(posts) == 0:
#         raise Http404()
#     context = {'title': 'Категории', 'cat_selected': cat_id, 'posts': posts}
#     return render(request, 'artists/index.html', context)
class ArtistsCategory(DataMixin, ListView):
    model = Artists
    template_name = 'artists/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Artists.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat') #select_related('cat') добавили, чтобы избежать повторного обращения к базе данных

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Категория - ' + str(context['posts'][0].cat), cat_selected = context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:  # Если пользователь не авторизован, то удаляем из словаря menu строку "Добавить статью"
        user_menu.pop(1)
    context = {'title': 'О сайте', 'menu': user_menu}
    return render(request, 'artists/about.html', context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form=AddPostForm()
#     context = {'title': 'Добавить статью', 'form': form}
#     return render(request, 'artists/addpage.html', context)

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    #form_class = UserCreationForm #Стандартная форма
    form_class = AddPostForm #Пользовательская форма
    template_name = 'artists/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))



# def contact(request):
#     context = {'title': 'Обратная связь',}
#     return render(request, 'artists/contact.html', context)
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'artists/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        send_mail(form.cleaned_data['name'], form.cleaned_data['content'], 'pavlovda1989@mail.ru',['d.a.pavlov@urfu.ru'])
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     context = {'title': 'Войти',}
#     return render(request, 'artists/login.html', context)

# def show_post(request, post_slug):
#     post = get_object_or_404(Artists, slug=post_slug)
#     context = {'title': '', 'post': post, 'cat_selected': post.cat_id}
#     return render(request, 'artists/post.html', context)
class ShowPost(DataMixin, DetailView):
    model = Artists
    template_name = 'artists/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    #form_class = AuthenticationForm #Стандартная форма
    form_class = RegisterUserForm #Пользовательская форма
    template_name = 'artists/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = "Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form): #Если пользователь правильно заполнил форму, то сохраняем его данные и выполняем его авторизацию на сайте, переводим на главную старницу
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'artists/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')




class ArtistsAPIView(generics.ListAPIView): #Создание APIView для переформатирования данных из атрибутов объекта класса Artists на яз. python в json и наоборот.
    queryset = Artists.objects.all()       #ListAPIView позволяет принимать инфу из базы данных об объектах в виде json (метод Post)
    serializer_class = ArtistsSerializer  #С помощью RestFramework


class ArtistsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):  #Создание APIView для переформатирования данных из атрибутов объекта класса Artists на яз. python в json и наоборот.
    queryset = Artists.objects.all()                    #RetrieveUpdateDestroyAPIView позволяет принимать инфу из базы данных по объекту в виде json (метод Post), создавать объекты в базе, менять их и удалять
    serializer_class = ArtistsSerializer                #С помощью RestFramework

# class ArtistsAPIView(APIView):  #Создание APIView для переформатирования данных из атрибутов объекта класса Artists на яз. python в json и наоборот.Вручную (кода в разы больше)
#     def get(self, request): #Отправляем данные обо всех артистах в виде json строки
#         a = Artists.objects.all()
#         return Response({'posts': ArtistsSerializer(a, many=True).data})
#
#     def post(self, request): #Принимаем данные об артисте в виде json строки и переформатируем её в атрибуты объёкта класса Artists на яз. python
#         serializer = ArtistsSerializer(data=request.data)# Распаковка данных из json строки
#         serializer.is_valid(raise_exception=True)#Проверка корректности введённых данных
#         serializer.save()
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs): #Метод позволяет вносить изменнёные данные из json-строки в базу данных на основе метода update из serializers.py
#         pk = kwargs.get("pk", None) #Берём ключ pk, если он есть в словаре
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#         try:
#             instance = Artists.objects.get(pk=pk)#Проверка, есть ли в базе данных объект с заданным номером pk
#         except:
#             return Response({"error": "Object does not exsists"}) # Если объекта с номером pk (pk берётся из json-строки) нет в базе данных, то выдётся ошибка
#         serializer = ArtistsSerializer(data=request.data, instance=instance)#Если объект с заднным номером есть, то переформатируем данные в python с помощью сериализатора
#         serializer.is_valid(raise_exception=True)#ПРоверка валидности данных
#         serializer.save()#Если всё ок, то сохраняем данные в базу
#         return Response({"post": serializer.data})#Возвращаем клиенту инфу о том, какие данные были внесены в базу данных
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)  # Берём ключ pk, если он есть в словаре
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#         try:
#             instance = Artists.objects.get(pk=pk)  # Проверка, есть ли в базе данных объект с заданным номером pk
#         except:
#             return Response({"error": "Object does not exsists"})  # Если объекта с номером pk (pk берётся из json-строки) нет в базе данных, то выдётся ошибка
#         Artists.objects.get(pk=pk).delete()
#         return Response({"post": "delete post " + str(pk)})