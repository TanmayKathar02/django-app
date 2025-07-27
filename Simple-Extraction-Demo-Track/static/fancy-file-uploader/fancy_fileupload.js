let token = document.getElementsByName('csrfmiddlewaretoken').value
$(function () {
  $('#multiple-documents-upload').FancyFileUpload({
    'url': '/client-portal/document-upload/',
    params: {
      action: 'fileuploader',
      "csrfmiddlewaretoken": token,
    },
  });
  $('#myTable').DataTable();
});