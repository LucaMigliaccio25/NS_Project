from utils import create_and_transfer_nft, update_nft_metadata
import os

# Percorso della cartella "data/metadata"
cartella_metadata = os.path.join('data', 'metadata')

# Nome del file JSON che vuoi leggere
avatar_uri_0 = 'metadata_arciera.json'
avatar_uri_1 = 'metadata_cavaliere.json'
avatar_uri_2 = 'metadata_stregone.json'

# Percorso completo del file JSON
path_avatar_uri_0 = os.path.join(cartella_metadata, avatar_uri_0)
path_avatar_uri_1 = os.path.join(cartella_metadata, avatar_uri_1)
path_avatar_uri_2 = os.path.join(cartella_metadata, avatar_uri_2)

# Percorso completo del file JSON (avatar aggiornati)
path_avatar_uri_0 = os.path.join(cartella_metadata, 'metadata_arciera_update.json')
path_avatar_uri_1 = os.path.join(cartella_metadata, 'metadata_cavaliere_update.json')
path_avatar_uri_2 = os.path.join(cartella_metadata, 'metadata_stregone_update.json')

if __name__ == '__main__':
    try:
        # Creazione NFT su Ethereum
        token_id, token_uri = create_and_transfer_nft(avatar_uri_2)
        # print("Everything ok")
        # print(f"{wallet_receiver, NFT_token_id = }")
        print(f"Ethereum: NFT dinamico creato.")
        print(f"TOKEN ID: {token_id}\n")
        print(f"TOKEN URI: {token_uri}\n")
        
        # Aggiornamento dei metadati dell'NFT
        # token_id = 0 # Token ID dell'NFT dinamico (possibile specificarlo)
        new_metadata_uri = path_avatar_uri_2
        update_receipt = update_nft_metadata(token_id, new_metadata_uri)
        print(f"Metadati aggiornati per il token {token_id}: {update_receipt}")
    
    except Exception as e:
        print(f"Errore durante la creazione o l'aggiornamento: {e}")