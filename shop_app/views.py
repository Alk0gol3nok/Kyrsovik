from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Model, Category, Racer, Season, Rating
from .forms import ReviewForm, RatingForm
# Create your views here.


class SeasonYear():
    """Фильтр Сезоны, года, категории"""
    def get_seasons(self):
        return Season.objects.all()

    def get_years(self):
        return Model.objects.filter(draft=False).values('year')

    def get_categories(self):
        return Category.objects.all()


class ModelView(SeasonYear, ListView):
    """Список моделей"""
    model = Model
    queryset = Model.objects.filter(draft=False)
    paginate_by = 20



class ModelDetailView(SeasonYear, DetailView):
    """Полное описание модели"""
    model = Model
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context



class AddReview(View):
    """Отправка отзыва"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        model = Model.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.model = model
            form.save()
        return redirect(model.get_absolute_url())


class RacerView(SeasonYear, DetailView):
    """Вывод информации о гонщике"""
    model = Racer
    template_name = 'shop_app/racer.html'
    slug_field = 'name'


class FilterModelsView(SeasonYear, ListView):
    """Фильтр моделей"""
    paginate_by = 20
    def get_queryset(self):
        queryset = Model.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(season__in=self.request.GET.getlist('season')) |
            Q(category__in=self.request.GET.getlist('category'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["season"] = ''.join([f"season={x}&" for x in self.request.GET.getlist("season")])
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context



class AddStarRating(View):
    """Добавление рейтинга модели"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                model_id=int(request.POST.get('model')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск моделей"""
    paginate_by = 20
    def get_queryset(self):
        return Model.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context

