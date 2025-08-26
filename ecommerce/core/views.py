from django.shortcuts import render

# Create your views here.
def home_public(request):
  return render(request, "core/home_public.html")