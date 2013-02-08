#!/usr/bin/env python
#
# Copyright 2011 Authors of PyTask.
#
# This file is part of PyTask.
#
# PyTask is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyTask is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyTask.  If not, see <http://www.gnu.org/licenses/>.


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    '"Nishanth Amuluru" <nishanth@fossee.in>',
    ]


from django.shortcuts import render_to_response,redirect
from django.template import RequestContext

from pytask.profile import models as profile_models
from pytask.taskapp.forms import *
from django.http import HttpResponse
from pytask.taskapp.models import *
from django.core.mail import send_mail
import datetime

def show_msg(user, message, redirect_url=None, url_desc=None):
    """ simply redirect to homepage """

    context = {
      'user': user,
      'message': message,
      'redirect_url': redirect_url,
      'url_desc': url_desc
    }

    return render_to_response('show_msg.html', context)
    
def is_moderator(user):
	if user.groups.filter(name = 'moderator').count() > 0 :
		return True
	else:
		return False

def home_page(request):
    """ get the user and display info about the project if not logged in.
    if logged in, display info of their tasks.
    """

    user = request.user
    
    if not user.is_authenticated():
        return render_to_response("index.html", RequestContext(request, {}))	
	
    context = {"user_loggedin":True,"user":user,"moderator":is_moderator(user)}
    return render_to_response("index.html", RequestContext(request, context))
    

def internship_form(request):
    return render_to_response("internship_forms.html")

def converted_textbooks(request):
    return render_to_response("converted_textbooks.html")

def books_in_progress(request):
    return render_to_response("books_under_progress.html")
   
def tbc_example(request):
	return render_to_response("tbc_example.html")


def about_tbc(request):
    return render_to_response("about_tbc.html")

def under_construction(request):
    return render_to_response("under_construction.html")
    
def submit_new_proposal(request):
	''' This function is used for users to submit a new proposal.
		
	'''
	user = request.user
	if not user.is_authenticated():
		return render_to_response("404.html")
	if request.method == "POST" :
		book_names = request.POST.getlist('book_name')
		author = request.POST.getlist('author')
		details = request.POST.getlist('details')
		for i in range(len(book_names)) :
			a = Book()
			a.name = book_names[i]
			a.author = author[i]
			a.details = details[i]
			a.save()
		
		new_proposal = Proposal()
		new_proposal.user = request.user
		books = list(Book.objects.all())[-3:]
		new_proposal.save()
		for book in books:
			new_proposal.textbooks.add(book)
		
	books = []
	for i in range(3):
		books.append(BookForm())
	context = {"user_loggedin":True,"user":user,"moderator":is_moderator(user),"forms":books}	
	return render_to_response("submit_new_proposal.html",RequestContext(request,context))

def proposal_status(request):
	user = request.user
	if not user.is_authenticated():
		return render_to_response("404.html")
	proposals = Proposal.objects.filter(user=user)
	if request.method == "POST":		
		for i in proposals:
			if "proposal" + str(i.id) in request.POST:
				doc_file = request.FILES['files' + str(i.id)]
				d = Document()
				d.name = doc_file.name
				d.size = doc_file.size
				d.file = doc_file
				d.upload_date = datetime.datetime.now()
				d.save()
				
				
	context = {"user_loggedin":True,"user":user,"moderator":is_moderator(user),"proposals":proposals}	
	return render_to_response("proposal_status.html",RequestContext(request,context))
	
def new_proposals(request):
	user = request.user
	if not user.is_authenticated() or not is_moderator(user):
		render_to_response("404.html")
	proposals = Proposal.objects.exclude(accepted__isnull=False)
	if request.method == "POST":
		for i in proposals:
			if str(i.id) in request.POST:
				book_id = request.POST['textbook']
				i.accepted = Book.objects.get(id=book_id)
				i.save()
				return redirect("/pytask/new-proposals/")
			if 'reject' + str(i.id) in request.POST:
				print 'reject' + i.id
				pass
	context = {"user_loggedin":True,"user":user,"moderator":is_moderator(user),"proposals":proposals}
	return render_to_response("view_new_proposals.html",RequestContext(request,context))	 
	 
