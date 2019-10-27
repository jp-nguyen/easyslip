import os
from os import path
import base64
import re
import json
from docusign_esign import *
from dotenv import load_dotenv
from datetime import datetime,timedelta
#loading environment variables
load_dotenv()

#get path to document
docs_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), os.getenv("DOCUMENT_PATH")))

def get_docusign_credentials():
    """
    1. Creates docusign credentials from .env file
    """

    args = {
        "account_id": os.getenv("ACCOUNT_ID"),
        "base_path": os.getenv("BASE_PATH"),
        "ds_access_token": os.getenv("DS_ACCESS_TOKEN"),
    }
    return args
    
def send_slip_worker(cred_info, env_info, document_name):
    """
    1. Create the envelope request object
    2. Send the envelope
    """
    api_client = ApiClient()
    api_client.host = cred_info["base_path"]
    api_client.set_default_header("Authorization", "Bearer " + cred_info["ds_access_token"])
    
    workflow_details = AccountsApi(api_client)
    workflow_response = workflow_details.get_account_identity_verification(cred_info["account_id"])
    workflow_id = workflow_response.identity_verification[0].workflow_id
    
    
    envelope_definition = make_envelope(env_info, document_name, workflow_id)
    envelopes_api = EnvelopesApi(api_client)
    result = envelopes_api.create_envelope(cred_info["account_id"], envelope_definition=envelope_definition)
    envelope_id = result.envelope_id
    return { "envelope_id" : envelope_id }

def make_envelope(env_info, document_name, workflow_id):
    """
    Creates envelope with a given document.
    Example env 
    envelope_args = {
        "signer_email":<email>,
        "signer_name": <name>,
        "status": <sent>,
        "child_name": <child>
    }
    """
    # create the envelope definition
    env = EnvelopeDefinition(
        email_subject="EasySlip: Please sign this document!"
    )
   
    # The reads could raise an exception if the file is not available!
    with open(path.join(docs_path, document_name), "rb") as file:
        doc_pdf_bytes = file.read()
    doc_b64 = base64.b64encode(doc_pdf_bytes).decode("ascii")

    # Create the document models
    document = Document(  # create the DocuSign document object
        document_base64 =doc_b64,
        name = ''.join(env_info["child_name"].split(' ')) + "_FieldTrip",  # can be different from actual file name
        file_extension = "pdf",  # many different document types are accepted
        document_id = "1" # a label used to reference the doc
    )
    # The order in the docs array determines the order in the envelope
    env.documents = [document]

    # Create the signer recipient model
    signer = Signer(
        email = env_info["signer_email"], 
        name = env_info["signer_name"],
        recipient_id = "1", 
        routing_order = "1",
        identity_verification = { "workflowId" : workflow_id, "steps": "null" },
    )

    # Create the CC recipient to receive a copy of the documents
    cc = CarbonCopy(
        email = env_info["cc_email"],
        name = env_info["cc_name"],
        recipient_id = "2", 
        routing_order = "2"
    )

    sign_here = SignHere(
        anchor_string = "/sn1/", 
        anchor_units = "pixels",
        anchor_y_offset = "0", 
        anchor_x_offset = "0"
    )

    parent_full_name = FullName(
        anchor_string = "/pn0/",
        anchor_units = "pixels",
        anchor_y_offset = "-5",
        anchor_x_offset = "-10"
    )
    
    child_full_name = Text(
        value = env_info["child_name"],
        anchor_string = "/cn0/",
        anchor_units = "pixels",
        anchor_y_offset = "-5", 
        anchor_x_offset = "-10"
    )

    current_date = DateSigned(
        anchor_string = "/dn1/",
        anchor_units = "pixels",
        anchor_y_offset = "0", 
        anchor_x_offset = "-25"
    )

    signer.tabs = Tabs(
        sign_here_tabs = [sign_here], 
        full_name_tabs = [parent_full_name],
        text_tabs = [child_full_name],
        date_signed_tabs= [current_date]
    )

    # Add the recipients to the envelope object
    recipients = Recipients(
        signers = [signer],
        carbon_copies = [cc]
    )
    env.recipients = recipients

    # Request that the envelope be sent by setting |status| to "sent".
    env.status = env_info["status"]
    return env

def list_recipients(cred_info, envelope_id):
    """
    1. Call the envelope recipients list method
    """
    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = cred_info["base_path"]
    api_client.set_default_header("Authorization", "Bearer " + cred_info["ds_access_token"])
    envelope_api = EnvelopesApi(api_client)
    from_date = (datetime.utcnow() - timedelta(days=10)).isoformat()
    results = envelope_api.list_status_changes(cred_info["account_id"], from_date = from_date)

    return results

def get_signed_envelope_ids(results):
    """
    1. Returns a list of envelope_ids where the status is completed, i.e. signed.
    """
    return [e.envelope_id for e in results.envelopes if e.status == "completed"]

if __name__ == "__main__":
    cred_info = get_docusign_credentials()
    env_info = {
        "signer_email": os.getenv("SIGNER_EMAIL"),
        "signer_name": os.getenv("SIGNER_NAME"),
        "status": "sent",
        "child_name": os.getenv("CHILD_NAME"),
        "cc_email": os.getenv("CC_EMAIL"),
        "cc_name": os.getenv("CC_NAME")
    }
    print(cred_info)
    envelope_id = send_slip_worker(cred_info, env_info, document_name="permission-slip-final.pdf")
    print(envelope_id)
    results = list_recipients(cred_info, envelope_id["envelope_id"])
    print(get_signed_envelope_ids(results))