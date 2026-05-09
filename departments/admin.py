from django.contrib import admin
from .models import Department, Program

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'code')
    raw_id_fields = ('department',) # Allows searching for department by ID
