from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=255)  # No choices
    color = models.CharField(max_length=255)
    key = models.FloatField(help_text="Unique numeric key, can include decimals")

    class Meta:
        ordering = ['make', 'color']
        verbose_name = "Car"
        verbose_name_plural = 'Cars'

    def __str__(self):
        return f"{self.make} - {self.color} (Key: {self.key})"
