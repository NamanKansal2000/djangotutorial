from typing import Optional

from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


# Create your views here.

# def index(request):
#     return HttpResponse("Hello world! You're at polls index...")

# def index(request):
#     latest_questions_list = Question.objects.order_by("-pub_date")[:5]
#     # output = [", ".join([q.question_text for q in latest_questions_list])]
#     # return HttpResponse(output)

#     # template = loader.get_template("polls/index.html")
#     # context = {"latest_questions_list": latest_questions_list}
#     # return HttpResponse(template.render(context=context))

#     context = {"latest_questions_list": latest_questions_list}
#     print(context)
#     return render(request, "polls/index.html", context=context)

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exits")
#     # return render(request, "polls/details.html", {"question": question})

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/details.html", context={"question": question})

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

    def get_queryset(self) -> QuerySet:
        return Question.objects.filter(pub_date__lte=timezone.now())

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/details.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
