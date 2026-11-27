-- Quem está vendendo?
-- Loja
-- -> Id do comércio (Primary Key)
-- -> Chave da API 
-- -> Nome do comércio
-- -> Email do comércio

CREATE TABLE "Comercio" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    apikey_crypt varchar(255) NOT NULL,
    nome_comercio varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);


-- O que está vendendo?
-- Item
-- -> Id do item (Primary Key)
-- -> Id do comércio que está vendendo (Foreign Key)
-- -> Nome do item
-- -> Preço do item
-- -> Moeda que foi feita a compra

CREATE TABLE "Produto" (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_comercio int NOT NULL,
	nome_item varchar(255) NOT NULL,
	preco real NOT NULL,
	FOREIGN KEY(id_comercio) REFERENCES Comercio(id)
);

-- Para quem está vendendo?
-- -> Id do usuário (Primary Key)
-- -> Nome do usuário 
-- -> Email do usuário 

CREATE TABLE Usuario (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nome_usuario varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	senha_crypt varchar(255) NOT NULL
);

-- Como está vendendo?
-- -> Id da compra (Primary Key)
-- -> Id do comércio que vendeu (Foreign Key)
-- -> Id do item vendido (Foreign Key)
-- -> Id da pessoa que comprou (Foreign Key)
-- -> Horário da compra
-- -> Status da compra

CREATE TABLE Venda (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_comercio int NOT NULL,
	id_item int NOT NULL,
	id_cliente int,
	hora_compra datetime,
	status varchar(10) NOT NULL,
	FOREIGN KEY(id_comercio) REFERENCES Comercio(id),
	FOREIGN KEY(id_item) REFERENCES Produto(id),
	FOREIGN KEY(id_cliente) REFERENCES Usuario(id)
);

-- Solicitações de exclusão de comércio

CREATE TABLE SolicitacaoExclusao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_comercio INTEGER NOT NULL,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    data_expiracao DATETIME NOT NULL,
    utilizado INTEGER NOT NULL DEFAULT 0
        CHECK (utilizado IN (0, 1)),
    FOREIGN KEY (id_comercio) REFERENCES Comercio(id)
);
