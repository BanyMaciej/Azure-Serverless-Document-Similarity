function getSimilarDocuments(formData) {
  function rowTemplate(obj) {
    return `<li class="table-row">
      <div class="col col-1" data-label="Title"><a href="${obj.url}">${obj.title}</a></div>
      <div class="col col-2" data-label="Customer Name">${obj.summary}</div>
    </li>`;
  };
  const headerHtml = '<li class="table-header"><div class="col col-1">Title</div><div class="col col-2">Summary</div></li>';

  const url = 'http://localhost:7071/api/getSimilarDocuments';
  
  $('#results').css("visibility", "hidden");
  $('.resultsSpinner').css("display", "inline-block");
  $('#processButton').attr('disabled', true);

  var title = $('#title').val();
  var data = { title: title };

  $('#results .responsive-table').html("");
  
  $.post(
    url, 
    JSON.stringify(data),
    function(data, status) {
      var result = data.result;
      var out = result.map(rowTemplate);
      $('#results').css("visibility", "visible");
      $('#results .responsive-table').append(headerHtml + out.join(''));
    }
  ).fail(function(err) { console.log(err); })
    .always(function() {
      $('.resultsSpinner').css("display", "none");
      $('#processButton').attr('disabled', false);
    });
}