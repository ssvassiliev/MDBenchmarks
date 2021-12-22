from django.contrib import admin

from .models import SimulationInput, Benchmark, BenchmarkInstance, SerialBenchmarkInstance, Software, CPU, GPU, Resource, Site

admin.site.register(Benchmark)
admin.site.register(CPU)

admin.site.register(GPU)
admin.site.register(Site)
admin.site.register(SimulationInput)

@admin.register(SerialBenchmarkInstance)
class SerialBenchmarkInstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    autocomplete_fields=("software",)
    search_fields=("software__name",)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ("id", "ncpu", "ngpu", "nvlink")  
    list_display = ("id", "ntasks", "ncpu", "ngpu", "nnodes", "nvlink")  
    search_fields=("label", "nvlink")
    list_filter = ("ncpu", "ntasks", "ngpu")

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ("id","name","module","module_version","toolchain","instruction_set")
    list_filter = ("instruction_set","toolchain", "module_version")
    search_fields=("name",)

@admin.register(BenchmarkInstance)
class BenchmarkInstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ("id", "benchmark", "software","site")
    list_filter = ("software__module","software__instruction_set")
    autocomplete_fields=("resource", "serial", "software")
    search_fields=("software__name",)