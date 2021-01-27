function getSimilarDocuments(formData) {
  function rowTemplate(obj) {
    return `<li class="table-row">
      <div class="col col-1" data-label="Title"><a href="${obj.url}">${obj.title}</a></div>
      <div class="col col-2" data-label="Customer Name">${obj.summary}</div>
    </li>`;
  };
  const url = 'https://asdsfunctionapp.azurewebsites.net/api/getSimilarDocuments';
  
  $('#results').css("visibility", "hidden");
  $('#processButton').attr('disabled', true);

  var title = $('#title').val();
  var data = { title: title };
  
  $.post(
    url, 
    JSON.stringify(data),
    function(data, status) {
      var result = data.result;
      var out = result.map(rowTemplate);
      $('#results').css("visibility", "visible");
      $('#results .responsive-table').append(out.join(''));
    }
  ).fail(function(err) { console.log(err); })
    .always(function() {
      $('#processButton').attr('disabled', false);
    });
}