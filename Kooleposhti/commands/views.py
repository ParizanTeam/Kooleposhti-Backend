from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
import os
import datetime


@api_view(['GET'])
def push_to_repo(request):
    bash_cmds = [
        'git add .',
        f'git commit -m {datetime.datetime.now()}',
        'git push'
    ]
    pass
