from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, Listing, Watchlist, Bid, Comment


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html", {
        "listings": activeListings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def showCategories(request):
    allCategories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": allCategories
    })


def categoryListings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, isActive=True)
    return render(request, "auctions/category-listings.html", {
        "listings": listings,
        "category": category,
    })


def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imgUrl = request.POST["imgUrl"]
        price = request.POST["price"]
        category = request.POST["category"]
        categoryData = Category.objects.get(categoryName=category)
        currentUser = request.user
        newListing = Listing(
            title = title,
            description = description,
            imageUrl = imgUrl,
            price = float(price),
            category = categoryData,
            owner = currentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))


def listingDetail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    isOwner = request.user == listing.owner
    inWatchlist = False
    if request.user.is_authenticated and not isOwner:
        inWatchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    
    highestBid = Bid.objects.filter(listing=listing).order_by('-bidAmount').first()
    isWinner = highestBid and highestBid.bidder == request.user

    allComments = Comment.objects.filter(listing=listing)

    if request.method == "POST":
        if 'placeBid' in request.POST:
            bidAmount = float(request.POST['bidAmount'])
            if bidAmount >= listing.price and (highestBid is None or bidAmount > highestBid.bidAmount):
                newBid = Bid(bidder=request.user, listing=listing, bidAmount=bidAmount)
                newBid.save()
                listing.price = bidAmount
                listing.save()
                return HttpResponseRedirect(reverse('listing-detail', args=[listing_id]))
            else:
                return render(request, "auctions/listing-detail.html", {
                    "listing": listing,
                    "isOwner": isOwner,
                    "inWatchlist": inWatchlist,
                    "highestBid": highestBid,
                    "msg": "Bid must be at least as large as the starting bid and greater than any other bids.",
                    "isWinner": isWinner,
                    "allComments": allComments
                })
        elif 'closeAuction' in request.POST and isOwner:
            listing.isActive = False
            listing.save()
            return HttpResponseRedirect(reverse('listing-detail', args=[listing_id]))
        elif 'addToWatchlist' in request.POST:
            watchlistItem = Watchlist(user=request.user, listing=listing)
            watchlistItem.save()
            return HttpResponseRedirect(reverse('listing-detail', args=[listing_id]))
        elif 'removeFromWatchlist' in request.POST:
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            return HttpResponseRedirect(reverse('listing-detail', args=[listing_id]))

    return render(request, "auctions/listing-detail.html", {
        "listing": listing,
        "isOwner": isOwner,
        "inWatchlist": inWatchlist,
        "highestBid": highestBid,
        "isWinner": isWinner,
        "allComments": allComments
    })


@login_required
def addComment(request, id):
    currentUser = request.user
    currentListing = Listing.objects.get(pk=id)
    comment = request.POST['newComment']

    newComment = Comment(
        commentAuthor = currentUser,
        listing = currentListing,
        comment = comment
    )
    newComment.save()

    return HttpResponseRedirect(reverse("listing-detail", args=(id,)))


@login_required
def watchlist(request):
    userWatchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": userWatchlist
    })


