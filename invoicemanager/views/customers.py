from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime

from invoicemanager.models import Customer, Invoice, InvoiceItem, Expense, InvoiceAttachment, ExpenseAttachment



# List all customers
@login_required(login_url='login/')
def customer_list(request):
	customers = Customer.objects.all()
	context = {
		'title' : 'Customer List',
		'customers' : customers,
	}
	return render(request, 'customers.html', context)



# Show specific customer details
@login_required(login_url='login/')
def customer(request, customer_id):
	customer = get_object_or_404(Customer, pk=customer_id)
	invoices = Invoice.objects.filter(customer = customer)
	context = {
		'title' : "Customer info - %s" % customer.name,
		'customer' : customer,
		'invoices' : invoices,
	}
	return render(request, 'customer.html', context)



# Add new customer
@login_required(login_url='login/')
def new_customer(request):
	if request.method == 'POST':
		# Stuff from form
		c = Customer(name=request.POST['name'], address1=request.POST['address1'], address2=request.POST['address2'], city=request.POST['city'], state=request.POST['state'], zip=request.POST['zip'], email=request.POST['email'])
		c.save()

		if 'savecreate' in request.POST:
			i = Invoice(customer=c, date=datetime.date.today(), status='Unpaid')
			i.save()
			return HttpResponseRedirect(reverse('invoice', args=(i.id,)))
		else:
			return HttpResponseRedirect(reverse('customer_list'))
	else:
		return render(request, 'new_customer.html')



# Update customer
@login_required(login_url='login/')
def update_customer(request, customer_id):
	# Stuff from form
	c = get_object_or_404(Customer, pk=customer_id)

	c.name = request.POST['name']
	c.address1 = request.POST['address1']
	c.address2 = request.POST['address2']
	c.city = request.POST['city']
	c.state = request.POST['state']
	c.zip = request.POST['zip']
	c.email = request.POST['email']

	c.save()

	return HttpResponseRedirect(reverse('customer', args=(c.id,)))


# Delete customer
@login_required(login_url='login/')
def delete_customer(request, customer_id):
	customer = get_object_or_404(Customer, pk=customer_id)
	customer.delete()
	return HttpResponseRedirect(reverse('customer_list'))
