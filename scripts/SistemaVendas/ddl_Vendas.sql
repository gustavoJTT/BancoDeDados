CREATE TABLE cliente (
    cliente_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(15),
    email VARCHAR(100)
);

CREATE TABLE endereco (
    endereco_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente(cliente_id),
    rua VARCHAR(255) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    cep VARCHAR(10) NOT NULL
);

CREATE TABLE forma_pagamento (
    forma_pagamento_id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE vendedor (
    vendedor_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(255),
    telefone VARCHAR(15)
);

CREATE TABLE item (
    item_id SERIAL PRIMARY KEY,
    vendedor_id INT REFERENCES vendedor(vendedor_id),
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50),
    quantidade_estoque INT NOT NULL
);

CREATE TABLE pedido (
    pedido_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente(cliente_id),
    endereco_id INT REFERENCES endereco(endereco_id),
    forma_pagamento_id INT REFERENCES forma_pagamento(forma_pagamento_id),
    data DATE NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE item_pedido (
    item_pedido_id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedido(pedido_id),
    item_id INT REFERENCES item(item_id),
    quantidade INT NOT NULL
);
