import uuid
from django.db import models

class Game(models.Model):
    DIFFICULTY_CHOICES = [
        (1, "Easy"),
        (2, "Medium"),
        (3, "Hard"),
        (4, "Expert"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    time_started = models.DateTimeField(auto_now_add=True)
    time_ended = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.get_difficulty_display()}"

class Question(models.Model):
    game = models.ForeignKey(Game, related_name='questions', on_delete=models.CASCADE)
    equation = models.CharField(max_length=255)
    answer = models.FloatField()
    user_answer = models.FloatField(null=True, blank=True)
    time_asked = models.DateTimeField(auto_now_add=True)
    time_answered = models.DateTimeField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def time_taken(self):
        if self.time_answered and self.time_asked:
            delta = self.time_answered - self.time_asked
            return round(delta.total_seconds(), 2)
        return None

    def __str__(self):
        return f"Q: {self.equation} | A: {self.answer}"
