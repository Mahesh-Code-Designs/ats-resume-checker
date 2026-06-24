from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from .resume_page import Resumepage
import os
import csv
import pandas as pd

# Create your views 

def upload_resume(request):
    if request.method == 'POST':
        files = request.FILES.getlist('resume')
        results = []

        for resume in files:
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            file_path = os.path.join(settings.MEDIA_ROOT, resume.name )

            with open (file_path , 'wb+') as destination:
                for chunk in resume.chunks():
                    destination.write(chunk)
            page = Resumepage(file_path)

            name = page.get_name()
            email = page.get_email()
            score = page.calculate_score()

            status = "Shortlisted" if score >=60 else "Rejected"

            if score >=60:
                file_exists = os.path.isfile("shortlisted.csv")
                with open("shortlisted.csv", 'a' , newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(["Name", "Email" "Score"])
                    writer.writerow([name,email,score])

            results.append({
                'name': name,
                'email': email,
                'score': score,
                'status': status
            })
        return render (request, 'resumeapp/upload.html',{'results':results})
    return render(request,'resumeapp/upload.html')

def dashboard(request):
    if os.path.exists('shortlisted.csv'):
        data = pd.read_csv('shortlisted.csv')
    else:
        data = pd.DataFrame(columns=['Name','Email','Score'])
    count = len(data)
    avg = data['Score'].mean() if not data.empty else 0

    return render( request, 'resumeapp/dashboard.html',{
        'count': count,
        'avg': round(avg,2)
    })

def download_csv(request):
    return FileResponse(open('shortlisted.csv','rb'), as_attachment= True)   
