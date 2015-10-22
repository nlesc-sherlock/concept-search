import vincent

def dict2bar(d):
    bar = vincent.Bar(d.keys())
    return bar.to_json()
