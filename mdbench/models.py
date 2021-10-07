# Apply changes:
# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py runserver
from django.db import models
import uuid 

class Software(models.Model):
    name = models.CharField(max_length=100, help_text='Enter a software name (e.g. NAMD)')
    module = models.CharField(max_length=100, help_text='Enter a module name') 
    module_version = models.CharField(max_length=100, help_text='Enter a module version')    
    toolchain = models.CharField(max_length=100, help_text='Enter a toolchain name') 
    toolchain_version = models.CharField(max_length=100, help_text='Enter a toolchain version') 
    instruction_set = models.CharField(max_length=100, help_text='Enter CPU instruction set (avx2/avx512)')  
    def __str__(self):
        return f'{self.name}({self.module}/{self.module_version})-\
            {self.toolchain}-{self.toolchain_version}-{self.instruction_set}'    

class Resource(models.Model):
    ncpu = models.IntegerField()
    ntasks = models.IntegerField()
    ngpu = models.IntegerField()
    nvlink = models.BooleanField() 
    def __str__(self):
        return f'Tasks={self.ntasks}, CpusPerTask={self.ncpu}, GPUs={self.ngpu},  NVLink={self.nvlink}'

class Benchmark(models.Model):
    name = models.CharField(max_length=100, help_text='Enter a benchmark name')
    natoms = models.IntegerField()
    description = models.TextField()
    def __str__(self):
        return f'{self.name}, {self.natoms} particles'

class CPU(models.Model):
    name = models.CharField(max_length=100, help_text='Enter a CPU name (e.g. Xeon)')
    model = models.CharField(max_length=100, help_text='Enter a CPU model (e.g. E5-2683 v4)')
    codename = models.CharField(max_length=100, help_text='Enter a CPU codename (e.g. Broadwell)')
    frequency = models.FloatField()
    def __str__(self):
        return f'{self.name} {self.model} ({self.codename})'

class GPU(models.Model):
    name = models.CharField(max_length=100, help_text='Enter a GPU name (e.g. Tesla)')
    model = models.CharField(max_length=100, help_text='Enter a GPU model (e.g. V100)') 
    def __str__(self):
        return f'{self.name} {self.model}'
    
class BenchmarkInstance(models.Model):
    benchmark = models.ForeignKey('Benchmark', on_delete=models.RESTRICT, null=True)
    software = models.ForeignKey('Software', on_delete=models.RESTRICT, null=True) 
    cpu = models.ForeignKey('CPU', on_delete=models.RESTRICT, null=True)
    gpu = models.ForeignKey('GPU', on_delete=models.RESTRICT, blank=True, null=True)
    resource = models.ForeignKey('Resource', on_delete=models.RESTRICT, null=True)   
    rate = models.FloatField(help_text='Simulation speed, ns/day')
    efficiency = models.FloatField(help_text='CPU efficiency, %')
    submission = models.TextField()
    def __str__(self):
        return f'{self.id}, {self.benchmark}'
