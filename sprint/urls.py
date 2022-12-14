from django.urls import path

from . import views

urlpatterns = [
    path('sprints', views.SprintC.as_view(), name='add'),
    path('sprints/<int:id>', views.SprintC.as_view(), name='update'),
    path('params', views.VoteParameter.as_view(), name='add-parameter'),
    path('params/<int:id>', views.VoteParameter.as_view(), name='update-parameter'),
    path('sprints/<int:id>/votes', views.Voting.as_view(), name='user-votes'),
    path('sprints/<int:id>/results', views.Result.as_view(), name='result'),
    path('sprintdata', views.SprintData.as_view(), name='sprintdata'),
    path('show', views.ShowResultApi.as_view(), name='showResult'),
    path('show/<int:id>', views.ShowResultApi.as_view(), name='update-showResult'),
    path('game', views.Gaming.as_view(), name='gaming'),
    path('game/<int:id>', views.Gaming.as_view(), name='update-gaming'),
    path('special-mention', views.SpecialMention.as_view(), name='special-mention'),
    path('special-mention/<int:id>', views.SpecialMention.as_view(), name='special-mention-get'),
    path('special-mention-result/<int:id>', views.SpecialMentionResult.as_view(), name='special-mention-result-get')
]
