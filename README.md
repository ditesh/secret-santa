*Automated Secret Santa*

The Automated Secret Santa program takes in a list of email addresses and template email to send, randomizes the email addresses, and sends off the secret santa details to the receipient.

Example usage:

./secret-santa.py -e emails -a attachment -H smtp.gmail.com -p 587 -u myusername -p mypassword

where emails is the file containing a list of email addresses (one per line) in the format: "Ditesh Kumar" <ditesh@gathani.org>
and attachment is a file containing the template HTML email to be sent to the receipient (use placeholder variables ${santa} and ${receipient})
