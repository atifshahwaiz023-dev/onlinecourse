from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        enrollment = Enrollment.objects.create(user=request.user, course=course, mode='audit')

    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)
        choice_ids = request.POST.getlist('choice')
        for choice_id in choice_ids:
            choice = Choice.objects.get(pk=int(choice_id))
            submission.choices.add(choice)
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    total_score = 0
    questions = course.question_set.all()
    for question in questions:
        selected_choices = submission.choices.filter(question=question)
        correct_choices = question.choice_set.filter(is_correct=True)

        selected_ids = set(selected_choices.values_list('id', flat=True))
        correct_ids = set(correct_choices.values_list('id', flat=True))

        if selected_ids == correct_ids and len(selected_ids) > 0:
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'grade': total_score
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
