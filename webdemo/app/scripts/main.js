var spec = { // comes from http://stackoverflow.com/questions/31393949/vega-horizontal-bar-charts
"width": 200,
"height": 210,
"padding": "auto",
"data": [
  {
    "name": "raw",
    "values": [
      {"x": "A","y": 91},
      {"x": "B","y": 87},
      {"x": "C","y": 81},
      {"x": "D","y": 55},
      {"x": "E","y": 53},
      {"x": "F","y": 52},
      {"x": "G","y": 43},
      {"x": "H","y": 28},
      {"x": "I","y": 19}
    ],
    "format": {"parse": {"y": "number"}},
    "transform": [{"type": "filter","test": "(d.data.y!==null)"}]
  }
],
"scales": [],
"marks": [
  {
    "_name": "cell",
    "type": "group",
    "properties": {
      "enter": {"width": {"value": 200},"height": {"value": 210}}
    },
    "scales": [
      {
        "name": "x",
        "type": "linear",
        "domain": {"data": "raw","field": "data.y"},
        "range": [0,200],
        "zero": true,
        "reverse": false,
        "round": true,
        "nice": true
      },
      {
        "name": "y",
        "type": "ordinal",
        "domain": {"data": "raw","field": "data.x"},
        "sort": true,
        "range": [0,210],
        "bandWidth": 21,
        "round": true,
        "nice": true,
        "points": true,
        "padding": 1
      }
    ],
    "axes": [
      {
        "type": "x",
        "scale": "x",
        "properties": {
          "grid": {
            "stroke": {"value": "#000000"},
            "opacity": {"value": 0.08}
          }
        },
        "layer": "back",
        "format": "",
        "ticks": 5,
        "titleOffset": 38,
        "grid": true,
        "title": "score"
      },
      {
        "type": "y",
        "scale": "y",
        "properties": {
          "labels": {"text": {"template": "{{data | truncate:25}}"}},
          "grid": {
            "stroke": {"value": "#000000"},
            "opacity": {"value": 0.08}
          }
        },
        "layer": "back",
        "titleOffset": 28,
        "grid": true,
        "title": "term suggestions"
      }
    ],
    "marks": [
      {
        "type": "rect",
        "from": {"data": "raw"},
        "properties": {
          "enter": {
            "x": {"scale": "x","field": "data.y"},
            "x2": {"value": 0},
            "yc": {"scale": "y","field": "data.x"},
            "height": {"value": 21,"offset": -1},
            "fill": {"value": "#4682b4"}
          },
          "update": {
            "x": {"scale": "x","field": "data.y"},
            "x2": {"value": 0},
            "yc": {"scale": "y","field": "data.x"},
            "height": {"value": 21,"offset": -1},
            "fill": {"value": "#4682b4"}
          }
        }
      }
    ],
    "legends": []
  }
]
};

vg.parse.spec(spec, function(chart) {
var view = chart({el:".chart"})
  .update();
});
