from typing import List
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import regist, CustomUser, curs, lessons, lessons_text, buy_curs
from .forms import registform, byu_cursForm
from django.contrib.auth.hashers import make_password
from django.http import StreamingHttpResponse
from .services import open_file
from django.views import generic
from datetime import datetime
from django.core.mail import send_mail
from .serializers import CustomUserSerializer, RegistSerializer, CursSerializer, LessonsSerializer, LessonsTextSerializer, BuyCursSerializer    
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
def index(request):
    return render(request, 'main/index1.html')


def about(request):
    return render(request, 'main/about.html')

class CustomUserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
# @api_view(['POST'])
class RegistCreate(APIView):
    def post(self, request):
        serializer = RegistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.create_user(
                serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password1']
            )
            
            return Response({'new_user': user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CursList(generics.ListCreateAPIView):
    queryset = curs.objects.all()
    serializer_class = CursSerializer

class CursDetailView(generics.RetrieveAPIView):
    queryset = curs.objects.all()
    serializer_class = CursSerializer

# @login_required
# @permission_required('curs.add_choice', login_url='/curs')
def accounts(request):
    username1 = request.user.username
    user = CustomUser.objects.filter(username=username1).first()
    context = {
        'curs_user': []
    }
    for i in user.curss:
        context['curs_user'].append(user.curss[str(i)])

    return render(request, 'main/account.html', context)


def registration(request):
    if request.method == 'POST':
        form = registform(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(form.cleaned_data['username'])
            user.first_name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.password = make_password(form.cleaned_data['password1'], salt=None, hasher='default')
            # user.is_active = False
            user.save()
            form.save()
            text = 'Вы зарегестрировались на сайте \nДля подтверждения своей почте перейдите по ссылке: http://127.0.0.1:8000/' + str(user.uuid)
            send_mail('Привет',
                      text,
                      'support@xn----7sbzffr6a4b.xn--p1ai',
                      [form.cleaned_data['email']],
                      fail_silently=False)

            return render(request, 'main/register_done.html', {'new_user': user})
        else:
            context = {
                'form': form
            }
            return render(request, 'main/registr.html', context)

    form = registform()
    context = {
        'form': form
    }
    return render(request, 'main/registr.html', context)


def email(request, pk:str):
    user = CustomUser.objects.filter(uuid=pk).first()
    user.is_active = True
    user.save()
    context = {
            'name' : user.username,
        }
    return render(request, 'registration/email_done.html', context)
# def curs_html(request):
#     lessons = curs.objects.order_by('-id')
#     context = {
#         'curs' : lessons,
#     }
#     return render(request, 'main/curs.html', context)


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response.data


class cursListView(generic.ListView):
    model = curs


def cursDetailView(request, pk:int, **kwargs):
    name_curs = curs.objects.get(id=pk)
    print(kwargs)
    if request.user.is_authenticated:
        username1 = request.user.username
        user = CustomUser.objects.filter(username=username1).first()

        if request.method == 'POST':
            length_curs = len(lessons.objects.filter(curs_id=pk)) #получение всех уроков курса
            print(datetime.now(), 'кнопка нажата')
            if str(pk) not in user.curss:
                user.curss[str(pk)] = {'name_curs':name_curs.name, 'date': str(datetime.now().date()), 'procent': 0, 'length': length_curs, 'progress': []}
                user.save()

        if str(pk) in user.curss:
            context = {
                'ans': True,
                'curs' : name_curs,
            }
        else:
            context = {
                'curs' : name_curs,
                }
    else:
        context = {
            'curs': name_curs,
        }

    return render(request, 'main/curs_detail.html', context)
    # permission_required = 'main.view_post'


@login_required
def my_curs(request):
    username1 = request.user.username
    user = CustomUser.objects.filter(username=username1).first()

    name_curs = []
    for i in user.curss:
        name_curs.append(curs.objects.get(id=str(i)))

    if len(name_curs) == 0:
        context = {
            'curs': name_curs,
            }
    else:
        context = {
            'cur' : True,
            'curs' : name_curs,
        }
    return render(request, 'main/my_curs.html', context)


@login_required
def my_curs_detail(request, pk:int, pn:int):
    username1 = request.user.username
    user = CustomUser.objects.filter(username=username1).first()
    user_progress = user.curss[str(pk)]['progress']  # список пройденных уроков
    length_curs = len(lessons.objects.filter(curs_id=pk))  # получение всех уроков курса

    if str(pn) not in user_progress and pn != 0:
        user.curss[str(pk)]['progress'].append(str(pn))
        user.curss[str(pk)]['length'] = length_curs
        user.curss[str(pk)]['procent'] = round((len(user_progress)/user.curss[str(pk)]['length'])*100)
        user.save()

    user_procent = user.curss[str(pk)]['procent'] #процент прохождения курса
    # user_procent = round((len(user_progress)/user.curss[str(pk)]['length'])*100)

    if str(pk) in user.curss:
        name_curs = curs.objects.get(id=pk)  # имя всего курса
        name_lessons = lessons.objects.filter(curs_id=pk)  # уроки курса
        if pn !=0:
            name_lesson = name_lessons.get(id=pn)
            dop_name_les = lessons_text.objects.filter(lesson_id=pn)
            context = {
                'cur': True,
                'less': name_lessons,
                'one': name_lesson,
                'text': dop_name_les,
                'curs': name_curs,
                'vid': True,
                'proc': user_procent
            }
        else:
            context = {
                'cur': True,
                'less': name_lessons,
                'one': {'name': name_curs, 'text': 'Выберите нужный урок'},
                # 'text': dop_name_les,
                'curs': name_curs,
                'vid': False,
                'proc': user_procent
            }
    else:
        return index(request)
    return render(request, 'main/my_curs_detail.html', context)