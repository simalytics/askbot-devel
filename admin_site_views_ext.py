from jinja2.ext import Extension

class AdminSiteViewsExtension(Extension):
    """Adds a `admin_site_views` tag to Jinja2 
    """
    tags = set(['admin_site_views'])

    def parse(self, parser):
        node = nodes.ExprStmt(lineno=next(parser.stream).lineno)
	node.node = parser.parse_tuple()
        return node

