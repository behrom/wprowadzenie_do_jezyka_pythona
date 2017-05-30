#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib, json
from functools import partial

import kivy
kivy.require('1.1.6')
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import AsyncImage
from kivy.config import Config

class YahooWeater():
    def __init__(self, city):
        """Konstruktor ustawiajacy parametry potrzebne do pobrania informacji o prognozie pogody."""

        # zmienna przechowujaca miasto dla ktorego sprawdzana jest pogoda
        self.city = city

        # pobranie informacji o aktualnej prognozie pogody
        self.get_data()

    def change_city(self, city):
        """Metoda, dzieki ktorej mozemy zmienic miasto dla ktorego ma zostac sprawdzona prognoza pogody."""

        # zmiana miasta
        self.city = city

        # aktualizacja danych po zmianie
        self.get_data()

    def get_data(self):
        """Metoda pobierajaca prognoze pogody."""

        # adres url bedacy podstawa dla zapytan o pogode
        self.base_url = "https://query.yahooapis.com/v1/public/yql?"

        # zmienna przechowujaca id miasta dla ktoremo ma zostac pobrana pogoda
        self.woeid = 'select woeid from geo.places(1) where text="{}"'.format(self.city)

        # zapytanie o prognoze pogody
        self.yql_query = "select * from weather.forecast where woeid in ({}) and u = 'c'".format(self.woeid)

        # pobranie danych pogodowych
        self.yql_url = self.base_url + urllib.urlencode({'q': self.yql_query}) + "&format=json"
        result = urllib2.urlopen(self.yql_url).read()
        self.data = json.loads(result)

        print json.dumps(self.data, indent=4)
        return self.data

    def get_current_weather(self):
        # podstawowy adres url z ktorego maja byc pobierane obrazki pogody
        imgs_url = "http://l.yimg.com/a/i/us/we/52/"

        # dodanie danych do slownika
        current = self.data['query']['results']['channel']['item']['condition']
        current[u'high'] = self.data['query']['results']['channel']['item']['forecast'][0]['high']
        current[u'low'] = self.data['query']['results']['channel']['item']['forecast'][0]['low']
        current[u'img'] = imgs_url + current['code'] + ".gif"

        return current

    def get_weather_img_url(self):
        """Metoda zwracajaca obrazek pogody."""
        return self.data['query']['results']['channel']['item']['condition']['temp']

    def get_weather_forecast(self):
        """Metoda zwracajaca prognoze pogody na dzisiaj i na nastepne 9 dni."""
        return self.data['query']['results']['channel']['item']['forecast']


class WindowWeather(FloatLayout):
    def __init__(self, **kwargs):
        super(WindowWeather, self).__init__(**kwargs)

        self.current_btn = Button(text='Pogoda na dziś', size_hint=(
            1, 1), on_press=partial(self.get_weather, True))

        self.forecast_btn = Button(text='Prognoza na 5 dni', size_hint=(
             1, 1), on_press=partial(self.get_weather, False))

        btn_box = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.2))
        btn_box.add_widget(self.current_btn)
        btn_box.add_widget(self.forecast_btn)

        self.btn_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.btn_anchor.add_widget(btn_box)
        self.add_widget(self.btn_anchor)

        self.data_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.9))
        self.add_widget(self.data_anchor)

    def get_weather(self, _, current=True):
        if current:
            w = YahooWeater("torun")
            current_weather = w.get_current_weather()
            print current_weather

            data_box = BoxLayout(orientation='vertical', size_hint=(None, None))

            self.date_lbl = Label(text="Data pomiaru: " + current_weather['date'])
            data_box.add_widget(self.date_lbl)

            weather_box = BoxLayout(orientation='horizontal', size_hint=(None, 1))

            self.weather_img = AsyncImage(source=current_weather['img'])
            weather_box.add_widget(self.weather_img)

            self.weather_text = Label(text=current_weather['text'])
            weather_box.add_widget(self.weather_text)

            data_box.add_widget(weather_box)

            self.current_temp = Label(text="Aktualna temperatura: {}°C".format(current_weather['temp']))
            data_box.add_widget(self.current_temp)

            self.max_temp = Label(text="Maksymalna temperatura: {}°C".format(current_weather['high']))
            data_box.add_widget(self.max_temp)

            self.min_temp = Label(text="Minimalna temperatura: {}°C".format(current_weather['low']))
            data_box.add_widget(self.min_temp)

            self.data_anchor.add_widget(data_box)
        else:
            pass

class MyJB(App):
    """Klasa obslugujaca aplikacje."""

    def __init__(self, **kwargs):
        super(MyJB, self).__init__(**kwargs)
        Config.set('graphics', 'width', '500')
        Config.set('graphics', 'height', '300')

    def build(self):
        """Metoda wywolywana za kazdym razem gdy okno zostaje tworzone."""
        parent = WindowWeather()
        return parent


if __name__ in ('__main__', '__android__'):
    MyJB().run()

# w = YahooWeater("torun")
# print w.get_current_weather()['date']