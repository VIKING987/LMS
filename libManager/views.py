from django.contrib.auth import login
from authenticate.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView
from libManager.models import BookRecords
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

def home(request):
    user = request.user
    if user.is_anonymous:
        messages.error(request, 'You Need To Be Logged In For That!!')
        return redirect('login')
    designation = user.designation
    fname = user.fname

    if designation.lower() == 'librarian':
        return render(request, 'libManager/librarian.html', {'fname':fname})
    elif designation.lower() == 'visitor':
        return redirect('visitor')

def crud(request):

    if request.method == 'POST':
        book = request.POST.get('search')
        try:
            bookexist = BookRecords.objects.get(title=book)
        except BookRecords.DoesNotExist:
            bookexist = None

        if bookexist is not None:
            euid = bookexist.id
            return redirect(f'{euid}/update')
        else:
            return redirect('create')

    return redirect('home')

class RecCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = 'login'
    model = BookRecords
    #form = EntryForm()
    #context = {'form':form}
    template_name = 'libManager/create.html'
    fields = ['title', 'copies_avail', 'tags']

    def test_func(self):
        return self.request.user.designation.lower() == 'librarian'

    def handle_no_permission(self):
        messages.error(self.request, "You Need To Be A Librarian To Do That!!")
        return redirect('home')

class RecUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = BookRecords
    login_url = 'login'
    #form = EntryForm()
    #context = {'form':form}
    template_name = 'libManager/update.html'
    fields = ['title', 'copies_avail', 'tags']

    def test_func(self):
        return self.request.user.designation.lower() == 'librarian'

    def handle_no_permission(self):
        messages.error(self.request, "You Need To Be A Librarian To Do That!!")
        return redirect('home')

class RecListView(ListView):

    model = BookRecords
    template_name = 'libManager/visitor.html'
    ordering = ['title']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def new_entry(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        copies_avail=request.POST.get('copies_avail')
        tags=request.POST.get('tags')
        bookn = BookRecords(title=title, copies_avail=copies_avail, tags=tags, copies_tot = copies_avail)
        bookn.save()
    
    return redirect('home')

def change_entry(request, pk):
    if request.method == 'POST':
        ch = request.POST.get('choice')
        username = request.POST.get('username')
        bookDetails = BookRecords.objects.get(id=pk)
        user = User.objects.get(username = username)
        if ch == 'issue':
            if user.is_active:
                if bookDetails.copies_avail>0:
                    if user.books_issued_curr<user.issue_limit:
                        if user.dues==0:
                            bookDetails.curr_issuers.add(user)
                            bookDetails.copies_avail-=1
                            user.books_issued_curr+=1
                            bookDetails.save()
                            user.save()
                            messages.success(request, 'Issue Successful!!')
                        else:
                            messages.error(request, 'Sorry! User Has Pending Dues!!')
                    else:
                        messages.error(request, 'Sorry! User Has Reached Your Issue Limit!!')
                else:
                    messages.error(request, 'Sorry! No More Copies Available For Issue!!')
            else:
                messages.error(request, 'Sorry! User Account Not Active!!')
        else:
            bookDetails.copies_avail+=1
            user.books_issued_curr-=1
            bookDetails.prev_issuers.add(user)
            bookDetails.curr_issuers.remove(user)
            bookDetails.save()
            user.save()
            messages.success(request, 'Return Successful!!')
        
    return redirect('crud')
