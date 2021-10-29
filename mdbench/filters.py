
import django_filters
from django import forms
from .models import BenchmarkInstance

class BenchmarkInstanceFilter(django_filters.FilterSet):

    class Meta:
        model = BenchmarkInstance
        fields = {
            'software__name':['contains'],
            'site__name':['contains'],
            'software__instruction_set':['exact'],
            'benchmark__name' : ['exact'],
            }
       
    