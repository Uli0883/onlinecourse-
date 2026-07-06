from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

class LessonInline(admin.TabularInline):          # <-- Ahora hereda de TabularInline
    model = Lesson
    extra = 1

class LessonAdmin(admin.ModelAdmin):              # <-- Este sí es ModelAdmin
    list_display = ['title', 'course', 'order']

class QuestionAdmin(admin.ModelAdmin):            # <-- Este sí es ModelAdmin
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'points']

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]      # <-- Usa las clases inline correctas
    list_display = ['name', 'instructor', 'pub_date']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'score', 'submission_date']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)