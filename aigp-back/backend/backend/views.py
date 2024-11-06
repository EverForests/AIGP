from django.http import HttpResponse
from django.shortcuts import render
 
def hello(request):
    return HttpResponse("Hello world ! ")


def runoob(request):
    context = {}
    context['hello'] = 'Hello World!'  # 模版参数的映射位置
    return render(request, 'runoob.html', context)