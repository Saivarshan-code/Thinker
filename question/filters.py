import django_filters

from question.models import question,comment

class QuestionFilter(django_filters.FilterSet):
    categories = (('maths','maths'),('biology','biology'),('physics','physics'),('chemistry','chemistry'),('history','history'),('geography','geography'),('democratic politics','democratic politics'),('economics','economics'),('english','english'),('Computer science','Computer science'),('Tamil','Tamil'),('Hindi','Hindi'),('General','General'))
    title = django_filters.CharFilter(label="Search:",lookup_expr='icontains')
    category = django_filters.ChoiceFilter(label='category',choices=categories)
    question = django_filters.CharFilter(label="Search:",lookup_expr='icontains')
    class Meta:
        model = question
        fields = ['title','category','question']


class SearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label="Search:",lookup_expr='icontains')
    class Meta:
        model = question
        fields = ['title']
