from django.db import models
# from django.core.urlresolvers import reverse

from pajtyn_django import settings

# Create your models here.
RATE_CHOICES = (
    (0, '1'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
)

MEAT_CHOICES = (
    ('Baranina', 'Baranina'),
    ('Baranina-Kurczak', 'Baranina-Kurczak'),
    ('Kurczak', 'Kurczak'),
    ('Wołowina', 'Wołowina'),
    ('Wegetariański', 'Wegetariański')
)

SAUCE_CHOICES = (
    ('Ostry', 'Ostry'),
    ('Mieszany', 'Mieszany'),
    ('Lagodny', 'Lagodny'),
    ('Czosnkowy', 'Czosnkowy'),
    ('Bez sosu', 'Bez sosu')
)

BATTER_CHOICES = (
    ('Tortilla', 'Tortilla'),
    ('Pita', 'Pita'),
    ('Bułka', 'Bułka')
)





class Kebaby_lokale(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200, default="")
    rate = models.FloatField(default=0)
    photo_ref = models.CharField(max_length=1000)

    # def get_absolute_url(self):
    #     return reverse()


class Kebaby_dania(models.Model):
    name = models.CharField(max_length=200)
    photo_ref = models.CharField(max_length=1000)

    meat_type = models.CharField(max_length=20, choices=MEAT_CHOICES, default='Baranina')
    meat = models.IntegerField(choices=RATE_CHOICES, default=0)

    sauce_type = models.CharField(max_length=20, choices=SAUCE_CHOICES, default='Lagodny')
    sauce = models.IntegerField(choices=RATE_CHOICES, default=0)

    batter_type=models.CharField(max_length=20, choices=BATTER_CHOICES, default='Tortilla')
    batter = models.IntegerField(choices=RATE_CHOICES, default=0)

    salds = models.IntegerField(choices=RATE_CHOICES, default=0)

    local_id = models.ForeignKey(Kebaby_lokale, on_delete=models.CASCADE)
    avg_ref = models.FloatField(default=0)

    def calculate_avg(self):
        return (Kebaby_dania.sauce + Kebaby_dania.batter + Kebaby_dania.meat + Kebaby_dania.salds) / 4


class Inne_dania(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    overall_rate = models.IntegerField(choices=RATE_CHOICES, default=0)
    photo_ref = models.CharField(max_length=1000)
    local_id = models.ForeignKey(Kebaby_lokale, on_delete=models.CASCADE)
