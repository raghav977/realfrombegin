from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
     SubjectViewSet, TeacherViewSet,
    ClassSubjectViewSet, SectionSubjectTeacherViewSet
)



router = DefaultRouter()
# router.register(r'classes', ClassViewSet)
# router.register(r'sections', SectionViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'class-subjects', ClassSubjectViewSet)
router.register(r'section-subject-teachers', SectionSubjectTeacherViewSet)

urlpatterns = router.urls
