$.getJSON( "http://localhost:9000/data/vega.json", function( data ) {
  console.log('got the data!');
  var spec = data;

  vg.parse.spec(spec, function(chart) {
  var view = chart({el:".chart"})
    .update();
  });

});
