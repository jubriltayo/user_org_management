from django.urls import path
from .views import *

urlpatterns = [
    path('api/organisations/', OrganisationListView.as_view(), name='organisations'),
    path('api/organisations/<int:orgId>', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations/', OrganisationCreateView.as_view(), name='create-organisation'),
    path('api/organisations/<int:orgId>/users/', AddUserToOrganisationView.as_view(), name='add-user-to-organisation')
]

