import imaplib
import getpass
import smtplib
import email

smtp_object = smtplib.SMTP('smtp.gmail.com',587)
smtp_object.ehlo()
smtp_object.starttls()

print('WELCOME TO EMAIL_CHECKER'.center(40,'='),'\n by:thomas otte correa','\n \n')

# IMAP server details
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Email account credentials
EMAIL_ADDRESS = input('Email Address: ')
EMAIL_PASSWORD =  getpass.getpass('Email Password: ') 

def fetch_last_10_emails():
    # Connect to the IMAP server
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    imap.select('inbox')

    # Retrieve the last 10 emails
    _, data = imap.search(None, 'ALL')
    email_ids = data[0].split()
    email_ids = email_ids[-10:]  # Get the last 10 email IDs

    emails = []
    for email_id in email_ids:
        _, data = imap.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        emails.append(email_message)

    imap.close()
    imap.logout()

    return emails


def display_emails(emails):
    for i, email_message in enumerate(emails, start=1):
        print(f'Email {i}:')
        print(f'From: {email_message["From"]}')
        print(f'Subject: {email_message["Subject"]}')
        print('---')

def view_email(emails):
    index = int(input('Enter the index of the email to view: ')) - 1
    selected_email = emails[index]

    print('--- Email Content ---')
    print(f'From: {selected_email["From"]}')
    print(f'To: {selected_email["To"]}')
    print(f'Subject: {selected_email["Subject"]}')
    print()
    for part in selected_email.walk():
        if part.get_content_type() == 'text/plain':
            print(part.get_payload(decode=True).decode('utf-8'))
            print()
    
    return selected_email


def reply_to_email(selected_email):
    reply_subject = 'RE: ' + selected_email['Subject']
    reply_body = input('Enter your reply: ')

    # Create the reply email
    reply_email = email.message.EmailMessage()
    reply_email['Subject'] = reply_subject
    reply_email['From'] = EMAIL_ADDRESS
    reply_email['To'] = selected_email['Reply-To'] or selected_email['From']
    reply_email.set_content(reply_body)

    # Connect to the SMTP server and send the reply email
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(reply_email)
    smtp.quit()

    print('Reply sent successfully!')


def run():

    c_opt = False #check if the user selected 1 or 2 only 
    while c_opt == False:
        choice_send_read = input('To SEND an email enter "1"; \nTo READ your emails enter "2";\nTo STOP enter "3"; ')

        if choice_send_read == "1": #to SEND emails

            send_email = email.message.EmailMessage()
            send_email['To'] = input('Enter the email you want to send to: ')
            send_email['Subject'] = input("Enter your Subject: ")
            send_body = input('Enter your reply: ')
            send_email['From'] = EMAIL_ADDRESS
            send_email.set_content(send_body)

            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(send_email)
            print('\n','EMAIL SENT SUCCESSFULLY'.center(40,'='),'\n')
            smtp.quit()

        
        elif choice_send_read == "2": #to READ emails
            # Fetch and display the last 10 emails
            emails = fetch_last_10_emails()
            display_emails(emails)
            view_choice = input('Do you want to view any email?(yes or no) ')  #choice to view 

            if view_choice == 'yes':
                # View and reply to a selected email
                selected_email = view_email(emails)
                reply_choice = input('Do you want to reply to this email?(yes or no) ')

                if reply_choice == 'yes':
                    reply_to_email(selected_email)
                

            elif view_choice == 'no':
                print("no")
                

        elif choice_send_read == "3": #to BREAK
            break
        else:
            print('\n','INCORRECT INPUT'.center(40,'='))


        
run()
