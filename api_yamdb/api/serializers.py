from rest_framework import serializers

from reviews.models import Comment, Review, User


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Review

    def get_score(self, obj):
        score = obj.score.aggregate(sum('score'))['score__sum']
        if score:
            return score / obj.score.count()
        return 0


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
