from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


import hashlib
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PapersModel


def checkdata(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def addpapers(request):
    login = request.session.get('login', None)  
    if request.method == "POST":
        title = request.POST['title']
        files = request.FILES['pdf']
        year = request.POST['year']
        
        temp_dir = os.path.join('static', 'tempfiles')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        filepath = os.path.join(temp_dir, files.name)

        with open(filepath, 'wb+') as destination:
            for chunk in files.chunks():
                destination.write(chunk)

        with open(filepath, 'rb') as f:
            data = f.read()
        
        hashed = checkdata(data)  
        
        os.remove(filepath)
        
        if PapersModel.objects.filter(paper_data=hashed).exists():
            messages.error(request, 'Paper already exists')
            return redirect('addpapers')
        else:
            data = PapersModel.objects.create(
                title=title, year=year, files=files, paper_data=hashed
            )
            data.save()
            messages.success(request, 'Paper uploaded successfully')
            return redirect('addpapers')
        
    return render(request, 'addpapers.html', {'login': login})


def removepapers(request, id):
    login = request.session['login']
    data = PapersModel.objects.get(id=id)
    data.delete()
    messages.success(request, 'Paper Removed Successfully')
    return redirect('viewpapers')   

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import PapersModel

# def updatepapers(request, id):
#     login = request.session.get('login')  # Using get() is safer in case 'login' doesn't exist
#     try:
#         data = PapersModel.objects.get(id=id)
#     except PapersModel.DoesNotExist:
#         # If the paper doesn't exist, redirect or show an error
#         messages.error(request, 'Paper not found.')
#         return redirect('viewpapers')

#     if request.method == "POST":
#         title = request.POST.get('title')  # Safer access for POST data
#         year = request.POST.get('year')  # Safer access for POST data
#         files = request.FILES.get('pdf')  # Access the file with 'pdf', since that's the name in the form

#         # Update the paper's fields
#         if title:
#             data.title = title
#         if year:
#             data.year = year
#         if files:
#             data.files = files  # Update the PDF file if uploaded

#         # Save the changes
#         data.save()

#         # Display success message and redirect
#         messages.success(request, 'Paper Updated Successfully')
#         return redirect('viewpapers')

#     return render(request, 'updatepaper.html', {'data': data, 'login': login, 'id': id})
