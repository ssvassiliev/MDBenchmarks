from django.contrib import admin

from .models import SimulationInput, Benchmark, BenchmarkInstance, SerialBenchmarkInstance, Software, CPU, GPU, Resource, Site

admin.site.register(Benchmark)
admin.site.register(SerialBenchmarkInstance)
admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(Resource)
admin.site.register(Site)
admin.site.register(SimulationInput)

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("module","module_version","toolchain")
    list_filter = ("instruction_set",)


@admin.register(BenchmarkInstance)
class BenchmarkInstanceAdmin(admin.ModelAdmin):
    list_display = ("software", "resource")
    list_filter = ("software__module","software__instruction_set")
