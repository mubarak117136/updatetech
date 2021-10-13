from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from home import views

router = DefaultRouter()
router.register(r"invoices", views.InvoiceApi, basename="invoice_api")
router.register(r"items", views.ItemApi, basename="item_api")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/signup/", views.SignUpApi.as_view(), name="sign_up_api"),
    path("api/signin/", views.SignInApi.as_view(), name="sign_in_api"),
    path('api/public/', include(router.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)