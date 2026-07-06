from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Course, Question, Choice, Submission

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse_app/course_list.html', {'courses': courses})

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse_app/course_details_bootstrap.html', {'course': course})

@login_required
def exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(course=course)
    return render(request, 'onlinecourse_app/exam.html', {
        'course': course,
        'questions': questions
    })

@login_required
def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        selected_choices = []

        # Recoger todas las opciones seleccionadas
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                try:
                    choice_id = int(value)
                    selected_choices.append(choice_id)
                except ValueError:
                    pass

        # Crear la Submission
        submission = Submission.objects.create(user=user, course=course, score=0)

        # Añadir las opciones seleccionadas
        for choice_id in selected_choices:
            try:
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
            except Choice.DoesNotExist:
                pass

        # Calcular el puntaje
        total_points = 0
        user_points = 0
        for question in Question.objects.filter(course=course):
            total_points += question.points
            # Opciones correctas de la pregunta
            correct_choices = Choice.objects.filter(question=question, is_correct=True)
            # Opciones que seleccionó el usuario para esta pregunta
            user_choices = submission.choices.filter(question=question)
            # Comparar conjuntos
            if set(correct_choices.values_list('id', flat=True)) == set(user_choices.values_list('id', flat=True)):
                user_points += question.points

        submission.score = user_points
        submission.save()

        # Redirigir a show_exam_result con course_id y submission_id
        return redirect('onlinecourse_app:show_exam_result', course_id=course_id, submission_id=submission.id)

    return redirect('onlinecourse_app:course_list')

@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
    questions = Question.objects.filter(course=course)

    # Preparar resultados por pregunta
    results = []
    total_score = 0
    possible_score = 0
    for question in questions:
        correct_choices = Choice.objects.filter(question=question, is_correct=True)
        user_choices = submission.choices.filter(question=question)
        is_correct = set(correct_choices.values_list('id', flat=True)) == set(user_choices.values_list('id', flat=True))
        points = question.points if is_correct else 0
        total_score += points
        possible_score += question.points
        results.append({
            'question': question,
            'correct_choices': correct_choices,
            'user_choices': user_choices,
            'is_correct': is_correct,
            'points': points,
            'possible_points': question.points
        })

    passed = submission.score >= possible_score * 0.7

    return render(request, 'onlinecourse_app/exam_result.html', {
        'course': course,
        'submission': submission,
        'results': results,
        'total_score': total_score,
        'possible_score': possible_score,
        'passed': passed
    })