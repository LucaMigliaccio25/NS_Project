// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Import dei contratti di OpenZeppelin direttamente da github
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.9.0/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.9.0/contracts/access/Ownable.sol";

/// @title DynamicNFT
/// @notice Smart Contract per creare un NFT dinamico che rappresenta un avatar (con metadati variabili)
contract DynamicNFT is ERC721URIStorage, Ownable {
    
    // contatore per assegnare ID unici agli NFT
    uint256 private tokenCounter;

    // evento per tracciare la creazione di un NFT
    event NFTCreated(uint256 indexed tokenId, string tokenURI);

    // evento per aggiornare i metadati dell'NFT creato
    event MetadataUpdated(uint256 indexed tokenId, string newTokenURI);

    /// @notice Costruttore per inizializzare il contratto
    /// @dev Inizializzazione di nome e simbolo del token
    constructor() ERC721("DynamicNFT", "DNFT") {
        tokenCounter = 0; // inizialmente dev'essere pari a 0
    }

    /// @notice Funzione per creare un nuovo NFT
    /// @param recipient è l'indirizzo che riceverà l'NFT
    /// @param tokenURI è l'URI iniziale dei metadati dell'NFT
    /// @return tokenId è l'ID dell'NFT creato
    function createNFT(address recipient, string memory tokenURI) public onlyOwner returns (uint256)
    {
        uint256 newTokenId = tokenCounter; // assegniamo il valore del contatore all'ID del nuovo token
        _safeMint(recipient, newTokenId); // creiamo l'NFT e lo assegniamo al destinatario
        _setTokenURI(newTokenId, tokenURI); // assegniamo i metadati iniziali
        emit NFTCreated(newTokenId, tokenURI); // emissione dell'evento di creazione dell'NFT (Log)
        tokenCounter += 1; // incrementiamo il contatore per i futuri NFT
        return newTokenId;
    }

    /// @notice Funzione per aggiornare i metadati di un NFT esistente
    /// @param tokenId è l'ID dell'NFT da aggiornare
    /// @param newTokenURI è il nuovo URI dei metadati
    function updateMetadata(uint256 tokenId, string memory newTokenURI) public {
        require(_existsInternal(tokenId), "Token ID does not exist");
        require(ownerOf(tokenId) == msg.sender, "Only the owner can update metadata");
        _setTokenURI(tokenId, newTokenURI); // aggiorniamo i metadati
        emit MetadataUpdated(tokenId, newTokenURI); // emissione dell'evento di aggiornamento (Log)
    }

    /// @notice Funzione che verifica se un token esiste
    /// @param tokenId è l'ID del token da verificare
    /// @return true se il token esiste, altrimenti false
    function _existsInternal(uint256 tokenId) internal view returns (bool) {
        try this.ownerOf(tokenId) {
            return true;
        } catch {
            return false;
        }
    }
}