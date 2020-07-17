from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from urllib.request import *
import simplejson
from django.conf import settings
from django.contrib import messages
from SolrClient import SolrClient


def clientHome(request):
    solr_url = settings.SOLR_BASE_URL 
    solr = SolrClient(solr_url)
    res = solr.query(settings.SOLR_CORE,{
        'q':'*',
        'start': 2000,
        'rows':5,
        'facet':True,
        'facet.field':'Country',
        })
    print("==================Result============")
    print("Result Count:",res.get_results_count())
    print("Facet:",res.get_facets())
    print("Document:",res.docs)
    return render(request, 'client-home.html', {})
