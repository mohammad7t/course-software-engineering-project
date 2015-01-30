# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.db import models
import datetime
from werkzeug.exceptions import LengthRequired


class Hotel(models.Model):
    CHOICES_STARS = [(i, i*u'*') for i in range(1, 6)]
    name = models.CharField(max_length=32, verbose_name=u'نام')
    city = models.CharField(max_length=56, blank=True, verbose_name=u'شهر')
    owner = models.ForeignKey('auth.User')
    server_url = models.URLField(blank=True, verbose_name=u'آدرس اینترنتی کارگذار هتل')
    room_count = models.PositiveIntegerField(verbose_name=u'تعداد اتاق‌')
    stars = models.SmallIntegerField(choices=CHOICES_STARS, verbose_name=u'ستاره')
    address = models.TextField(blank=True, verbose_name=u'آدرس')
    is_approved = models.BooleanField(default=False, verbose_name=u'تاییدیه‌ی مدیر')
    features = models.ManyToManyField('hotels.Feature', blank=True, verbose_name=u'ویژگی‌ها')

    def vote_set(self):
        #stars = []
        #comments = []
        #for room_class in self.roomclass_set.all():
        #    for reservation_order in room_class.reservationorder_set.all():
        #        stars.append(reservation_order.vote.stars)

        from reservation.models import Vote
        #for vote in Vote.objects.filter(reservation_order__hotel=self):
            #stars.append(vote.stars)
            #comments.append(vote.comment)
        return Vote.objects.filter(reservation_order__room_class__hotel=self)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('hotel_view', kwargs={'pk': self.id})


class RoomClass(models.Model):
    hotel = models.ForeignKey('hotels.Hotel', verbose_name=u'هتل')
    name = models.CharField(max_length=32, verbose_name=u'نام')
    description = models.TextField(verbose_name=u'توضیح')
    price = models.PositiveIntegerField(verbose_name=u'قیمت')
    bed_count = models.PositiveIntegerField(verbose_name=u'تعداد تخت‌خواب')
    features = models.ManyToManyField('hotels.Feature', blank=True, verbose_name=u'ویژگی‌ها')

    def __unicode__(self):
        return self.name


class HotelImage(models.Model):
    hotel = models.ForeignKey('hotels.Hotel', verbose_name=u'هتل')
    caption = models.TextField(blank=True, verbose_name=u'زیرنویس عکس')
    image = models.ImageField(upload_to = 'images/', verbose_name=u'عکس')

    def __unicode__(self):
        return self.caption


class Feature(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'نام')
    icon = models.ImageField(verbose_name=u'عکس')
    is_for_hotel = models.BooleanField(default=True, verbose_name=u'برای هتل')
    is_for_room = models.BooleanField(default=True, verbose_name=u'برای اتاق')

    def __unicode__(self):
        return self.name
