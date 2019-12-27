from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import datetime

from invoicemanager.models import Customer, Invoice, InvoiceItem, Expense, InvoiceAttachment, ExpenseAttachment



# Add expense to invoice
@login_required(login_url='login/')
def add_invoice_expense(request, invoice_id):
	invoice = get_object_or_404(Invoice, pk=invoice_id)
	try:
		e = invoice.expense_set.create(description=request.POST['description'], cost=request.POST['cost'], qty=request.POST['qty'])
		e.save()
	except (KeyError, Invoice.DoesNotExist):
		return render(request, 'view_invoice.html', {
			'invoice': invoice,
			'error_message': 'Not all fields were completed.',
		})
	else:
		return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))



# Delete expense from invoice
@login_required(login_url='login/')
def delete_invoice_expense(request, expense_id, invoice_id):
	expense = get_object_or_404(Expense, pk=expense_id)
	invoice = get_object_or_404(Invoice, pk=invoice_id)
	try:
		expense.delete()
	except (KeyError, Expense.DoesNotExist):
		return render(request, 'view_invoice.html', {
			'invoice': invoice,
			'error_message': 'Expense does not exist.',
		})
	else:
		return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))



# List all business expenses (expense item with no invoice_id)
@login_required(login_url='login/')
def expense_list(request):
	expenses = Expense.objects.filter(invoice_id=None)
	context = {
		'expenses' : expenses,
	}
	return render(request, 'expenses.html', context)



# New business expense
@login_required(login_url='login/')
def new_business_expense(request):
	if request.method == 'POST':
		# Stuff from form
		date = datetime.datetime.strptime(request.POST['date'], "%m/%d/%Y")
		e = Expense(description=request.POST['description'], date=date, cost=request.POST['cost'], qty=request.POST['qty'])
		e.save()
		return HttpResponseRedirect(reverse('expense_list'))
	else:
		return render(request, 'new_expense.html')



# Upload attachment for business expense
@login_required(login_url='login/')
def upload_business_expense_attachment(request, expense_id):
    # Get expense
    expense = get_object_or_404(Expense, pk=expense_id)

    if request.method == 'POST':
        # Get file from POST data
        myfile = request.FILES['file']

        # Save file to filesystem
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)

        # Create new ExpenseAttachment record
        e = expense.expenseattachment_set.create(file=myfile, displayname=myfile.name)
        e.save()

		# Redirect to expenses list
        return HttpResponseRedirect(reverse('expense_list'))
    else:
        context = {
            'expense' : expense,
        }
        return render(request, 'upload_attachment.html', context)



# Delete attachment from business expense
@login_required(login_url='login/')
def delete_business_expense_attachment(request, expense_id, expenseattachment_id):
	expense = get_object_or_404(Expense, pk=expense_id)
	expenseattachment = get_object_or_404(ExpenseAttachment, pk=expenseattachment_id)
	try:
		expenseattachment.delete()
		fs = FileSystemStorage()
		fs.delete(expenseattachment)
	except:
		context = {
			'error_message' : "Unable to delete attachment!",
		}
		return render(request, 'expenses.html', context)
	else:
		return HttpResponseRedirect(reverse('expense_list'))



# Delete business expense
@login_required(login_url='login/')
def delete_business_expense(request, expense_id):
	expense = get_object_or_404(Expense, pk=expense_id)
	try:
		expense.delete()
	except (KeyError, Expense.DoesNotExist):
		return render(request, 'expenses.html', {
			'error_message': 'Expense does not exist!',
		})
	else:
		return HttpResponseRedirect(reverse('expense_list'))
