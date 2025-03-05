from subscription_cost.celery import app as celeryApp

from subscriptions.models import Subscription

@celeryApp.task(bind=True)
def iterate_subscription(self, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    if subscription.active:
        subscription.iteration += 1
        subscription.save()
        iterate_subscription.s(subscription.id).apply_async(eta=subscription.renewal_date)


