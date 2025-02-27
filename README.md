# Dynamic NFT Project - XRPL & Ethereum

Questo progetto implementa un'applicazione decentralizzata (dApp) che utilizza uno smart contract su Ethereum per la gestione di NFT dinamici (Dynamic NFT). È possibile creare e aggiornare NFT tramite un'interfaccia frontend sviluppata con Streamlit, interagendo con la blockchain attraverso la libreria Web3 e QuickNode. In particolare, vi è una cross chain tra XRPL ed Ethereum, in quanto la creazione dell'NFT dinamico è vincolata alla creazione dell'NFT su XRPL.
L'idea alla base di questa progetto nasce dal voler associare all'NFT un Digital Twin (come, ad esempio, un avatar), del quale è poi possibile andare ad aggiornare i metadati associati. Quindi, nel caso dell'avatar, all'atto della creazione dell'NFT si avrà la corrispondente creazione del personaggio e, se il giocatore lo desidera, può aggiornare i metadati. Ciò, nel nostro caso, corrisponde a far "evolvere l'avatar".

## Struttura del progetto
Il progetto è organizzato come segue:

- data/: cartella contenente dati statici per immagini e metadati.
    - images/: immagini associate agli NFT.
    - metadata/: metadati JSON associati agli NFT.
- env/: directory dell'ambiente virtuale Python.
- img/: cartella contenente le immagini del README.
- .gitignore: file per escludere file o directory specifici dal commit (es. env/, file .env).
- app.py: frontend basato su Streamlit per creare e aggiornare NFT.
- dynamic_nft_abi.json: file JSON contenente l'ABI (Application Binary Interface) del contratto Ethereum.
- Dynamic_NFT.sol: contratto smart Ethereum per la gestione di NFT dinamici.
- email_utils.py: modulo per inviare email tramite l'API di Mailjet.
- mailjet_key.env: file di configurazione contenente le chiavi API di Mailjet (escluso dal commit).
- main.py: script principale per la gestione di NFT su XRPL ed Ethereum.
- private_data.env: file di configurazione contenente le credenziali Ethereum (es. chiavi private, escluso dal commit).
- README.md: documentazione principale del progetto, incluse istruzioni per l'installazione e l'uso.
- requirements.txt: elenco delle dipendenze Python necessarie al progetto.
- server.py: server basato su FastAPI per gestire le richieste API.
- test_func.py: script per testare funzionalità XRPL come creazione di wallet, NFT, e offerte.
- utils.py: modulo con funzioni di supporto per l'interazione con XRPL ed Ethereum (ad esempio, funzioni per creare e aggiornare NFT).

Di seguito riportiamo i passaggi che sono stati seguiti durante lo sviluppo del progetto e i dettagli ad essi associati.

## 1. Copia dei file della vecchia repository
Questo progetto è stato implementato sulla base di un altro, sviluppato per la realizzazione di NFT esclusivamente su XRPL. Dunque, la prima fase consiste nel fare la clone della repository associata. Il comando è il seguente:

```
git clone https://github.com/LucaMigliaccio25/Project_XRPL_NFT
```

N.B. Non è necessario effettuare la clone di tutti i file della repository. Quelli indispensabili sono:
- main.py
- utils.py
- requirements.txt
- .gitignore

## 2. Configurazione dell'ambiente virtuale
Per isolare le dipendenze del progetto:

```
python -m venv env
.\env\Scripts\activate
```

## 3. Aggiornamento del file requirements.txt
È stato necessario aggiornare il file requirements.txt. L'utente può utilizzare quello fornito nella repository utilizzando il seguente comando:

```
pip install -r requirements.txt
```

## 4. Test dello Smart Contract
Il test del corretto funzionamento delle funzionalità dello smart contract (Dynamic_NFT.sol) è stato effettuato nell'IDE Remix, in quanto la versione light di Remix integrata in Visual Studio Code non supporta in maniera ottimale l'esecuzione degli smart contract.
Per poter effettuare correttamente il test è necessario:
- avere un account Metamask (wallet Ethereum utilizzato per firmare transazioni e connettersi a dApps);
- configurarlo aggiungendo la testnet Sepolia (assicurarsi di avere del test ETH);
- utilizzare Remix IDE (possibile copiare il codice presente in Dynamic_NFT.sol);

Una volta creato lo smart contract:
- andare nella sezione Solidity Compiler > Compile Dynamic_NFT.sol;
- andare nella sezione Deploy and run transactions > Deployed Contracts (qui troveremo il nostro contratto). In questa sezione è possibile testare le funzioni presenti all'interno del contratto.

