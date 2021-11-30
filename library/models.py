from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=150)
    book_id = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='books')

    def get_average_rating(self):
        ratings = Rating.objects.filter(book=self)
        if ratings:
            average = sum([r.rating for r in ratings]) / len(ratings)
            return round(average, 2)
        return 0

    def __str__(self):
        return f"{' '.join([i.capitalize() for i in self.title.split()])} - [ {self.book_id} ]"

class Order(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    book = models.ForeignKey(Book, related_name="orders", on_delete=models.CASCADE)
    dateOfIssue = models.DateField(auto_now_add=True)
    returnDate = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        if self.returnDate:
            if not self.is_returned:
                self.is_returned = True
            if not self.book.is_available:
                self.book.is_available = True
    
        return f'{self.student.last_name} {self.student.username[0].upper()}. - {self.book}'

class Comment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(choices=((1,1), (2,2), (3,3), (4,4), (5,5)))

    def __str__(self):
        return str(self.rating)