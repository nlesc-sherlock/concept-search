import vincent,pandas

def dict2bar(d):
    # function to convert a dictionary created by TermSuggester to vega readable json
    df = pandas.DataFrame(d.values(),index = d.keys())
    bar = vincent.Bar(df)
    bar.axis_titles(x='Terms', y='Scores')
    return bar.to_json()
