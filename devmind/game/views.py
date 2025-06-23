from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Game, Question
from .serializers import (
    AnswerSerializer,
    StartGameSerializer,
    SubmitAnswerSerializer,
    QuestionHistorySerializer
)
import random

def generate_question(difficulty):
    operands_count = difficulty + 1
    if difficulty == 1:
        numbers = [random.randint(1, 9) for _ in range(operands_count)]
    elif difficulty == 2:
        numbers = [random.randint(10, 99) for _ in range(operands_count)]
    elif difficulty == 3:
        numbers = [random.randint(100, 999) for _ in range(operands_count)]
    else:
        numbers = [random.randint(1000, 9999) for _ in range(operands_count)]

    ops = random.choices(['+', '-', '*', '/'], k=operands_count - 1)
    equation = f"{numbers[0]}"
    result = float(numbers[0])
    for i in range(1, operands_count):
        op = ops[i - 1]
        equation += f" {op} {numbers[i]}"
        if op == '+':
            result += numbers[i]
        elif op == '-':
            result -= numbers[i]
        elif op == '*':
            result *= numbers[i]
        elif op == '/':
            result /= numbers[i]

    return equation, round(result, 2)


@api_view(['POST'])
def start_game(request):
    serializer = StartGameSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        difficulty = serializer.validated_data['difficulty']
        game = Game.objects.create(name=name, difficulty=difficulty)

        equation, answer = generate_question(difficulty)
        Question.objects.create(game=game, equation=equation, answer=answer)

        return Response({
            "message": f"Hello {name}, find your submit API URL below",
            "submit_url": f"/game/{game.id}/submit",
            "question": equation,
            "time_started": game.time_started
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def submit_answer(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({"error": "Game not found."}, status=404)

    # 🚫 Prevent answer after game ends
    if game.time_ended:
        return Response({"error": "Game has already ended."}, status=400)

    # ✅ Validate input using AnswerSerializer
    serializer = AnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    user_answer = serializer.validated_data['answer']

    # Find the latest unanswered question
    try:
        question = game.questions.filter(answered_at__isnull=True).earliest("created_at")
    except:
        return Response({"error": "No active question."}, status=400)

    # Evaluate correct answer
    try:
        correct_answer = eval(question.equation)
    except ZeroDivisionError:
        correct_answer = None

    is_correct = abs(user_answer - correct_answer) < 0.01 if correct_answer is not None else False

    question.answered_at = timezone.now()
    question.user_answer = user_answer
    question.is_correct = is_correct
    question.save()

    # Prepare next question
    next_eq, correct = generate_question(game.difficulty)
    next_question = Question.objects.create(game=game, equation=next_eq)

    correct_count = game.questions.filter(is_correct=True).count()
    total_attempted = game.questions.exclude(answered_at__isnull=True).count()

    return Response({
        "result": f"{'Good job' if is_correct else 'Sorry'} {game.name}, your answer is {'correct' if is_correct else 'incorrect'}.",
        "time_taken": (question.answered_at - question.created_at).total_seconds(),
        "next_question": {
            "submit_url": f"/game/{game.id}/submit",
            "question": next_question.equation
        },
        "current_score": f"{correct_count} / {total_attempted}"
    })



@api_view(['GET'])
def end_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.time_ended = timezone.now()
    game.save()

    questions = game.questions.all()
    total = questions.count()
    correct = questions.filter(is_correct=True).count()
    best = min(
        [q for q in questions if q.time_taken() is not None],
        key=lambda q: q.time_taken(),
        default=None
    )

    return Response({
        "name": game.name,
        "difficulty": game.difficulty,
        "current_score": f"{correct}/{total}",
        "total_time_spent": round(sum(q.time_taken() or 0 for q in questions), 2),
        "best_score": {
            "question": best.equation,
            "answer": best.user_answer,
            "time_taken": best.time_taken()
        } if best else None,
        "history": QuestionHistorySerializer(questions, many=True).data
    })
