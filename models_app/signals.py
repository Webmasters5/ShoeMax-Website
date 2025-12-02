from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from .models import Order, OrderItem, ShoeVariant

@receiver(post_save, sender=OrderItem)
def orderitem_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        order_status = (instance.order.status or '').lower()
    except Exception:
        order_status = ''

    if order_status != 'pending':
        return

    # Equivalent to BEGIN TRANSACTION
    with transaction.atomic():
        variant = ShoeVariant.objects.select_for_update().get(pk=instance.variant.pk)
        if variant.stock < instance.quantity:
            raise ValidationError(f"Insufficient stock for {variant}. Available {variant.stock}, requested {instance.quantity}.")
        ShoeVariant.objects.filter(pk=variant.pk).update(stock=F('stock') - instance.quantity)


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    old_status = (old.status or '').lower()
    new_status = (instance.status or '').lower()

    if old_status == new_status:
        return

    # pending -> cancelled: restock items
    if old_status == 'pending' and new_status == 'cancelled':
        with transaction.atomic():
            for item in old.items.select_related('variant').all():
                ShoeVariant.objects.filter(pk=item.variant.pk).update(stock=F('stock') + item.quantity)
