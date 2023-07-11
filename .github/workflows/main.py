import os
import requests
import logging
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    old_hubspot_token = os.environ.get("OLD_HUBSPOT_API_TOKEN")
    new_hubspot_token = os.environ.get("NEW_HUBSPOT_API_TOKEN")

    old_hubspot_endpoint = f"https://api.hubapi.com/contacts/v1/lists/all/contacts/recent?hapikey={old_hubspot_token}"
    new_hubspot_endpoint = f"https://api.hubapi.com/contacts/v1/contact?hapikey={new_hubspot_token}"

    try:
        response = requests.get(old_hubspot_endpoint)
        response.raise_for_status()
        contacts = response.json().get("contacts", [])

        for contact in contacts:
            contact_data = {
                "properties": [
                    {"property": "email", "value": contact.get("email", "")},
                    {"property": "firstname", "value": contact.get("firstname", "")},
                    {"property": "lastname", "value": contact.get("lastname", "")}
                    # Add more properties as needed
                ]
            }

            response = requests.post(new_hubspot_endpoint, json=contact_data)
            response.raise_for_status()

            logging.info(f"Contact created successfully: {contact.get('email')}")

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
