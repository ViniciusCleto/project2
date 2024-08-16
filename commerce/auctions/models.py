from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=25)

    def __str__(self):
        return self.categoryName


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=360)
    imageUrl = models.CharField(max_length=360)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder.username} - {self.listing.title} - {self.bidAmount}"


class Comment(models.Model):
    commentAuthor = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingComment")
    comment = models.CharField(max_length=264)
    createdAt = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"{self.commentAuthor}'s comment on {self.listing}"
