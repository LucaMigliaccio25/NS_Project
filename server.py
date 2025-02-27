from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from typing import Optional
from utils import create_and_transfer_nft  # Funzione per creare e trasferire l'NFT
from email_utils import send_email  # Modulo separato per l'invio di email
import uvicorn
from random import choice
from string import ascii_letters

# Costanti del progetto
BASE_URL = "http://127.0.0.1:5000"  # URL base per il metadata dell'NFT
seed_company = "sEd7uhRLEHf7sELoTUiKTcDwgn3zvdA"  # Seed del wallet aziendale per la creazione di NFT
ALPHABET = ascii_letters  # Alfabeto per generare URI casuali
COMPANY_EMAIL =  "kings@diaden.com"  # Email del mittente

# Creazione dell'app FastAPI
app = FastAPI()

# Modello per la richiesta al servizio
class NFTTransferRequest(BaseModel):
    taxon: int  # Categoria dell'NFT
    email_receiver: str  # Email del destinatario

@app.post("/nft/")
def create_and_transfer_nft_endpoint(request: NFTTransferRequest):
    """
    Endpoint per creare un NFT, trasferirlo e inviare un'email di conferma.
    """
    chain_url = "https://s.altnet.rippletest.net:51234"  # URL del nodo XRPL
    # Generazione casuale di un URI per l'NFT
    product_uri = BASE_URL + "/" + "".join([choice(ALPHABET) for _ in range(10)])

    try:
        # Creazione e trasferimento dell'NFT
        wallet_receiver, NFT_token_id = create_and_transfer_nft(
            seed_company=seed_company,
            product_uri=product_uri,
            taxon=int(request.taxon),
            chain_url=chain_url,
        )

        # Invio dell'email al destinatario
        result = send_email(
            subject="I dettagli del tuo acquisto NFT",
            sender_email=COMPANY_EMAIL,
            recipient_email=request.email_receiver,
            wallet=wallet_receiver
        )
        print(f"Risultato dell'invio email: {result}")

        # Risposta in caso di successo
        return {
            "status": "success",
            "NFT": NFT_token_id,
            "message": "NFT creato e trasferito con successo."
        }

    except Exception as e:
        # Gestione degli errori
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    # Avvio del server FastAPI
    uvicorn.run("server:app", port=5000, log_level="info")