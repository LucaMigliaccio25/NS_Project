import os
from mailjet_rest import Client
from dotenv import load_dotenv

# Load environment variables for Mailjet API credentials
load_dotenv(dotenv_path="mailjet_key.env")

def create_email_content(wallet):
    """
    Generates the email body with wallet details for the recipient.
    """
    return f"""
    Hello,

    Your new NFT has been successfully created. Below are your wallet details:

    **Address**: {wallet.address}
    **Seed**: {wallet.seed}

    Please store these credentials securely as they grant full access to your wallet.

    Best regards,
    The DIADEN Team
    """

def send_email(subject, recipient_email, sender_email, wallet):
    """
    Sends an email using the Mailjet API.
    """
    # Retrieve API credentials from environment variables
    api_key = os.getenv("MAILJET_API_KEY")
    api_secret = os.getenv("MAILJET_API_SECRET")

    # Validate credentials
    if not api_key or not api_secret:
        raise ValueError("Mailjet API credentials are missing. Please set them in environment variables.")

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    # Email data
    body = create_email_content(wallet=wallet)
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "DIADEN"
                },
                "To": [
                    {
                        "Email": recipient_email
                    }
                ],
                "Subject": subject,
                "TextPart": body
            }
        ]
    }

    # Send email and handle response
    result = mailjet.send.create(data=data)
    if result.status_code != 200:
        raise Exception(f"Email failed to send: {result.json()}")
    return result.json()
