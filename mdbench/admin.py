from django.contrib import admin

from .models import Benchmark, BenchmarkInstance, Software, CPU, GPU, Resource

admin.site.register(Benchmark)
admin.site.register(BenchmarkInstance)
admin.site.register(Software)
admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(Resource)