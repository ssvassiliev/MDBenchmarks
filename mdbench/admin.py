from django.contrib import admin

from .models import SimulationInput, Benchmark, BenchmarkInstance, SerialBenchmarkInstance, Software, CPU, GPU, Resource, Site

admin.site.register(Benchmark)
admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(Site)
admin.site.register(SimulationInput)

@admin.register(SerialBenchmarkInstance)
class SerialBenchmarkInstanceAdmin(admin.ModelAdmin):
    autocomplete_fields=("software",)
    search_fields=("software__name",)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    search_fields=("ntasks__exact","ncpu__exact")
    list_filter = ("ncpu","ntasks", "ngpu")


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("name","module","module_version","toolchain","instruction_set")
    list_filter = ("instruction_set",)
    search_fields=("name",)

@admin.register(BenchmarkInstance)
class BenchmarkInstanceAdmin(admin.ModelAdmin):
    list_filter = ("software__module","software__instruction_set")
    autocomplete_fields=("resource", "serial", "software")
    search_fields=("resource",)