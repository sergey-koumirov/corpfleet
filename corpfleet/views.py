from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    print('@login_required')
    return render(request, 'corpfleet/index.html')
