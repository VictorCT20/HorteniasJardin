from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.

class UserEntryView(View):
    def get(self, request, *args, **kwargs):
        context={
        }
        return render(request, 'interfaceUser.html', context)