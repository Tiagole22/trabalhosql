-- =========================================
-- SISTEMA DE RESERVAS - POSTGRESQL
-- =========================================

-- APAGAR TABELAS SE JÁ EXISTIREM
DROP TABLE IF EXISTS reservas CASCADE;
DROP TABLE IF EXISTS quartos CASCADE;
DROP TABLE IF EXISTS hospedes CASCADE;

-- =========================================
-- TABELA DE HÓSPEDES
-- =========================================
CREATE TABLE hospedes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)
);

-- =========================================
-- TABELA DE QUARTOS
-- =========================================
CREATE TABLE quartos (
    id SERIAL PRIMARY KEY,
    numero INT NOT NULL,
    tipo VARCHAR(50),
    preco DECIMAL(10,2),        -- valor da diária
    status VARCHAR(20) DEFAULT 'LIVRE'
);

-- =========================================
-- TABELA DE RESERVAS
-- =========================================
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    id_hospede INT REFERENCES hospedes(id),
    id_quarto INT REFERENCES quartos(id),
    entrada DATE,
    saida DATE,
    total DECIMAL(10,2)         -- calculado pela function
);

-- =========================================
-- FUNCTION: CALCULAR TOTAL DA RESERVA
-- =========================================
CREATE OR REPLACE FUNCTION calcular_total(
    p_quarto INT,
    p_entrada DATE,
    p_saida DATE
)
RETURNS DECIMAL(10,2)
AS $$
DECLARE
    preco_quarto DECIMAL(10,2);
    dias INT;
BEGIN
    -- Buscar preço do quarto
    SELECT preco
    INTO preco_quarto
    FROM quartos
    WHERE id = p_quarto;

    -- Calcular quantidade de dias
    dias := (p_saida - p_entrada);

    -- Retornar valor total
    RETURN preco_quarto * dias;
END;
$$ LANGUAGE plpgsql;

-- =========================================
-- TRIGGER: ATUALIZAR STATUS DO QUARTO
-- =========================================
CREATE OR REPLACE FUNCTION atualizar_status_quarto()
RETURNS TRIGGER
AS $$
BEGIN
    UPDATE quartos
    SET status = 'OCUPADO'
    WHERE id = NEW.id_quarto;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_atualizar_status_quarto
AFTER INSERT ON reservas
FOR EACH ROW
EXECUTE FUNCTION atualizar_status_quarto();

-- =========================================
-- PROCEDURE: REALIZAR RESERVA
-- =========================================
CREATE OR REPLACE PROCEDURE reservar(
    p_hospede INT,
    p_quarto INT,
    p_entrada DATE,
    p_saida DATE
)
AS $$
DECLARE
    v_total DECIMAL(10,2);
BEGIN
    -- Calcular total da reserva
    v_total := calcular_total(p_quarto, p_entrada, p_saida);

    -- Inserir reserva
    INSERT INTO reservas (
        id_hospede,
        id_quarto,
        entrada,
        saida,
        total
    )
    VALUES (
        p_hospede,
        p_quarto,
        p_entrada,
        p_saida,
        v_total
    );
END;
$$ LANGUAGE plpgsql;

-- =========================================
-- DADOS DE TESTE
-- =========================================
INSERT INTO hospedes (nome, telefone)
VALUES ('Maria', '8899-8888');

INSERT INTO quartos (numero, tipo, preco)
VALUES (101, 'Casal', 150.00);

-- =========================================
-- CHAMAR A PROCEDURE
-- =========================================
CALL reservar(1, 1, '2025-11-29', '2025-12-01');

-- =========================================
-- CONSULTAS (CRUD - READ)
-- =========================================
SELECT * FROM hospedes;
SELECT * FROM quartos;
SELECT * FROM reservas;
