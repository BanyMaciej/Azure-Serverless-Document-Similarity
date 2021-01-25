function getSimilarDocuments(formData) {
  var title = $('#title').val();
  const url = 'https://asdsfunctionapp.azurewebsites.net/api/getSimilarDocuments';
  var data = { title: title };
  $('#processButton').attr('disabled', true);
  $.post(
    url, 
    JSON.stringify(data),
    function(data, status) {
      var result = data.result;
      var out = result.map(function (o) { 
        return '' + o.title + ' - ' + '<a href=' + o.url + '>LINK</a>' + ' - ' + o.summary;
      });
      $('#categoryResult').html(out.join("<br/>"));
    }
  ).fail(function(err) { console.log(err); })
    .always(function() {
      $('#processButton').attr('disabled', false);
    });
}