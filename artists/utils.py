from artists.models import Category
# from django.core.cache import cache

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'addpage'},
        {'title': 'Обратная связь', 'url_name': 'contact'}]


class DataMixin:
    paginate_by = 4 #количество отображаемых статей на 1 странице
    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = cache.get('cats') #Кэширование боковой панели категорий
        # if not cats:
        #     cats = Category.objects.all()
        #     cache.set('cats', cats, 60)
        cats = Category.objects.all() # Если включаем кэширование боковой панели категорий эту строку надо закоментировать

        user_menu = menu.copy()
        if not self.request.user.is_authenticated: #Если пользователь не авторизован, то удаляем из словаря menu строку "Добавить статью"
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context