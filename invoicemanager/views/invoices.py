from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import datetime

from invoicemanager.models import Customer, Invoice, InvoiceItem, Expense, InvoiceAttachment, ExpenseAttachment



# Default invoice list, show 25 recent invoices
@login_required(login_url='login/')
def index(request):
    invoices = Invoice.objects.order_by('-date')[:25]
    context = {
		'title' : 'Recent Invoices',
        'invoice_list' : invoices,
    }
    return render(request, 'index.html', context)




# Show big list of all invoices
@login_required(login_url='login/')
def all_invoices(request):
    invoices = Invoice.objects.order_by('-date')
    context = {
		'title' : 'All Invoices',
        'invoice_list' : invoices,
    }
    return render(request, 'index.html', context)



# Show draft invoices
@login_required(login_url='login/')
def draft_invoices(request):
    invoices = Invoice.objects.filter(status='Draft').order_by('-date')
    context = {
		'title' : 'Draft Invoices',
        'invoice_list' : invoices,
    }
    return render(request, 'index.html', context)



# Show paid invoices
@login_required(login_url='login/')
def paid_invoices(request):
    invoices = Invoice.objects.filter(status='Paid').order_by('-date')
    context = {
		'title' : 'Paid Invoices',
        'invoice_list' : invoices,
    }
    return render(request, 'index.html', context)



# Show unpaid invoices
@login_required(login_url='login/')
def unpaid_invoices(request):
    invoices = Invoice.objects.filter(status='Unpaid').order_by('-date')
    context = {
		'title' : 'Unpaid Invoices',
        'invoice_list' : invoices,
    }
    return render(request, 'index.html', context)



# Display a specific invoice
@login_required(login_url='login/')
def invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    context = {
		'title' : 'Invoice ' + str(invoice_id),
	    'invoice' : invoice,
	}
    return render(request, 'invoice.html', context)



# Search for invoice
@login_required(login_url='login/')
def search_invoice(request):
    id = request.POST['id']
    return HttpResponseRedirect(reverse('invoice', args=(id,)))



# Create new invoice
@login_required(login_url='login/')
def new_invoice(request):
	# If no customer_id is defined, create a new invoice
	if request.method=='POST':
		customer_id = request.POST['customer_id']

		if customer_id=='None':
			customers = Customer.objects.order_by('name')
			context = {
				'title' : 'New Invoice',
				'customer_list' : customers,
				'error_message' : 'Please select a customer.',
				}
			return render(request, 'new_invoice.html', context)
		else:
			customer = get_object_or_404(Customer, pk=customer_id)
			i = Invoice(customer=customer, date=datetime.date.today(), status='Unpaid')
			i.save()
			return HttpResponseRedirect(reverse('invoice', args=(i.id,)))

	else:
		# Customer list needed to populate select field
		customers = Customer.objects.order_by('name')
		context = {
			'title' : 'New Invoice',
			'customer_list' : customers,
		}
		return render(request, 'new_invoice.html', context)



# Print invoice
@login_required(login_url='login/')
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    context = {
		'title' : "Invoice " + str(invoice_id),
	    'invoice' : invoice,
	}
    return render(request, 'print_invoice.html', context)



# Delete an invoice
@login_required(login_url='login/')
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice.delete()
    return HttpResponseRedirect(reverse('index'))



# Update invoice
@login_required(login_url='login/')
def update_invoice(request, invoice_id):
	invoice = get_object_or_404(Invoice, pk=invoice_id)
	try:
		invoice.date = datetime.datetime.strptime(request.POST['date'], "%m/%d/%Y")
		invoice.status = request.POST['status']
		invoice.save()
	except (KeyError, Invoice.DoesNotExist):
		return render(request, 'invoice.html', {
			'invoice': invoice,
			'error_message': 'Not able to update invoice!',
		})
	else:
		context = {
			'confirm_update' : True,
			'title' : 'Invoice ' + str(invoice_id),
			'invoice' : invoice,
			}
		return render(request, 'invoice.html', context)



# Upload attachment for invoice
@login_required(login_url='login/')
def upload_invoice_attachment(request, invoice_id):
    myfile = request.FILES['file']
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    fs = FileSystemStorage()
    fs.save(myfile.name, myfile)

    e = invoice.invoiceattachment_set.create(file=myfile, displayname=myfile.name)
    e.save()

    return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))



# Delete attachment from invoice
@login_required(login_url='login/')
def delete_invoice_attachment(request, invoice_id, invoiceattachment_id):
	invoice = get_object_or_404(Invoice, pk=invoice_id)
	invoiceattachment = get_object_or_404(InvoiceAttachment, pk=invoiceattachment_id)
	try:
		invoiceattachment.delete()
		fs = FileSystemStorage()
		fs.delete(invoiceattachment)
	except:
		context = {
			'error_message' : "Unable to delete attachment!",
			'invoice_id' : invoice_id
		}
		return render(request, 'view_invoice.html', context)
	else:
		return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))
