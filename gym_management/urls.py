"""
URL configuration for gym_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from plans.views import PlansViewSet, FitnessClassesViewSet, ScheduledClassViewSet, AllReviewViewSet, ReviewViewset
from bookings.views import BookPlansViewSet, BookClassesViewSet, AttendenceViewSet, PaymentPlansViewSet, DashboardViewSet
from bookings.views import initiate_payment, payment_cancel, payment_success, payment_fail
from notification.views import NotificationViewSet
from message.views import ConvoViewset, MessageViewset
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
# from message.views import get_conversations

router = routers.DefaultRouter()
router.register("plans", PlansViewSet, basename="plans")
router.register("fitness_classes", FitnessClassesViewSet, basename="fitness_classes")
router.register("scheduled_classes", ScheduledClassViewSet, basename="scheduled_classes")
router.register("book_plans", BookPlansViewSet, basename="book_plans")
router.register("book_classes", BookClassesViewSet, basename="book_classes")
router.register("attendence", AttendenceViewSet, basename="attendence")
router.register("payment", PaymentPlansViewSet, basename="payment")
router.register("all_reviews", AllReviewViewSet, basename="all_reviews")
router.register("dashboard", DashboardViewSet, basename="dashboard")
router.register("notification", NotificationViewSet, basename="notification")
router.register("conversations", ConvoViewset, basename="conversations")
router.register("message", MessageViewset, basename="message")

fitness_cls_router = routers.NestedDefaultRouter(router, "fitness_classes", lookup='fitness_class')
fitness_cls_router.register('reviews', ReviewViewset, basename='fitness_class-reviews')



schema_view = get_schema_view(
   openapi.Info(
      title="MuscleGain - Gym management API",
      default_version='v1',
      description="API documentation for gym management system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tanvirulislam149@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
#    patterns=[
#         path('/', include(router.urls)),
#         path('/', include(fitness_cls_router.urls)),
#     ],
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('', include(fitness_cls_router.urls)),
    path("makePayment/initiate/", initiate_payment, name="initiate-payment"),
    path("makePayment/success/", payment_success, name="payment-success"),
    path("makePayment/fail/", payment_fail, name="payment-fail"),
    path("makePayment/cancel/", payment_cancel, name="payment-cancel"),
    # # # path("get_conversations/", get_conversations, name="get_conversations"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
