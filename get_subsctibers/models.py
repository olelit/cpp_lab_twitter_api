from django.db import models


class Subscriber(models.Model):
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)

    def __str__(self):
        return self.name + " " + self.surname


class SubscriberSubscriber(models.Model):
    user_owner = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    user_subsciber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name="user_subsciber_user_id")

    def __str__(self):
        return self.user_owner.name + " " + self.user_owner.surname + "-->" + self.user_subsciber.name + " " + self.user_subsciber.surname
