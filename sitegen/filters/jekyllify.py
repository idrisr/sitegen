def jekyllify(path):
    return '<img src="{{site.baseurl | append: "/assets/images/' + path + '"}}">'