Per verificare che le operazioni vadano a buon fine, è possibile utilizzare Etherscan: strumento utile per cercare transazioni, indirizzi di wallet, smart contract ed altro sulla blockchain di Ethereum. Di seguito, sono presenti degli esempi di test delle funzioni presenti nello smart contract (visualizzati su Etherscan):

### 4.1. Test Creazione dell'NFT
![Test_Create_NFT](img/TEST_CREATE_NFT.png)

- Informazioni Generali della Transazione;
- Azione della Transazione;
- Indirizzi Coinvolti
    - from: indirizzo Ethereum del mittente della transazione, configurato tramite MetaMask;
    - to: indirizzo dello smart contract DynamicNFT.
- Informazioni sul trasferimento dell'NFT;
- Costo della transazione.

### 4.2. Test Aggiornamento Metadati
![Test_Update_Metadata](img/TEST_CREATE_NFT.png)

- Ciò di significativo che cambia è la parte associata all'azione della transazione (updateMetadata).

## 5. Utilizzo ABI
Da Remix IDE è necessario prendere l'ABI associato al contratto per:
- definire l'interfaccia del contratto;
- consentire interazioni con il contratto tramite Web3.

## 6. Creazione del file private_data.env
File utilizzato per memorizzare dati sensibili:
- CONTRACT_ADDRESS -> indirizzo del contratto sulla blockchain Ethereum (recuperabile da Remix IDE);
- QUICKNODE_URL -> endpoint di QuickNode per connettersi alla blockchain (questo URL consente al progetto di connettersi alla blockchain Ethereum in modo affidabile e scalabile. QuickNode funge da ponte tra l'applicazione e la rete Ethereum);
- PRIVATE_KEY_METAMASK -> chiave privata per firmare transazioni (recuperabile dal proprio account Metamask);

N.B. Per quanto riguarda Quicknode, è possibile, una volta creato un account, recuperare l'URL da questa schermata:
![QUICKNODE](img/creazione_endpoint_con_quicknode.png)

## 7. Test e verifica con Etherscan
Per i test finali, è necessario utilizzare il seguente comando:

```
python main.py
```

Una volta fatto, è possibile verificare su Etherscan la creazione e l'aggiornamento dell'NFT:
- creazione
![TEST_FINALE_CREATE](img/TEST_FINALE_ETHERSCAN_CREATE_DYNAMIC_NFT.png)

- aggiornamento
![TEST_FINALE_CREATE](img/TEST_FINALE_ETHERSCAN_UPDATE_METADATA.png)

## 8. Frontend con Streamlit
Streamlit è stato scelto per la sua semplicità e immediatezza nella creazione di interfacce grafiche interattive, rendendo il progetto facilmente accessibile e utilizzabile anche da utenti non esperti in sviluppo software.
L'interfaccia consente agli utenti di:
- creare un NFT, rappresentato come un digital twin associato ad un avatar (immagine specifica) e i dettagli del token creato, come il suo ID e i metadati, vengono mostrati direttamente nella schermata;
- aggiornare i metadati associati all'NFT esistente.

N.B. Ogni azione è legata a un tasto specifico.

Per il test dell'interfaccia, è necessario utilizzare il seguente comando:

```
streamlit run app.py 
```

![FRONTEND](img/FRONTEND_STREAMLIT.png)

## Limitazioni
- Dipendenza da servizi esterni (come Quicknode o Mailjet API);
- Valore del gas price incrementato all'atto della creazione di un Dynamic NFT: le commissioni di gas possono rendere costoso aggiornare frequentemente i metadati o creare nuovi NFT, soprattutto in momenti di congestione della rete;
- Mancanza di una decentralizzazione dei dati: rischio di perdere i dati (metadati e images) associati agli NFT;
- Complessità della configurazione (chiavi private, endpoint QuickNode e wallet) per i non esperti;
- I test realizzati sono stati limitati da un numero fisso di SepoliaETH da poter utilizzare.

## Miglioramenti
- Implementare strategie per ridurre il gas price (ad esempio: utilizzo di layer-2);
- Migliorare la gestione dei permessi nel contratto Ethereum;
- Decentralizzazione dei dati: per garantire persistenza ed immutabilità sarebbe meglio memorizzare metadati e immagini degli avatar escusivamente su IPFS o simili;
- Estendere l'interfaccia streamlit;
- Introduzione degli Oracoli per l'automazione: poter aggiornare i metadati degli NFT dinamici in risposta ad eventi esterni.

N.B. Questo progetto vuole rappresentare solo un caso d'uso specifico, in cui il digital twin e il relativo aggiornamento sono fissati. Quindi ciò che potrebbe essere successivamente implementato è una dinamicità nella creazione/aggiornamento dei digital twin, dando tramite l'interfaccia la possibilità all'utente di scegliere il tokenID su cui lavorare.

## Autore
Progetto sviluppato da: Migliaccio Luca