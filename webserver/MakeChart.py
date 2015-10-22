import vincent,pandas,operator
from vincent import AxisProperties, PropertySet, ValueRef

def dict2bar(d):
    # function to convert a dictionary created by TermSuggester to vega readable json
    sortedlist=sorted(d.items(), key=operator.itemgetter(1),reverse=True)
    i = [x[0] for x in sortedlist]
    v = [x[1] for x in sortedlist]
    df = pandas.DataFrame(v,i)
    bar = vincent.Bar(df)
    vert2horiz(bar)
    bar.axis_titles(x='Terms', y='Scores')
    ax = AxisProperties(labels = PropertySet(angle=ValueRef(value=-90)))
    bar.axes[0].properties=ax
    bar.axes[0].properties
    bar.height=350
    return bar.to_json()
    
def vert2horiz(bar):
    print bar.grammar()
