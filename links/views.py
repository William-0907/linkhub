import io
import json
from datetime import timedelta

import qrcode
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, F
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse

from accounts.forms import ProfileForm

from .forms import LinkForm
from .models import ClickEvent, Link

CHART_DAYS = 14


@login_required
def dashboard(request):
    links = request.user.links.all()
    total_clicks = sum(link.clicks for link in links)

    today = timezone.localdate()
    start = today - timedelta(days=CHART_DAYS - 1)
    daily = dict(
        ClickEvent.objects.filter(
            link__user=request.user,
            created_at__date__gte=start,
        )
        .values_list('created_at__date')
        .annotate(n=Count('id'))
        .order_by('created_at__date')
    )
    labels = [(start + timedelta(days=i)) for i in range(CHART_DAYS)]
    chart_labels = [d.strftime('%b %d') for d in labels]
    chart_values = [daily.get(d, 0) for d in labels]

    context = {
        'links': links,
        'link_form': LinkForm(),
        'profile_form': ProfileForm(instance=request.user.profile),
        'total_clicks': total_clicks,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
    }
    return render(request, 'links/dashboard.html', context)


@login_required
def link_create(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    form = LinkForm(request.POST)
    if form.is_valid():
        link = form.save(commit=False)
        link.user = request.user
        last = request.user.links.order_by('-order').first()
        link.order = (last.order + 1) if last else 0
        link.save()
    return redirect('dashboard')


@login_required
def link_edit(request, link_id):
    link = get_object_or_404(Link, id=link_id, user=request.user)
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
    return redirect('dashboard')


@login_required
def link_delete(request, link_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    link = get_object_or_404(Link, id=link_id, user=request.user)
    link.delete()
    return redirect('dashboard')


@login_required
def link_reorder(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        payload = json.loads(request.body)
        link_ids = payload.get('order', [])
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    links = {link.id: link for link in request.user.links.all()}
    if set(link_ids) != set(links.keys()):
        return JsonResponse({'error': 'Link IDs do not match user links'}, status=400)

    for index, link_id in enumerate(link_ids):
        Link.objects.filter(id=link_id).update(order=index)
    return JsonResponse({'status': 'ok'})


def public_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    links = user.links.all()
    context = {
        'profile_user': user,
        'links': links,
    }
    return render(request, 'links/public_profile.html', context)


def go(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    with transaction.atomic():
        Link.objects.filter(id=link_id).update(clicks=F('clicks') + 1)
        ClickEvent.objects.create(
            link=link,
            referrer=request.META.get('HTTP_REFERER', '')[:255],
        )
    return redirect(link.url)


def qr_code(request, username):
    profile_url = request.build_absolute_uri(reverse('profile', args=[username]))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')
