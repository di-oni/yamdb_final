import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from titles.models import Category, Comment, Genre, Review, Title

from .models import Code

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    """Serializer for incoming registration email."""
    email = serializers.EmailField()


class CodeSerializer(serializers.ModelSerializer):
    """Serializer for code model with default
       functional of ModelSerializer."""
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=Code.objects.all()),
        ]
    )
    confirmation_code = serializers.CharField(max_length=32)

    class Meta:
        fields = '__all__'
        model = Code


class CheckEmailCodeSerializer(serializers.ModelSerializer):
    """Serializer for checking email and code exist in code model
       with default functional of ModelSerializer."""
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=32)

    class Meta:
        fields = '__all__'
        model = Code

    def validate(self, data):
        """
        Checking email - code combination is exists and code is correct.
        """

        code_obj = get_object_or_404(Code, email=data['email'])
        incoming_code = data['confirmation_code']
        true_code = code_obj.confirmation_code
        if incoming_code != true_code:
            raise serializers.ValidationError(
                'Confirmation code is not valide'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model with default
       functional of ModelSerializer."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class UserTokenSerializer(serializers.ModelSerializer):
    """Serializer for creating a user by token with default
       functional of ModelSerializer."""
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class MeSerializer(serializers.ModelSerializer):
    """Serializer to change your data with default
       functional of ModelSerializer."""
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review model with default
       functional of ModelSerializer."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        author = self.context['request'].user
        logging.debug(
            f'ReviewSerializer. Validate. Checking author - {author}'
        )
        title_id = self.context['request']. \
            parser_context['kwargs']['title_id']
        logging.debug(
            f'ReviewSerializer. Validate. Checking title id - {title_id}'
        )
        title = get_object_or_404(Title, id=title_id)
        review_exists = Review.objects.filter(
            author=author,
            title=title
        ).exists()
        if review_exists:
            error_message = 'You already have a review for this work.'
            raise serializers.ValidationError(error_message)
        return data

    class Meta:
        model = Review
        read_only_fields = ('title',)
        fields = '__all__'


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer for update review model with default
       functional of ModelSerializer."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        read_only_fields = ('title',)
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category model with default
       functional of ModelSerializer."""
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre model with default
       functional of ModelSerializer."""
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleCreateSerializer(serializers.ModelSerializer):
    """Serializer for title model when creating with default
       functional of ModelSerializer."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    rating = serializers.IntegerField(read_only=True,)

    class Meta:
        model = Title
        fields = '__all__'


class TitleListSerializer(serializers.ModelSerializer):
    """Serializer for title model when we send a list of
       objects with default functional of ModelSerializer."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True,)

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment model with default
       functional of ModelSerializer."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment
