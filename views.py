from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,QueryDict, HttpResponseBadRequest
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
import uuid
from ip2geotools.databases.noncommercial import DbIpCity
import folium
import random, string, os, requests, time
from django.conf import settings
import csv
import json
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from collections import defaultdict
from django.db.models import Q
from urllib.parse import unquote


@method_decorator(login_required, name='dispatch')
class BinderViewSet(viewsets.ModelViewSet):
    queryset = Binder.objects.all()
    serializer_class = BinderSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
            
        else:
            raise ValueError("User must be authenticated to create a folder.")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('Binder')  # Redirect to 'Binder' after signup
    template_name = './auth/signup.html'

    def form_valid(self, form):
        # Call the original form_valid to save the user
        response = super().form_valid(form)
        # Authenticate the user
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        # Log the user in
        login(self.request, user)
        # Rest of the code...
        return response

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to 'login' after logout

class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('Binder')  # Redirect to 'Binder' after login
    template_name = './auth/login.html' 

    def form_valid(request, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse('login_fail'))  # Redirect to 'login_fail' if login failed



def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to 'login' after logout

class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('Binder')  # Redirect to 'Binder' after login
    template_name = './auth/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse('login_fail'))  # Redirect to 'login_fail' if login failed


class LoginApiView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            # Here you can add code to generate a token and return it in the response
            return Response({"message": "Successful login"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class BinderListView(View):
    def get(self, request, *args, **kwargs):
        Binders = Binder.objects.filter(user=request.user)
        serializer = BinderSerializer(Binders, many=True)
        data = serializer.data
        return render(request, './Pages/Binder.html', {'parents': data})

@method_decorator(login_required, name='dispatch')
class BinderCreateViewSet(View):  
    def post(self, request, *args, **kwargs):
        form = BinderForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                print(form.cleaned_data)
                instance = form.save(commit=False)
                instance.user = request.user  # Set the user before saving
                instance.save()
                return HttpResponseRedirect('/Binder/')
        return render(request, './Pages/BinderCreate.html', {'form': form})
    
    def get(self, request, *args, **kwargs):
        form = BinderForm(request.POST or None)
        return render(request, './Pages/BinderCreate.html', {'form': form})
    
@method_decorator(login_required, name='dispatch')
class BinderRetrieveView(View):
    def get(self, request, pk, *args, **kwargs):
        Binders = get_object_or_404(Binder, user=request.user, pk=pk)
        form = FolderForm(initial={'binderId': pk})     
        serializer = BinderSerializer(Binders)
        data = serializer.data
        return render(request, './Pages/BinderDetail.html', {'parents': data, "form": form})
    
    def post(self, request, pk, *args, **kwargs):
        binder = get_object_or_404(Binder, user=request.user, pk=pk)
        serializer = BinderSerializer(binder)
        data = serializer.data
        # Create a new Folder object nested within the retrieved Binder
        new_folder = Folder.objects.create(binderId=binder, name=request.POST['name'], user=request.user)
        new_folder_serializer = FolderSerializer(new_folder)
        new_folder_data = new_folder_serializer.data                
        return HttpResponseRedirect(f'/Binder/{pk}')

def flatten_dict(d):
    def expand(key, value):
        if isinstance(value, dict):
            return [(key + '.' + k, v) for k, v in flatten_dict(value).items()]
        else:
            return [(key, value)]

@method_decorator(login_required, name='dispatch')
class FolderRetrieveView(View):
    def get(self, request, pk, *args, **kwargs):
        form = FileForm(initial={"folderId": pk}) 
        PForm = ProcessForm(initial={"folderId": pk})
        PSForm = ProcessSinglesForm(initial={"folderId": pk})
        DPSForm = deleteSinglesForm(initial={"folderId": pk})
        DForm = DeleteForm(initial={"folderId": pk})
        folder = get_object_or_404(Folder, user=request.user, pk=pk)
        serializer = FolderSerializer(folder)
        data = serializer.data
        
        return render(request, './Pages/FolderDetail.html', {'parent': data, "form": form, "ProcessForm": PForm, "DeleteForm": DForm, "PSForm": PSForm, "DPSForm": DPSForm, 'user': request.user})

    def post(self, request, pk, *args, **kwargs): 
        form = FileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            file = request.FILES['file']
            filename, file_extension = os.path.splitext(file.name)
            name = form.cleaned_data.get('name')
            if file_extension == '.csv':
                new_file = File.objects.create(folderId=Folder.objects.get(pk=pk), file=file, user=request.user, name=name)
                with open(new_file.file.path, 'r') as f:
                    data = self.csv_to_json(f)
                    data = self.parse_json(data)
                    filename = filename + '.json'
                    file.name = filename
                    flattened_data = [self.flatten_dict(d) for d in data]
                    new_file.dataDoct = self.align_dict_keys(flattened_data)
                    new_file.save()
                return HttpResponse("File uploaded and saved successfully.")
            elif file_extension == '.json':
                new_file = File.objects.create(folderId=Folder.objects.get(pk=pk), file=file, user=request.user, name=name)
                with open(new_file.file.path, 'r') as f:
                    data = f.read()
                    flattened_data = [self.flatten_dict(d) for d in json.loads(data)]
                    new_file.dataDoct = self.align_dict_keys(flattened_data)
                    new_file.save()
                return HttpResponse("File uploaded and saved successfully.")
            else:
                return JsonResponse({"error": "Invalid file format. Only .json and .csv files are allowed."}, status=400)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    def csv_to_json(self, csv_file):
        reader = csv.DictReader(csv_file.read().splitlines())
        data = list(reader)
        return data

    def parse_json(self, data):
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        elif isinstance(data, dict):
            return {k: self.parse_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.parse_json(i) for i in data]
        else:
            return data

    def align_dict_keys(self, data):
        if isinstance(data, list) and all(isinstance(i, dict) for i in data):
            # Get all keys from all dictionaries
            keys = set(k for d in data for k in d.keys())
        
            # Create new dictionaries with all keys
            aligned_data = []
            for d in data:
                new_dict = {k: d.get(k, None) for k in keys}
                aligned_data.append(new_dict)
        
            return aligned_data
        else:
            return data

    def flatten_dict(self, d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if k == 'AuditData' and isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            elif k == 'AuditData' and isinstance(v, list) and all(isinstance(i, dict) for i in v):
                for i, dict_item in enumerate(v):
                    items.extend(self.flatten_dict(dict_item, f"{new_key}_{i}", sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

@method_decorator(login_required, name='dispatch')
class FileView(View):
    def get(self, request, pk, *args, **kwargs):
        form = FolderForm() 
        file = get_object_or_404(File, user=request.user, pk=pk)
        serializer = FileSerializer(file)
        data = serializer.data

        # Get search query and URL decode it
        q = request.GET.get('q')
        if q:
            q = unquote(q)
            # Filter data based on search query
            data['dataDoct'] = [item for item in data['dataDoct'] if q.lower() in str(item).lower()]

        # Get sort key
        sort = request.GET.get('sort')
        if sort:
            # Sort data based on sort key
            reverse = sort.startswith('-')
            key = sort[1:] if reverse else sort
            data['dataDoct'] = sorted(data['dataDoct'], key=lambda item: str(item.get(key)) or '', reverse=reverse)

        paginator = Paginator(data['dataDoct'], 100)  # Show 100 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, './Pages/FileDetail.html', {'parent': page_obj, "form": form})
    
    def post(self, request, Filepk, Folderpk, *args, **kwargs):  # Add pk as a parameter
        action = request.POST.get('action')
        if action == 'delete':
            instance = get_object_or_404(File, user=request.user, pk=Filepk)
            instance.delete()
            return HttpResponseRedirect(f'/Binder/Folder/{Folderpk}')
        else:
            return HttpResponseBadRequest('Invalid action')


def get_ip_info(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}')
    return response.json()

@method_decorator(login_required, name='dispatch')
class AnalyticsView(View):
    def post(self, request, *args, **kwargs):
        instance = request.POST['action']
        print(instance)
        if 'process' == instance:
            return self.process(request, *args, **kwargs)
        elif 'delete' == instance:
            return self.delete(request, *args, **kwargs)
        elif 'processSingles' == instance:
            return self.processSingles(request, *args, **kwargs)
        elif 'deleteSingles' == instance:
            return self.deleteSingles(request, *args, **kwargs)        
        else:
            return HttpResponseBadRequest("Invalid POST request")

    def processSingles(self, request, Folderpk, Filepk, *args, **kwargs):
        folder = get_object_or_404(Folder, user=request.user, pk=Folderpk)
        file = get_object_or_404(File, user=request.user, pk=Filepk)
        # Access the file data directly, skipping the first files for loop
        file_data = file.dataDoct
        # Now you have the file data and you can use it as needed
        seens = []
        map = folium.Map(location=[0, 0], zoom_start=2)
        users = [ ]
        for record in file_data:
            ip = record.get('ipAddress') or record.get('IP address') or record.get('clientIP')
            UserId = record.get('UserId') or record.get('userId')
            Operation = record.get('Operation') or record.get('operation')
            if ip and ip not in seens and type(ip) != None:
                try:
                    seens.append(ip)
                    ipwhois_obj = IPWhois(ip)
                    data = ipwhois_obj.lookup_rdap(depth=1)
                    response = get_ip_info(ip)
                    responsejson = response
                    location = [responsejson['lat'], responsejson['lon']]

                    # Append each responsejson to userLocation
                    file.userLocation = file.userLocation if file.userLocation else []
                    file.userLocation.append(responsejson)

                    # Append new ipWhois to the instance
                    file.ipWhois = data

                    folium.Marker(location, popup=f'<i>{ip}</i>', tooltip='<div>' + '<br>'.join([f"{k}: {v}" for k,v in record.items() if v and v != 'none']) + '</div>').add_to(map)

                except:
                    continue
            if UserId and UserId not in users and type(UserId) != None:
                print(UserId)
                users.append(UserId)
        # Add a marker to the map for each location
        file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))       
        print('cat')
        # Save the map as an HTML file with the generated file name
        base_dir = './order365/static/maps/'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        name = os.path.join(base_dir, f'{file_name}.html')
        map.save(name)
        
        file.userMap = name
        file.save()
        return HttpResponseRedirect(f'/Binder/Folder/{Folderpk}')

    def deleteSingles(self, request, Folderpk, Filepk, *args, **kwargs):
        instance = File.objects.filter(user=request.user, pk=Filepk)
        # Delete the userMap file from the system before clearing the field
        if instance.userMap:
            user_map_path = os.path.join(settings.BASE_DIR, str(instance.userMap))
            if os.path.exists(user_map_path):
                os.remove(user_map_path)
        instance.ipWhois = None  # Clear the ipWhois field
        instance.userMap = None  # Clear the userMap field
        instance.userLocation = None  # Clear the userLocation field
        instance.save()  # Save the changes to the instance
        return HttpResponseRedirect(f'/Binder/Folder/{Folderpk}')

    def process(self, request, pk, *args, **kwargs):
        instance = Folder.objects.filter(user=request.user, pk=pk)
        files = instance.files.all()  # Get all files in the folder

        seens = []
        map = folium.Map(location=[0, 0], zoom_start=2)

        for file in files:
            dataDoct = file.dataDoct
            # Extract the 'ipAddress' from each record in dataDoct
            for record in dataDoct:
                time.sleep(2)
                ip = record.get('ipAddress') or record.get('IP address')
                if ip and ip not in seens and type(ip) != None:
                    try:
                        print(ip)
                        seens.append(ip)
                        ipwhois_obj = IPWhois(ip)
                        data = ipwhois_obj.lookup_rdap(depth=1)
                        response = get_ip_info(ip)
                        print(type(response))
                        responsejson = response
                        print(f"IP: {ip}, Location: {responsejson}")  # Print the IP and location
                        print([responsejson['lat'], responsejson['lon']])
                        location = [responsejson['lat'], responsejson['lon']]

                        # Append each responsejson to userLocation
                        instance.userLocation = instance.userLocation if instance.userLocation else []
                        instance.userLocation.append(responsejson)

                        # Append new ipWhois to the instance
                        instance.ipWhois = data
                        

                        folium.Marker(location, popup=f'<i>{ip}</i>', tooltip='Node Alt Text').add_to(map)

                    except:
                        continue
        # Initialize a map centered at [0, 0]

        # Add a marker to the map for each location
        file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))       
        print('cat')
        # Save the map as an HTML file with the generated file name
        name = f'/order365/static/maps/{file_name}.html' 
        map.save(name)
        instance.userMap = name
        instance.save()
        return HttpResponseRedirect(f'/Binder/Folder/{pk}')


    def delete(self, request, pk, *args, **kwargs):
        instance = Folder.objects.filter(user=request.user, pk=pk)
        # Delete the userMap file from the system before clearing the field
        if instance.userMap:
            user_map_path = os.path.join(settings.BASE_DIR, instance.userMap)
            if os.path.exists(user_map_path):
                os.remove(user_map_path)
        instance.ipWhois = None  # Clear the ipWhois field
        instance.userMap = None  # Clear the userMap field
        instance.userLocation = None  # Clear the userLocation field
        instance.save()  # Save the changes to the instance
        return HttpResponseRedirect(f'/Binder/Folder/{pk}')
