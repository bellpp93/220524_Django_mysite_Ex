from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
from .forms import QuestionForm

# Create your views here.
def index(request):
    """
        pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')  # -붙으면 내림차순 없으면 오름차순
    context = {'question_list': question_list}  # 딕셔너리의 {키 : 값}
    return render(request, 'pybo/question_list.html', context)  # 인자 값 3개

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)  # get_object_or_404 추가 후 아래처럼 수정
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
        pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)

def question_create(request):
    """
        pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():  # 폼이 유효하다면
            question = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴받는다.
            question.create_date = timezone.now()  # 실제 저장을 위해 작성일시를 설정한다.
            question.save()  # 데이터를 실제로 저장한다.
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)