from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


USER = get_user_model()


STATUS_CHOICES = (
    (0, "Due"),
    (1, "Unpaid"),
    (2, "Paid"),
)


class Invoice(models.Model):
    user = models.ForeignKey(
        USER, 
        verbose_name=_("User"), 
        on_delete=models.CASCADE,
        related_name="invoices"
    )
    name = models.CharField(_("Invoice name"), max_length=150)
    logo = models.ImageField(upload_to="logo", blank=True, null=True)

    invoice_from = models.TextField(_("Invoice From"))
    bill_to = models.TextField(_("Bill to"))
    ship_to = models.TextField(_("Ship to"))
    date = models.DateField(_("Creation date"))
    due_date = models.DateField(_("Due date"))

    notes = models.TextField(_("Notes"))
    terms = models.TextField(_("Terms"))

    status = models.CharField(
        _("Status"), 
        max_length=50,
        choices=STATUS_CHOICES,
        default=1
    )

    def __str__(self):
        return self.name


class Item(models.Model):
    invoice = models.ForeignKey(
        Invoice, 
        verbose_name=_("Invoice"), 
        on_delete=models.CASCADE,
        related_name="items"
    )
    title = models.CharField(_("Title"), max_length=250)
    quantity = models.SmallIntegerField(_("Quantity"))
    rate = models.IntegerField(_("Rate"))

    def __str__(self):
        return f"{self.invoice.name}:{self.name}"