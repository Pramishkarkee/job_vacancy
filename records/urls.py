from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    about,
    applicantUpdate,
    list_applicant_details,
    list_provider_details,
    providerUpdate,
    userSignup,
    applicantSignup,
    providerSignup,
)

urlpatterns = [
    path("about/", about, name="about"),
    path("signup/<str:profile_type>/", userSignup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("applicantregister/", applicantSignup, name="applicant_registration"),
    path(
        "applicant/profile/update/",
        applicantUpdate,
        name="applicant_update",
    ),
    path("providerregister/", providerSignup, name="provider_registration"),
    path(
        "provider/profile/update/",
        providerUpdate,
        name="provider_update",
    ),
    path(
        "applicant/<slug:applicant_id>/details/",
        list_applicant_details,
        name="list_applicant_details",
    ),
    path(
        "provider/<slug:provider_id>/details",
        list_provider_details,
        name="list_provider_details",
    ),
]
