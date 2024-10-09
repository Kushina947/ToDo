from django.shortcuts import render

def top(request):
    ctx = {'title': 'testtttttttt', 'aaaa': 'bbbb'}
    return render(request, 'base/top.html', ctx)
