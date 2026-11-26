
BEGIN TRANSACTION;

-- Adiciona o controle de status do comércio
ALTER TABLE Comercio
ADD COLUMN ativo INTEGER NOT NULL DEFAULT 1
CHECK (ativo IN (0, 1));

-- Cria a tabela de solicitações de exclusão
CREATE TABLE SolicitacaoExclusao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_comercio INTEGER NOT NULL,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    data_expiracao DATETIME NOT NULL,
    utilizado INTEGER NOT NULL DEFAULT 0
        CHECK (utilizado IN (0, 1)),
    FOREIGN KEY (id_comercio) REFERENCES Comercio(id)
);

COMMIT;
