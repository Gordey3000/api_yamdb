from django.core.validators import MaxValueValidator, MinValueValidator

MIN_SCORE = 1
MAX_SCORE = 10

min_score_validator = MinValueValidator(MIN_SCORE)
max_score_validator = MaxValueValidator(MAX_SCORE)
