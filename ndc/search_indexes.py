from haystack import indexes
from haystack import site
from models import Session, Company, Speaker


class SessionIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr='name', document=True)

    def index_queryset(self):
        return Session.objects.all()

site.register(Session, SessionIndex)


class SpeakerIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr='name', document=True)

    def index_queryset(self):
        return Speaker.objects.all()

site.register(Speaker, SpeakerIndex)


class CompanyIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr='name', document=True)

    def index_queryset(self):
        return Company.objects.all()

site.register(Company, CompanyIndex)
