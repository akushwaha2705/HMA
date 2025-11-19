from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse

from .forms import PDFUploadForm
from .models import UploadedPDF

from fleetAI.query import QueryRetriever


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                # Prevent superuser from logging in via this view
                return HttpResponse("Invalid login")
            else:
                login(request, user)
                # Redirect to chat view after successful login
                return HttpResponseRedirect('/chat/')
        else:
            return HttpResponse("Invalid login")


class ChatView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "chat.html")
    
    def post(self, request):
        # Get the logged-in user
        user = request.user
        # Assuming each user is associated with only one group; modify as needed
        user_group = user.groups.first()

        if not user_group:
            return JsonResponse({'error': 'User not associated with any group'}, status=400)

        # Extract the query from the form input (assuming the input name is "query")
        query = request.POST.get('query')
        
        if not query:
            return JsonResponse({'error': 'No query provided'}, status=400)

        # Replace this with actual query handling and fetching result
        retriever = QueryRetriever(collection=user_group.name)
        result = retriever.retrieve(query)

        return JsonResponse({'result': result})
        

class PDFUploadView(LoginRequiredMixin, CreateView):
    model = UploadedPDF
    form_class = PDFUploadForm
    template_name = 'upload.html'
    success_url = reverse_lazy('chat')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
