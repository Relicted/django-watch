from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
# ============================================== #


class WatchingList(models.Model):
    STATUSES = (
        (1, _("Watching")),
        (2, _("Completed")),
        (3, _("Plan to watch")),
        (4, _("On-hold")),
        (5, _("Dropped")),
        (6, _("Waiting for")),
    )
    SCORES = (
        (1, _('1 - Appalling')),
        (2, _('2 - Horrible')),
        (3, _('3 - Very Bad')),
        (4, _('4 - Bad')),
        (5, _('5 - Average')),
        (6, _('6 - Fine')),
        (7, _('7 - Good')),
        (8, _('8 - Very Good')),
        (9, _('9 - Great')),
        (10, _('10 - Masterpiece')),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True,
        related_name='watchlist')
    video = models.ForeignKey(
        'Video', on_delete=models.CASCADE, related_name='watchlist')
    score = models.PositiveSmallIntegerField(choices=SCORES)
    status = models.PositiveSmallIntegerField(choices=STATUSES)
    is_favorite = models.BooleanField(default=False)
    tags = models.CharField(max_length=500, blank=True, default='')
    comment = models.CharField(max_length=500, blank=True, default='')

    def __str__(self):
        return str(self.score)

    def tag_list(self):
        return self.tags.split(',')