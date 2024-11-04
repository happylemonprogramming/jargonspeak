import resend
import os

resend.api_key = os.environ.get('resendtestkey')

def send_email(to, subject, body):
  email = resend.Emails.send({
    "sender": "nedry@nublar.co",
    "to": [to],
    "subject": subject,
    "html": body
  })
  return email.id


if __name__ == "__main__":
  print(send_email("claytonlemons@live.com","Hello!", "Thank you for using our service!"))