from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from invoicemanager.models import Customer, Invoice, InvoiceItem, Expense, InvoiceAttachment, ExpenseAttachment



# Add invoiceitem to invoice
@login_required(login_url='login/')
def add_item(request, invoice_id):
	invoice = get_object_or_404(Invoice, pk=invoice_id)
	try:
		i = invoice.invoiceitem_set.create(name=request.POST['name'], description=request.POST['description'], cost=request.POST['cost'], qty=request.POST['qty'])
		i.save()
	except (KeyError, Invoice.DoesNotExist):
		return render(request, 'view_invoice.html', {
			'invoice': invoice,
			'error_message': 'Not all fields were completed.',
		})
	else:
		return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))



# Delete invoiceitem from invoice
@login_required(login_url='login/')
def delete_item(request, invoiceitem_id, invoice_id):

	item = get_object_or_404(InvoiceItem, pk=invoiceitem_id)
	invoice = get_object_or_404(Invoice, pk=invoice_id)
	try:
		item.delete()
	except (KeyError, InvoiceItem.DoesNotExist):
		return render(request, 'view_invoice.html', {
			'invoice': invoice,
			'error_message': 'Item does not exist.',
		})
	else:
		return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))
