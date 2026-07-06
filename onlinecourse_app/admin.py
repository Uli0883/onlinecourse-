from django.contrib import admin
from .models import Instructor, Learner, Course, Lesson, Question, Choice, Submission

# Inlines
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 2
    fields = ['title', 'description', 'order']
    ordering = ['order']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2
    fields = ['question_text', 'points']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    fields = ['choice_text', 'is_correct']

# Administradores
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user']
    search_fields = ['full_name']

class LearnerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user']
    search_fields = ['full_name']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'points']
    list_filter = ['course']

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ['name', 'instructor', 'pub_date']
    search_fields = ['name', 'instructor__full_name']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'score', 'submission_date']
    list_filter = ['course', 'user']

# Registro
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)