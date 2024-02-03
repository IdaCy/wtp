from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def legal_disclaimer(request):
    return render(request, 'legal_disclaimer.html')

@login_required
def contact(request):
    if request.method == 'POST':
        user = request.user
        #sender_email = request.POST.get('email')
        message_content = request.POST.get('message')

        # Prepare the email
        subject = 'New Contact Form Submission'
        message = f"From: {user.username} ({user.email})\n\nMessage:\n{message_content}"
        recipient_list = [settings.EMAIL_RECIPIENT]

        # Send the email
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        messages.success(request, f"Thank you, {user.username}, for your message!")
        return redirect('contact')

    return render(request, 'contact.html', {'email_address': settings.EMAIL_HOST_USER})
