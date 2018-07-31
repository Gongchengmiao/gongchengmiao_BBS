
import datetime

from haystack import indexes
from .models import ArticlePost

class ArticlePostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author = indexes.CharField(model_attr='author')
    #pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return ArticlePost

    #def index_queryset(self, using=None):  # 重载index_..函数
     #   """Used when the entire index for model is updated."""
      #  return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())

    def index_queryset(self, using=None):
        return self.get_model().objects.all()