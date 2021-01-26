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
        return '<tr><td><a href="' + o.url + '">' + o.title + '</a></td><td>' + o.summary + '</td></tr>';
      });
      $('#results tbody').html(out.join(''));
    }
  ).fail(function(err) { console.log(err); })
    .always(function() {
      $('#processButton').attr('disabled', false);
    });
}