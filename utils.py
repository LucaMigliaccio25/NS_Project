# CODICE PROGETTO XRPL
from xrpl.account import get_balance, get_next_valid_seq_number
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.core import keypairs
from xrpl.transaction import sign, submit_and_wait, XRPLReliableSubmissionException
from xrpl.models import Payment
from xrpl.models.transactions import NFTokenMint, NFTokenCreateOffer, NFTokenAcceptOffer
from xrpl.utils import str_to_hex, datetime_to_ripple_time
from xrpl.ledger import get_latest_validated_ledger_sequence
from datetime import datetime, timedelta
from dotenv import load_dotenv

client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

def _generate_xrpl_wallet_seed() -> str:
    """
    Generate a random seed. Notice that if you create a wallet with this seed, it won't be a working wallet, because you need to fund it before. See https://xrpl.org/docs/concepts/accounts#creating-accounts.
    """
    return keypairs.generate_seed()

def get_wallet(seed: str | None = None) -> Wallet:
    """
    Generate a wallet.
    """
    if seed:
        wallet = Wallet.from_seed(seed)
    else:
        wallet = generate_faucet_wallet(client, debug=True)
    return wallet

def print_balances(wallets: list, client: JsonRpcClient) -> None:
    """
    Print the balances of wallets.
    """
    print("Balances:")
    for wallet in wallets:
        print(f"{wallet.address}: {get_balance(wallet.address, client)}")

def mint_nft_token(seed, uri, flags, transfer_fee, taxon):
    minter_wallet=Wallet.from_seed(seed)
    mint_tx=NFTokenMint(
        account=minter_wallet.address,
        uri=str_to_hex(uri),
        flags=int(flags),
        transfer_fee=int(transfer_fee),
        nftoken_taxon=int(taxon)
    )
    response=""
    try:
        response=submit_and_wait(mint_tx,client,minter_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response

def create_sell_offer(seed, amount, nftoken_id, expiration, destination):
    owner_wallet = Wallet.from_seed(seed)
    expiration_date = datetime.now()
    if expiration != '':
        expiration_date = datetime_to_ripple_time(expiration_date)
        expiration_date = expiration_date + int(expiration)
    sell_offer_tx=NFTokenCreateOffer(
        account=owner_wallet.address,
        nftoken_id=nftoken_id,
        amount=amount,
        destination=destination if destination != '' else None,
        expiration=expiration_date if expiration != '' else None,
        flags=1
    )
    response=""
    try:
        response=submit_and_wait(sell_offer_tx,client,owner_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response

def accept_sell_offer(seed, offer_index):
    buyer_wallet=Wallet.from_seed(seed)
    accept_offer_tx=NFTokenAcceptOffer(
       account=buyer_wallet.classic_address,
       nftoken_sell_offer=offer_index
    )
    try:
        response=submit_and_wait(accept_offer_tx,client,buyer_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response

MIN_AMOUNT = "2000"
MIN_FEE = "20"

#----------------------------------------------------------------------------------------------------
# CODICE PROGETTO ETHEREUM-XRPL
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

def create_and_transfer_nft(seed_company, product_uri, avatar_uri, taxon, seed_receiver = None, chain_url = "https://s.altnet.rippletest.net:51234"):
    try:
        client=JsonRpcClient(chain_url)

        wallet_company = get_wallet(seed_company)
        seed_company = wallet_company.seed
        
        flag = 8
        transfer_fee = 0
        response_mint_token = mint_nft_token(
                seed_company,
                product_uri,
                flag,
                transfer_fee,
                taxon
            )
        # print(f"{response_mint_token = }")
        NFT_token_id = response_mint_token['meta']['nftoken_id'] 

        wallet_receiver = get_wallet(seed_receiver)
        seed_receiver = wallet_receiver.seed
        # print(f"{seed_receiver = }")

        # Create account by sending funds
        current_validated_ledger = get_latest_validated_ledger_sequence(client)

        tx_payment = Payment(
            account=wallet_company.address,
            amount=MIN_AMOUNT,
            destination=wallet_receiver.address,
            last_ledger_sequence=current_validated_ledger + 20,
            sequence=get_next_valid_seq_number(wallet_company.address, client),
            fee=MIN_FEE,
        )
        my_tx_payment_signed = sign(tx_payment, wallet_company)
        tx_response = submit_and_wait(my_tx_payment_signed, client)

        # print_balances([wallet_company, wallet_receiver], client)

        # Create Sell Offer for the receiver account with amount 0 and accept it
        current_time = datetime.now()
        expiration_time = current_time + timedelta(minutes=60)
        expiration_time = datetime_to_ripple_time(expiration_time)

        response_sell_offer = create_sell_offer(seed_company, '0', NFT_token_id, expiration=expiration_time, destination=wallet_receiver.address)
        # print(f"{response_sell_offer = }")
        sell_offer_ledger_index = response_sell_offer['meta']['offer_id']

        # Accept sell offer of company by receiver
        response_accept_sell_offer = accept_sell_offer(seed_receiver, sell_offer_ledger_index)
        # print(f"{response_accept_sell_offer = }")

        if not response_accept_sell_offer['meta']['TransactionResult'] == 'tesSUCCESS':
            raise Exception(f'Didn\'t work: {e}')
        
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
    
        return wallet_receiver, NFT_token_id, token_id, token_uri
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