from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ApprovedManager(models.Manager):
    use_for_related_fields = True
    def get_queryset(self):
        return super().get_queryset().filter(approved_by__isnull=False)


class ProductComment(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    product = models.ForeignKey('products.Product', verbose_name=_("product"), on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE, related_name='comment_users')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("approved by"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comment_approved_users',
        editable=False
    )
    approved_time = models.DateTimeField(blank=True, null=True, editable=False)
    content = models.TextField(_("content"))

    objects = models.Manager()
    approves = ApprovedManager()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _("Comments")

    def is_approved(self):
        return bool(self.approved_by)
    is_approved.boolean = True
