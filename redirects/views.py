from django.shortcuts import render, redirect

def redirects(request):
    return redirect('blog/')