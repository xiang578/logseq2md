import html

class Post():

    def __init__(self, title, permalink, date, updated, tags, categories) -> None:
        self.title = title
        self.permalink = permalink
        self.date = date
        self.updated = updated
        self.tags = tags
        self.categories = categories

    def __str__(self):
        ret = []
        ret.append("---")
        ret.append("title: \"{}\"".format(html.escape(self.title)))
        ret.append("date: {}".format(self.date))
        ret.append("updated: {}".format(self.updated))
        ret.append("tags: [{}]".format(" ,".join(self.tags)))
        ret.append("categories: {}".format(self.categories))
        ret.append("toc: true")
        ret.append("mathjax: true")
        ret.append("permalink: {}.html".format(self.permalink))
        ret.append("---\n")
        return "\n".join(ret)