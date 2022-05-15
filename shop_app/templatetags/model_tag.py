from django import template
from shop_app.models import Category, Model
register = template.Library()

@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()

@register.inclusion_tag('shop_app/tags/last_model.html')
def get_last_models(count=5):
    models = Model.objects.order_by('id')[:count]
    return {'last_models': models}