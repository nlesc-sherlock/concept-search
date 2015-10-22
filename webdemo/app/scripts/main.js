$.ajax({
  dataType: "json",
  url: "http://127.0.0.1:5000/",
  method: "get",
  xhrFields: {
    withCredentials: true
  },
  success: function(data) {
    console.log('got the data!');
    console.log(data);
    $.each(data, function( key, method ){
      var html = "<div class=\"checkbox-inline\">" +
                 "   <label>" +
                 "     <input type=\"checkbox\" name=\"methods[]\" value=\"" +
                 key + "\" checked> " + method[0] + "  </label>";
      $(html).appendTo( $("#qem") );
    });
  },
  error: function(xhr, ajaxOptions, thrownError) {
    console.log(xhr.status);
    console.log(thrownError);
  }
});

$("#search").submit(function(e) {
  console.log('form submitted');
  e.preventDefault();

  console.log($("#search").serialize());

  $.ajax({
    dataType: "json",
    url: "http://127.0.0.1:5000/suggester",
    method: "get",
    data: $("#search").serialize(),
    xhrFields: {
      withCredentials: true
    },
    success: function(data) {
      console.log('got the data!');
      console.log(data);
      console.log(JSON.stringify(data));

      displayChart(data);

    },
    error: function(xhr, ajaxOptions, thrownError) {
      console.log(xhr.status);
      console.log(thrownError);
    }
  });
});

$('input[type=radio]').on('change', function() {
  console.log('changed radio');
  var term = $( "#term" ).val();
  if(term !== ''){
    $("#search").submit();
  }
});

function displayChart(json_data) {
  vg.parse.spec(json_data, function(chart) {
    var view = chart({
        el: ".chart"
      })
      .update();
  });
}
