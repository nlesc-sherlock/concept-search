import vincent

def dict2bar(d):
    # function to convert a dictionary created by TermSuggester to vega readable json
    bar = vincent.Bar(d.values())
    return bar.to_json()
