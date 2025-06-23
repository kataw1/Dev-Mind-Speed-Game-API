from rest_framework import serializers
from .models import Game, Question

class StartGameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    difficulty = serializers.ChoiceField(choices=[(i, i) for i in range(1, 5)])


class SubmitAnswerSerializer(serializers.Serializer):
    answer = serializers.FloatField()


class QuestionHistorySerializer(serializers.ModelSerializer):
    time_taken = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['equation', 'answer', 'user_answer', 'is_correct', 'time_taken']

    def get_time_taken(self, obj):
        return obj.time_taken()

class AnswerSerializer(serializers.Serializer):
    answer = serializers.FloatField()
