from web3 import Web3
import os
from dotenv import load_dotenv
import json

# Caricamento delle variabili d'ambiente
load_dotenv(dotenv_path="private_data.env")

# Configurazione di QuickNode (Ethereum)
quicknode_url = os.getenv("QUICKNODE_URL")
web3 = Web3(Web3.HTTPProvider(quicknode_url))
if not web3.is_connected():
    raise Exception("--- Connessione a QuickNode fallita! ---")

contract_address = os.getenv("CONTRACT_ADDRESS")
with open("dynamic_nft_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
private_key = os.getenv("PRIVATE_KEY_METAMASK")

# definizione funzione per la creazione di NFT dinamico su Ethereum
def trigger_ethereum_nft(uri, owner_address):
    """
    Trigger the Ethereum smart contract to create a dynamic NFT.
    """
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    
    # Ottiene il gas price dinamico ed applica un incremento minimo
    current_gas_price = web3.eth.gas_price
    adjusted_gas_price = current_gas_price + web3.to_wei('2', 'gwei')  # Aggiunta di 2 gwei come incremento

    # Stampa di debug
    print(f"Utilizzando gas price: {web3.from_wei(adjusted_gas_price, 'gwei')} gwei")

    # Creazione dell'NFT su Ethereum
    txn = contract.functions.createNFT(owner_address, uri).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 300000,  # Limite di gas
        'gasPrice': adjusted_gas_price  # Gas price regolato
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Transazione inviata su Ethereum: {web3.to_hex(tx_hash)}")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transazione confermata")
    # print(f"Transazione confermata: {receipt}")
    return receipt

# definizione funzione per la verifica della corretta creazione di un NFT
def verify_nft(token_id):
    """
    Verifica l'esistenza dell'NFT e recupera l'URI del token.
    """
    try:
        # Recupera il tokenURI
        token_uri = contract.functions.tokenURI(token_id).call()
        print(f"Token ID: {token_id}, Token URI: {token_uri}")
        return token_uri
    except Exception as e:
        print(f"Errore nella verifica dell'NFT: {e}")
        return None

def create_and_transfer_nft(avatar_uri):
    try:
        # Trigger del contratto Ethereum
        print("Attivazione del contratto Ethereum...")
        account_address = "0x0CbB29c4659DB51384fA809e0a7b7147c315DC4c" # indirizzo Metamask
        receipt = trigger_ethereum_nft(avatar_uri, account_address)
        # print(f"Dati receipt: {receipt}")
        print("NFT dinamico creato su Ethereum.")
        
        # Recupera il token_id dai log
        logs = contract.events.NFTCreated().process_receipt(receipt)
        for log in logs:
            token_id = log['args']['tokenId']
            print(f"Token ID: {token_id}")
        
        # Verifica l'NFT appena creato
        token_uri = verify_nft(token_id)
    
        return token_id, token_uri
    except Exception as e:
        raise Exception(f'Didn\'t work: {e}')

# definizione funzione per aggiornare i metadati del digital twin (avatar) associato all'NFT creato
def update_nft_metadata(token_id, new_uri):
    """
    Aggiorna i metadati di un NFT esistente.
    """
    try:
        account = web3.eth.account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(account.address)

        # Ottieni il gas price corrente e aumentalo leggermente
        current_gas_price = web3.eth.gas_price
        adjusted_gas_price = int(current_gas_price * 1.1)  # Aumenta del 10%
        print(f"Utilizzando gas price: {web3.from_wei(adjusted_gas_price, 'gwei')} gwei")

        # Transazione per aggiornare i metadati
        txn = contract.functions.updateMetadata(token_id, new_uri).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 300000,  # Limite di gas regolabile
            'gasPrice': adjusted_gas_price
        })

        # Firma e invio della transazione
        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        print(f"Transazione inviata per aggiornare i metadati: {web3.to_hex(tx_hash)}")
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Metadati aggiornati: {receipt}")
        return receipt
    except Exception as e:
        print(f"Errore durante l'aggiornamento dei metadati: {e}")
        return None