-- Quem está vendendo?
-- Loja
-- -> Id do comércio (Primary Key)
-- -> Chave da API 
-- -> Nome do comércio
-- -> Email do comércio

CREATE TABLE "Comercio" (
	id int NOT NULL,
	apikey_crypt varchar(255) NOT NULL,
	nome_comercio varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	PRIMARY KEY(id)
);

-- O que está vendendo?
-- Item
-- -> Id do item (Primary Key)
-- -> Id do comércio que está vendendo (Foreign Key)
-- -> Nome do item
-- -> Preço do item
-- -> Moeda que foi feita a compra

CREATE TABLE "Produto" (
	id int NOT NULL,
	id_comercio int NOT NULL,
	nome_item varchar(255) NOT NULL,
	preco real NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(id_comercio) REFERENCES Comercio(id)
);

-- Para quem está vendendo?
-- -> Id do usuário (Primary Key)
-- -> Nome do usuário 
-- -> Email do usuário 

CREATE TABLE Usuario (
	id int NOT NULL,
	nome_usuario varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	senha_crypt varchar(25) NOT NULL,
	PRIMARY KEY(id)
);

-- Como está vendendo?
-- -> Id da compra (Primary Key)
-- -> Id do comércio que vendeu (Foreign Key)
-- -> Id do item vendido (Foreign Key)
-- -> Id da pessoa que comprou (Foreign Key)
-- -> Horário da compra
-- -> Status da compra

CREATE TABLE Venda (
	id int NOT NULL,
	id_comercio int NOT NULL,
	id_item int NOT NULL,
	id_cliente int,
	hora_compra datetime,
	status varchar(10) NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(id_comercio) REFERENCES Comercio(id),
	FOREIGN KEY(id_item) REFERENCES Produto(id),
	FOREIGN KEY(id_cliente) REFERENCES Usuario(id)
);