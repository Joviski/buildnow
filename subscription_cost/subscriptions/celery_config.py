
class SubscriptionCeleryConfig(object):
    """Class representing the `subscription` application celery configuration."""

    @staticmethod
    def task_routes() -> dict:
        """Retrieve the celery.task_routes records related to the App."""
        return {"subscription.tasks.*": {"queue": "subscription-celery"}}
