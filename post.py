import html

class Post():

    def __init__(self, title, date, updated, tags, categories) -> None:
        self.tilte = title
        self.date = date
        self.updated = updated
        self.tags = tags
        self.categories = categories

    def __str__(self):
        ret = []
        ret.append("---")
        ret.append("tilte: \"{}\"".format(html.escape(self.tilte)))
        ret.append("date: {}".format(self.date))
        ret.append("updated: {}".format(self.updated))
        ret.append("tags: [{}]".format(" ,".join(self.tags)))
        ret.append("categories: {}".format(self.categories))
        ret.append("toc: true")
        ret.append("mathjax: true")
        ret.append("---\n\n")
        return "\n".join(ret)