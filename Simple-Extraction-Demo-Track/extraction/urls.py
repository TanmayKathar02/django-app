from django.urls import path, include

from extraction.views import ExtractionView, UploadDocumentView, get_tc_extract, ApplicationView, \
    apply_tc_to_data_extract, TCExtractListView

app_name = 'extraction'

urlpatterns = [
    path('create-extraction/<int:pk>/<str:email>/', ExtractionView.as_view(), name='create_extraction'),
    path('application/', ApplicationView.as_view(), name='application'),
    path('tc-extract-list/', TCExtractListView.as_view(), name='tc_extract_list'),
    path('get-tc-extract/<int:pk>/', get_tc_extract, name='get_tc_extract'),
    path('data-extract-tc/<int:pk>/', apply_tc_to_data_extract, name='tc_extract_data'),
    path('', UploadDocumentView.as_view(), name='upload_document'),

    # api urls
    path('api/v1/', include('extraction.api.urls')),
]
