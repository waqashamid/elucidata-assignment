from django.conf.urls import url
from .api import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^upload$', UploadFile.as_view(), name='upload_file'),
    url(r'^process/task1$', FilterPCLPCPLasmogen.as_view(), name='perform_task'),
]
