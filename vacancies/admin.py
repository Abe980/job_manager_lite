from django.contrib import admin
from .models import Vacancy, Comment


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'status', 'author', 'created_at', 'get_updated_at')
    list_filter = ('status', 'created_at', 'company')
    search_fields = ('title', 'company', 'description')
    readonly_fields = ('created_at', 'get_updated_at', 'status_changed_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'company', 'description', 'author')
        }),
        ('Зарплата', {
            'fields': ('min_salary', 'max_salary'),
            'classes': ('collapse',)
        }),
        ('Статус и даты', {
            'fields': ('status', 'status_changed_at', 'created_at', 'get_updated_at')
        }),
    )

    def get_updated_at(self, obj):
        return obj.updated_at
    get_updated_at.short_description = 'Дата последнего изменения'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs['choices'] = Vacancy.StatusChoices.choices
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'author', 'created_at', 'short_text')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'vacancy__title')

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Текст'