from django.shortcuts import render,redirect
from dashboard.models import StolenItem,StolenItemImage
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import nltk
from dashboard.models import StolenItem,ReportItem,Match
from django.dispatch import receiver
nlp = spacy.load("en_core_web_sm")
nltk.download("punkt")
nltk.download("stopwords")


def dashboard(request):
    if request.method=="POST":
        if 'name' in request.POST:
            name = request.POST.get("name")
            category = request.POST.get("category")
            description = request.POST.get("description")
            stolen_datetime = request.POST.get("stolen_datetime")
            location = request.POST.get("location")
            location_description = request.POST.get("location_description")
            images = request.FILES.getlist("image")  
            print(name,category,description,stolen_datetime,location,location_description)
            #keywords find

            doc = nlp(f"{description.lower()} {location_description} {location}")
            extracted_keywords = set(token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"])


            # stop_words = set(stopwords.words("english"))
            # words = word_tokenize(f"{description.lower()} {location_description}") 
            # keywords = [word for word in words if word.isalnum() and word not in stop_words]
            
            word_str = ", ".join(extracted_keywords)
            st_obj = StolenItem(name=name, user =request.user,category=category,description=description,stolen_datetime=stolen_datetime,keywords=word_str,location=location,location_description=location_description)
            
            st_obj.save()
            for image in images:
                st_img = StolenItemImage(stolen_item=st_obj,image=image)
                st_img.save()

        if 'reportname' in request.POST:
            name = request.POST.get("reportname")
            category = request.POST.get("category")
            description = request.POST.get("description")
            stolen_datetime = request.POST.get("stolen_datetime")
            location = request.POST.get("location")
      
            doc = nlp(f"{description.lower()} {location}")
            extracted_keywords = set(token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"])

            
            word_str = ", ".join(extracted_keywords)
            re_obj = ReportItem(name=name, user =request.user,category=category,description=description,stolen_datetime=stolen_datetime,keywords=word_str,location=location)
            
            re_obj.save()
            

        if "sname" in request.POST:
            search = request.POST.get("sname")
            return redirect(f"/dashboard/search/{search}")

        if "sdes" in request.POST:
            search = request.POST.get("sdes")
            mat = Match(query=search)
            mat.save()
            return redirect(f"/dashboard/searchdes/{search}")
            #return redirect(f"/dashboard/searchdes/{mat.uid}")

    stolen = StolenItem.objects.filter(user=request.user)
    report = ReportItem.objects.filter(user=request.user)
    # print(len(stolen))
    # for st in stolen:
    #     print(st.name)
    data = {
        'items':stolen,
        'reports':report,
        'message':"success"
    }   
           
    return render(request,'dashboard.html',context=data)

def searchquery(request,query):
    stolen_item= StolenItem.objects.filter(name__icontains=query)
    
    return render(request,'searchquery.html',{'searches':stolen_item})

def searchdescr(request,query):
   # se = Match.objects.get(query=query)
    obj = StolenItem.find_matching_items(query)
    print("in search",obj)
    for i in obj:
        print(i.name)
    return render(request,'searchquery.html',{'searches':obj})


def delete_stolen(request,id):
    obj = StolenItem.objects.get(uid=id)
    if request.method =="POST":
        
        obj.delete()
        return redirect("/dashboard/home")
    return render(request,'delete.html',{'data':obj})


def delete_report(request,id):
    obj = ReportItem.objects.get(uid=id)
    if request.method =="POST":
        obj.delete()
        return redirect("/dashboard/home")
    return render(request,'delete.html',{'data':obj})
