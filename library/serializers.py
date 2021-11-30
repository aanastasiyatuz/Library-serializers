from rest_framework import serializers

from .models import * 


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = Book.objects.get(id=representation.get('id')).get_average_rating()


        action = self.context.get('action')
        if action == 'retrieve':
            comments = CommentSerializer(instance.comments.all(), many=True).data
            representation['comments'] = comments

        elif action == 'list':
            comments = CommentSerializer(instance.comments.all(), many=True).data
            if not comments:
                representation['comments'] = []
            else:
                representation['comments'] = comments[0]
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        image = request.FILES
        book = Book.objects.create(image=image, **validated_data)
        return book


class CommentSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        book = validated_data.get('book')
        comment = Comment.objects.create(student=request.user, book=book, **validated_data)
        return comment


class OrderSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.email')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        book = validated_data.get('book')
        comment = Order.objects.create(student=request.user, book=book, **validated_data)
        return comment


class RatingSerializer(serializers.ModelSerializer):
	student = serializers.ReadOnlyField(source='student.username')

	class Meta:
		model = Rating
		fields = '__all__'

	def create(self, validated_data):
		request = self.context.get('request')
		user = request.user
		book = validated_data.get('book')

		if Rating.objects.filter(student=user, book=book):
			rating = Rating.objects.get(student=user, book=book)
			rating.delete()

		rating = Rating.objects.create(student=request.user, book=book, **validated_data)
		return rating
