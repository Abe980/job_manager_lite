from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Vacancy(models.Model):

    class StatusChoices(models.TextChoices):
        INTERESTING = 'interesting', 'Интересно'
        REQUEST_SENT = 'request_sent', 'Отправлен запрос'
        IN_PROGRESS = 'in_progress', 'В работе'
        REJECTED = 'rejected', 'Отказ'
        NOT_INTERESTING = 'not_interesting', 'Не интересно'


    title = models.CharField(max_length=200, verbose_name='Название вакансии')
    company = models.CharField(max_length=100, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    min_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Минимальная зарплата',
        null=True,
        blank=True
    )
    max_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Максимальная зарплата',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.INTERESTING,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    status_changed_at = models.DateTimeField(
        verbose_name='Дата изменения статуса',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Автор'
    )


    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} {self.company}'
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Vacancy.objects.get(pk=self.pk).status
            if old_status != self.status:
                self.status_changed_at = timezone.now()
        else:
            self.status_changed_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def status_display(self):
        return self.get_status_display()
        

class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Вакансия'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vacancy_comments',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

        def __str__(self):
            return f'Комментарий от {self.author} к вакансии {self.vacancy.title}'
