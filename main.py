from utils import create_and_transfer_nft, update_nft_metadata

# dati per XRPL
seed_company = "sEd7uhRLEHf7sELoTUiKTcDwgn3zvdA"
seed_receiver = "sEd7vJWGo5cYxju2raWQ1yQSFPgVejN"
product_uri = "https://diadenn.vercel.app/product/mike-wind-1"
taxon = 0

# URI dell'avatar associato all'NFT dinamico
avatar_uri = "https://drive.google.com/file/d/1hjWW9yfOnPk1rlcLcjg4ycADWvacXrQy/view?usp=drive_link"

if __name__ == '__main__':
    try:
        # Creazione NFT su XRPL e Ethereum
        wallet_receiver, NFT_token_id, token_id, token_uri = create_and_transfer_nft(seed_company, product_uri, avatar_uri, taxon, seed_receiver=seed_receiver)
        # print("Everything ok")
        # print(f"{wallet_receiver, NFT_token_id = }")
        print(f"Creazione completata:\nXRPL: {NFT_token_id}\nEthereum: NFT dinamico creato.")
        print(f"TOKEN ID: {token_id}\n")
        print(f"TOKEN URI: {token_uri}\n")
        
        # Aggiornamento dei metadati dell'NFT
        # token_id = 0 # Token ID dell'NFT dinamico (possibile specificarlo)
        new_metadata_uri = "https://drive.google.com/file/d/1fO30hSD1ZExxBIa4tY2QDbdGD1zhoJ3t/view?usp=drive_link"
        update_receipt = update_nft_metadata(token_id, new_metadata_uri)
        print(f"Metadati aggiornati per il token {token_id}: {update_receipt}")
    
    except Exception as e:
        print(f"Errore durante la creazione o l'aggiornamento: {e}")