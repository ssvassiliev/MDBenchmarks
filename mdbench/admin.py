from django.contrib import admin

from .models import SimulationInput, Benchmark, BenchmarkInstance, SerialBenchmarkInstance, Software, CPU, GPU, Resource, Site

admin.site.register(Benchmark)
admin.site.register(BenchmarkInstance)
admin.site.register(SerialBenchmarkInstance)
admin.site.register(Software)
admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(Resource)
admin.site.register(Site)
admin.site.register(SimulationInput)