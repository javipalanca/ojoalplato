# Glyphicon halflings for Bootstrap courtesy http://glyphicons.com/
#
# Bootstrap glyphicon stars ver 2
from django import forms
from django.utils.safestring import mark_safe
from six import string_types
import floppyforms

star_set_2 = {
    'star': "<i class='glyphicon glyphicon-star likert-star'></i>",
    'unlit': "<i class='glyphicon glyphicon-star-empty likert-star'></i>",
    'noanswer': "<i class='glyphicon glyphicon-ban-circle likert-star'></i>"
}


class PointWidget(floppyforms.gis.PointWidget, floppyforms.gis.BaseOsmWidget):
    pass


def render_stars(num, max_stars, star_set):
    """
    Star renderer returns a HTML string of stars
    If num is None or a blank string, it returns the unanswered tag
    Otherwise, the returned string will contain num solid stars
    followed by max_stars - num empty stars
    If num > max_stars, render max_stars solid stars
    star_set is a dictionary of strings with keys: star, unlit, noanswer
    """
    _input = '<input class="vIntegerField" id="id_stars" name="stars" value="{}" '.format(num)
    _input += 'title="" type="number" data-original-title="" min=0 max=3 style="width: 50px;">'
    if num is None or (isinstance(num, string_types) and len(num) == 0):
        return '<span>' + _input + "&nbsp;" + star_set['noanswer'] + '</span>'

    difference = int(max_stars) - int(num)
    if difference < 0:
        num = max_stars
        difference = 0

    stars = ''.join(star_set['star'] * int(num) + star_set['unlit'] * difference)
    return '<span>' + _input + "&nbsp;" + stars + '</span>'


class StarsWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        max_stars = 3
        return mark_safe(render_stars(value, max_stars, star_set_2))


class WeekdayWidget(forms.CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        value = super(WeekdayWidget, self).value_from_datadict(data, files, name)
        return ",".join([x for x in value])
