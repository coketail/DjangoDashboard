from django.shortcuts import render
from youtube.models import AccountInfo
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):

    info = AccountInfo.objects.first() # get(id=1) 보다 안전한 방법입니다.
    context = {"info":info}
    return render(request,'youtube/index.html',context)