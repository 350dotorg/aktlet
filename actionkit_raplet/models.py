from django.conf import settings
from django.db import models

class Configuration(models.Model):

    sql = models.TextField(default="""
SELECT u.id, u.first_name, u.last_name, u.source, u.subscription_status,
              (SELECT COALESCE((SELECT MIN(created_at) FROM core_subscriptionhistory h WHERE h.user_id=u.id AND h.change_id IN (1, 2, 7)), u.created_at))
                AS created_at,
              (SELECT COUNT(distinct a.id) from core_action a where a.user_id=u.id) AS num_actions, 
              (SELECT MIN(start) FROM core_orderrecurring WHERE status="active" AND start > NOW() AND user_id=u.id) AS next_recurring_donation_date,
              (SELECT amount FROM core_orderrecurring WHERE status="active" AND start > NOW() AND user_id=u.id ORDER BY start asc LIMIT 1) AS next_recurring_donation_amount,
              (SELECT COALESCE(SUM(core_transaction.amount),0) from core_transaction JOIN core_order on core_order.id=core_transaction.order_id
               WHERE user_id=u.id AND core_transaction.status="completed" AND core_order.status="completed") AS total_donations_direct,
              (SELECT COALESCE(SUM(core_order.total),0) from core_order WHERE user_id=u.id AND core_order.status="completed" AND core_order.import_id IS NOT NULL) AS total_donations_imported,
              (SELECT MAX(a.id) from core_action a where a.user_id=u.id) AS latest_action_id,
              (SELECT la.created_at FROM core_action la WHERE la.user_id=u.id ORDER BY la.id DESC LIMIT 1) as latest_action_date,
              (SELECT lap.name FROM core_action la
                    JOIN core_page lap ON lap.id=la.page_id WHERE la.user_id=u.id ORDER BY la.id DESC LIMIT 1)
                 AS latest_action_page
    FROM core_user u
  WHERE u.email=%s
""")
    html = models.TextField(default="""
{%% load helpful_tags %%}
{%% if id %%}
<h3 class='name'>%(SITE_NAME)s AK ID: {{ id }}</h3>
<p><a href="%(ACTIONKIT_API_HOST)s/admin/core/user/{{ id }}/">{{ first_name }} {{ last_name }}</a> has been a member
since {{ created_at }} (source: {{ source }})</p>
<p class="subscription-{{ subscription_status }}">Subscription status: {{ subscription_status }}</p>
<p>Actions taken: {{ num_actions }}</p>
<p>Lifetime donations: ${{ total_donations_direct|add_numbers:total_donations_imported|floatformat:2 }} {%% if next_recurring_donation_date %%}<span class="green">(${{ next_recurring_donation_amount }} recurring donation scheduled for {{ next_recurring_donation_date }})</span>{%% endif %%}</p>
<p>Last acted on page <a href="%(ACTIONKIT_API_HOST)s/act/{{ latest_action_page }}">{{ latest_action_page }}</a>, {{ latest_action_date }}</p>
{%% else %%}
<h3 class='name'>No %(SITE_NAME)s Actionkit Entry</h3>
{%% endif %%}""" % {'SITE_NAME': settings.SITE_NAME, 
                    'ACTIONKIT_API_HOST': settings.ACTIONKIT_API_HOST})
    css = models.TextField(default="""
a { color: blue; border-bottom: 1px dotted blue; }
h2.name { color: gray; }
p.subscription-unsubscribed { font-weight: bold; color: red }
p.subscription-subscribed, span.green { color: green }
""")

    slug = models.SlugField(unique=True, blank=True)

from django.contrib import admin
admin.site.register(Configuration)

#from djangohelpers.lib import register_admin
#register_admin(Configuration)
