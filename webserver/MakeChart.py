import operator,json

template = json.loads("""{
"width": 200,
"padding": "auto",
"data": [
  {
    "name": "raw",
    "values": [],
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
      "enter": {"width": {"value": 200}}
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
        "orient": "top",
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
        "grid": true
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
}
""")

def dict2bar(d):
    # function to convert a dictionary created by TermSuggester to vega readable json
    sortedlist=sorted(d.items(), key=operator.itemgetter(1),reverse=True)
    print sortedlist
    values = [{u'y':x[1],u'x':x[0]} for x in sortedlist]
    template['data'][0]['values'] = values
    return json.dumps(template,indent=2)
