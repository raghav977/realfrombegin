import django_filters
from accounts.models import Student, Teacher

class StudentFilter(django_filters.FilterSet):
    academic_year = django_filters.CharFilter(
        field_name='section__grade__academic_year__academic_year',
        lookup_expr='exact'
    )

    class Meta:
        model = Student
        fields = ['academic_year']


class TeacherFilter(django_filters.FilterSet):
    academic_year = django_filters.CharFilter(
        field_name='sections__grade__academic_year__academic_year',
        lookup_expr='exact'
    )

    class Meta:
        model = Teacher
        fields = ['academic_year']