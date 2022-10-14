import io


from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .models import *




class ArtistsSerializer(serializers.ModelSerializer):#Создание сериализатора с помощью RestFrramework. Быстро и мало кода
    class Meta:
         model = Artists
         fields = ('title', 'slug', 'content', 'time_create', 'time_update', 'is_published', 'cat_id')# Поля, с которыми можно работать через json
        # Можно ещё так fields = __all__


# class ArtistsSerializer(serializers.Serializer): #Здесь сериализатор создан вручную. Сравнительно больше кода
#     title = serializers.CharField(max_length=255)#Сериализатор преобразует данные в json-формат
#     content = serializers.CharField()
#     # time_create = serializers.DateTimeField()
#     # time_update = serializers.DateTimeField()
#     is_published = serializers.BooleanField(default=True)
#     cat_id = serializers.IntegerField()
#
#     def create(self, validated_data): #Этот создаёт и сохраняет данные из json-строки в базу данных
#         return Artists.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):#Метод позволяет менять данные в базе (изменённые данные берутся из json-строки)
#         instance.title = validated_data.get("title", instance.title)#Здесь бёрем изменённые даные из json-строки для поля title.Если данных нет, то берём существующий instance.title
#         instance.content = validated_data.get("content", instance.content)
#         instance.time_update = validated_data.get("time_update", instance.time_update)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         instance.save() #Сохраняем новые данные из json-строки в базу данных
#         return instance


# class ArtistsModel: #Ниже представлен пример создания json строки на основе данных атрибутов объекта класса на яз. python с помощью сериализатора, и наоборот - расшифровка json данных и передачи из в формат python
#     def __init__(self, title, content, cat_id):
#         self.title = title
#         self.content = content
#         self.cat_id = cat_id

# class ArtistsSerializer(serializers.Serializer):#Класс, на основе которого будет создаваться объект. Атрибуты этого объекта будут направлены в методе encode в виде json
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     cat_id = serializers.IntegerField()

# def encode(): #Кодирование данных на основе данных атрибутов объекта класса на яз. python в json
#     model = ArtistsModel('Vasya', 'Vasina biografiya', 1)
#     model_sr = ArtistsSerializer(model)
#     print(model_sr.data, type(model_sr.data),sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():#Декодирование данных json в атрибуты объекта класса на яз. python
#     stream = io.BytesIO(b'{"title": "Dmitry", "content": "Biography of Dmitry", "cat_id": "1"}')
#     data = JSONParser().parse(stream)
#     serializer = ArtistsSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
