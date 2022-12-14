import email
import imaplib
import os
import schedule
import time

def check_ultramanorder():
    # Connect to Gmail and select the inbox
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('youaccount@gmail.com', 'yourapppasswords')
    mail.select('inbox')

    # Search for email with the specified subject
    typ, data = mail.search(None, '(UNSEEN) SUBJECT "Ultraman order"')
    print ('searching')

    # Loop through the messages that were found
    for num in data[0].split():
        print (num)
        # Fetch the raw message data
        typ, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        # Loop through all attachments in the message
        for part in msg.walk():
            # If the part is an attachment, save it to the specified folder
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if not filename:
                continue

            # Save the attachment to the specified folder
            att_path = os.path.join(r"C:\Users\blues\Documents\AUTOMATION\Ultraman\order received", filename)
            with open(att_path, 'wb') as fp:
                fp.write(part.get_payload(decode=True))
            print ('attachment saved')

    # Close the connection to Gmail
    mail.close()
    mail.logout()

def countdown():
   # Calculate the time remaining until the next scheduled execution
    next_run_timestamp = schedule.next_run().timestamp()  # Convert the datetime value to a float timestamp
    remaining = next_run_timestamp - time.time()  # Subtract the float timestamp from the current time

    # Convert the remaining time to minutes and seconds
    minutes, seconds = divmod(remaining, 60)
    
    # Display the time remaining until the next scheduled execution
    print(f"Next scheduled execution in {minutes:.0f} minutes and {seconds:.0f} seconds")

def main():
    print ('Program Started')
    # Schedule the task to run every 5 minutes
    schedule.every(1).minutes.do(check_ultramanorder)

    # Run the scheduler in an infinite loop
    while True:
        schedule.run_pending()
        countdown()  # Display the countdown
        time.sleep(1)  # Pause for 1 second
        
if __name__ == "__main__":
    main()


