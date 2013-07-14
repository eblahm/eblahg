import webapp2
import re
import render
import utility
import random
import pictures
from google.appengine.ext import db
from google.appengine.api import search

def full_text_query(query_string, limit=10, cursor=None, s_expression="score"):
    score_desc = search.SortExpression(
        expression="_score",
        direction=search.SortExpression.DESCENDING,
        default_value=0,
        )
    sorts = {"score":score_desc}
    #    try:

    # Sort up to 1000 matching results by subject in descending order
    sort = search.SortOptions(expressions=[sorts[s_expression]], limit=1000)
    # Set query options
    qs = query_string.decode('utf-8', 'replace')
    snip_expression = 'snippet("%s", body, 300, 10)' % (qs)
    options = search.QueryOptions(
        limit=limit,  # the number of results to return
        cursor=cursor,
        sort_options=sort,
        #        snippeted_fields=['title','body'],
        returned_expressions=[search.FieldExpression(name='snippet',
                                                     expression=snip_expression)]
    )
    query = search.Query(query_string=qs, options=options)
    index = search.Index(name="articles")
    doc_sresults = index.search(query)
    return doc_sresults

class term(webapp2.RequestHandler):
    def get(self):
        v = {}
        term = self.request.get("term")
        text_query = full_text_query(term)
        posts = []
        for i in text_query:
            rec = db.get(i.doc_id)
            if rec == None:
                continue
            rec.snip = ""
            for e in i.expressions:
                regex = "<b>(%s)<\/b>" % (term)
                try:
                    this_term = re.search(regex, e.value, flags=re.IGNORECASE).group(1)
                except:
                    this_term = term
                highlighted = '<span class="highlight">%s</span>' % (this_term)
                this_snip = e.value.replace("<br", "")
                this_snip = utility.strip_tags(this_snip)
                rec.snip += re.sub(term, highlighted, this_snip, count=10, flags=re.IGNORECASE)
            posts.append(rec)

        v = {"results":posts}
        v['title'] = "Search Results"
        v['count'] = 0
        v['offset'] = 0
        v = pictures.random_pic_update(v)
        render.page(self, "/templates/main/landing.html", v)