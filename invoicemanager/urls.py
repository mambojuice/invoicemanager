from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'invoicemanager'

patterns = [
    
	# # # DEFAULT
    
	url(r'^$', views.invoices.index, name='index'),

    # # # INVOICES

    url(r'^invoice/new/$', views.invoices.new_invoice, name='new_invoice'),
    url(r'^invoice/all/$', views.invoices.all_invoices, name='all_invoices'),
    url(r'^invoice/draft/$', views.invoices.draft_invoices, name='draft_invoices'),
    url(r'^invoice/paid/$', views.invoices.paid_invoices, name='paid_invoices'),
    url(r'^invoice/unpaid/$', views.invoices.unpaid_invoices, name='unpaid_invoices'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/$', views.invoices.invoice, name='invoice'),
    url(r'^invoice/search/$', views.invoices.search_invoice, name='search_invoice'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/update/$', views.invoices.update_invoice, name='update_invoice'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/print/$', views.invoices.print_invoice, name='print_invoice'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/delete/$', views.invoices.delete_invoice, name='delete_invoice'),

    # # # ITEMS

    url(r'^invoice/(?P<invoice_id>[0-9]+)/item/add/$', views.items.add_item, name='add_item'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/item/(?P<invoiceitem_id>[0-9]+)/delete/$', views.items.delete_item, name='delete_item'),

    # # # INVOICE EXPENSES

    url(r'^invoice/(?P<invoice_id>[0-9]+)/expenses/add/$', views.expenses.add_invoice_expense, name='add_invoice_expense'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/expenses/(?P<expense_id>[0-9]+)/delete/$', views.expenses.delete_invoice_expense, name='delete_invoice_expense'),

    # # # BUSINESS EXPENSES
	
    url(r'^expenses/$', views.expenses.expense_list, name='expense_list'),
    url(r'^expenses/new/$', views.expenses.new_business_expense, name='new_business_expense'),
    url(r'^expenses/(?P<expense_id>[0-9]+)/delete/$', views.expenses.delete_business_expense, name='delete_business_expense'),

    # # # REPORTS

    url(r'^accounting/$', views.reports.accounting, name='accounting'),

    # # # ATTACHMENTS

    url(r'^invoice/(?P<invoice_id>[0-9]+)/attachments/add/$', views.invoices.upload_invoice_attachment, name='upload_invoice_attachment'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/attachments/(?P<invoiceattachment_id>[0-9]+)/delete/$', views.invoices.delete_invoice_attachment, name='delete_invoice_attachment'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/attachments/add/$', views.expenses.upload_business_expense_attachment, name='upload_business_expense_attachment'),

    # # # CUSTOMERS

    url(r'^customers/$', views.customers.customer_list, name='customer_list'),
    url(r'^customer/(?P<customer_id>[0-9]+)/$', views.customers.customer, name='customer'),
	url(r'^customer/(?P<customer_id>[0-9]+)/update/$', views.customers.update_customer, name='update_customer'),
    url(r'^customer/(?P<customer_id>[0-9]+)/delete/$', views.customers.delete_customer, name='delete_customer'),
    url(r'^customer/new/$', views.customers.new_customer, name='new_customer'),

    # # # USER AUTHENTICATION
	
    url(r'^login/$', views.userauth.login_view, name='login'),
    url(r'^logout/$', views.userauth.logout_view, name='logout'),

    # # # ADMIN
	
    url(r'^users/$', views.admin.users, name='users'),
    url(r'^settings/$', views.admin.settings, name='settings'),
]

urlpatterns = [
    url(r'^', include(patterns, namespace="invoicemanager")),
]
