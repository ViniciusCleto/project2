from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.createListing, name="create"),
    path("categories/", views.showCategories, name="categories"),
    path("category/<int:category_id>/", views.categoryListings, name="category-listings"),
    path("listing/<int:listing_id>/", views.listingDetail, name="listing-detail"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("add-comment/<int:id>", views.addComment, name="add-comment"),
]
