# Create your views here.
from tags.models import Tag, FS1Tag
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from utils.search.solr import SolrQuery, SolrResponseInterpreter, \
    SolrResponseInterpreterPaginator, SolrException, Solr
import logging

search_logger = logging.getLogger("search")

def tags(request, multiple_tags=None):
    if multiple_tags:
        multiple_tags = multiple_tags.split('/')
    else:
        multiple_tags = []
    
    multiple_tags = sorted(filter(lambda x:x, multiple_tags))
    
    try:
        current_page = int(request.GET.get("page", 1))
    except ValueError:
        current_page = 1

    solr = Solr(settings.SOLR_URL)
    
    query = SolrQuery()
    if multiple_tags:
        query.set_query(" ".join("tag:\"" + tag + "\"" for tag in multiple_tags))
    else:
        query.set_query("*:*")
    query.set_query_options(start=(current_page - 1) * settings.SOUNDS_PER_PAGE, rows=settings.SOUNDS_PER_PAGE, field_list=["id"], sort=["num_downloads desc"])
    query.add_facet_fields("tag")
    query.set_facet_options_default(limit=100, sort=True, mincount=1, count_missing=False)
    
    try:
        results = SolrResponseInterpreter(solr.select(unicode(query)))
        paginator = SolrResponseInterpreterPaginator(results, settings.SOUNDS_PER_PAGE)
        page = paginator.page(current_page)
        error = False
        tags = [dict(name=f[0], count=f[1]) for f in results.facets["tag"]]
    except SolrException, e:
        error = True
        search_logger.error("SOLR ERROR - %s" % e)

    return render_to_response('sounds/tags.html', locals(), context_instance=RequestContext(request))


def old_tag_link_redirect(request):    
    fs1tag_id = request.GET.get('id', False)
    if fs1tag_id:
        tags = fs1tag_id.split('_')
        try:
            fs1tags = FS1Tag.objects.filter(fs1_id__in=tags).values_list('tag', flat=True)            
        except ValueError, e:
            raise Http404
            
        tags = Tag.objects.filter(id__in=fs1tags).values_list('name', flat=True)
        if not tags:
            raise Http404
         
        return HttpResponsePermanentRedirect(reverse("tags", args=['/'.join(tags)]))
    else:
        raise Http404    