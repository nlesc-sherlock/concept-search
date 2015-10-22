import vincent,pandas,operator

def dict2bar(d):
    # function to convert a dictionary created by TermSuggester to vega readable json
    sortedlist=sorted(d.items(), key=operator.itemgetter(1),reverse=True)
    i = [x[0] for x in sortedlist]
    v = [x[1] for x in sortedlist]
    df = pandas.DataFrame(v,i)
    bar = vincent.Bar(df)
    bar.axis_titles(x='Terms', y='Scores')
    return bar.to_json()
