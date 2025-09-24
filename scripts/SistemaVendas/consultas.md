# Consultas, como e o que elas estão fazendo

## Conculta 01

```sql
SELECT * FROM cliente
JOIN pedido ON cliente.cliente_id = pedido.cliente_id
WHERE cliente.cliente_id = 1;
```

- Mostra todos os dados de um cliente específico e também mostra as informações dos pedidos desse cliente

## Consulta 02

```sql
SELECT * FROM pedido
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
WHERE pedido.pedido_id = 1;
```

- Mostra todas as informações e a forma de pagamento do primeiro pedido registrado

## Consulta 03

```sql
SELECT * FROM pedido
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
WHERE forma_pagamento.tipo = 'Cartão de Crédito';
```

- Mostra todos os pedidos feitos com "Cartão de Crédito"

## Consulta 04

```sql
SELECT forma_pagamento.tipo, count(pedido.pedido_id) as total_pedidos FROM pedido
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
GROUP BY forma_pagamento.tipo;
```

- Mostra cada forma de pagamento e a quantidade de pedidos feitos com ela

## Consulta 05

```sql
SELECT * FROM pedido
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
JOIN item ON item_pedido.item_id = item.item_id
WHERE pedido.pedido_id = 1;
```

- Mostra todos os dados do pedido além do(s) item(s) daquele pedido

## Consulta 06

```sql
SELECT sum(item.preco) as total FROM pedido
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
JOIN item ON item_pedido.item_id = item.item_id
WHERE pedido.pedido_id = 1;
```

- Mostra a soma dos preços dos produtos do pedido de ID 1, sem considerar a quantidade comprada de cada item

## Consulta 07

```sql
SELECT * FROM item
JOIN item_pedido ON item_pedido.item_pedido_id = item.item_id
JOIN vendedor ON item_pedido.item_id = item.item_id
WHERE item_pedido.pedido_id = 1;
```

- Mostra todos os dados dos itens de um pedido específico e também mostra as informações do vendedor

## Consulta 08

!!CONSULTA ERRADA!!

```sql
SELECT * FROM pedido
JOIN vendedor ON pedido.vendedor_id = vendedor.vendedor_id
WHERE vendedor.vendedor_id = 1;
```

- Mostra todos os pedidos feitos por um vendedor especifico

## Consulta 09

```sql
SELECT vendedor.nome, count(pedido.pedido_id) as total_pedidos FROM pedido
JOIN vendedor ON vendedor.vendedor_id = vendedor.vendedor_id
GROUP BY vendedor.nome
```

- Mostra quantos pedidos foram feitos por cada vendedor

## Consulta 10

```sql
SELECT * FROM cliente
JOIN endereco ON cliente.cliente_id = endereco.cliente_id
WHERE cliente.cliente_id = 1;
```

- Mostra as informações de um cliente especifico bem como suas informações de endereço

## Consulta 11

```sql
SELECT sum(item.preco) as total FROM cliente
JOIN pedido ON cliente.cliente_id = pedido.cliente_id
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
JOIN item ON item_pedido.item_id = item.item_id
WHERE cliente.cliente_id = 1;
```

- Mostra o valor total gasto em todos os pedidos feitos por um cliente específico

## Consulta 12

```sql
SELECT forma_pagamento.tipo, sum(item.preco) as total FROM cliente
JOIN pedido ON cliente.cliente_id = pedido.cliente_id
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
JOIN item ON item_pedido.item_id = item.item_id
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
WHERE cliente.cliente_id = 1
GROUP BY forma_pagamento.tipo;
```

- Mostra quanto um cliente específico gastou em cada forma de pagamento, agrupando por tipo de pagamento
<!-- tirando o WHERE mostra o total de todas as formas de pagamento de todos os clientes juntos -->

## Consulta 13

```sql
SELECT forma_pagamento.tipo, sum(item.preco) as total FROM cliente
JOIN pedido ON cliente.cliente_id = pedido.cliente_id
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
JOIN item ON item_pedido.item_id = item.item_id
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
WHERE cliente.cliente_id = 1
GROUP BY forma_pagamento.tipo
HAVING count(pedido.pedido_id) > 1;
```

- Mostra quanto um cliente específico gastou em cada forma de pagamento, mas apenas nas formas em que ele fez mais de um pedido

## Consulta 14

```sql
SELECT forma_pagamento.tipo, sum(item.preco) as total FROM cliente
JOIN pedido ON cliente.cliente_id = pedido.cliente_id
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
JOIN item ON item_pedido.item_id = item.item_id
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
WHERE cliente.cliente_id = 1
GROUP BY forma_pagamento.tipo
HAVING count(pedido.pedido_id) > 1
ORDER BY total DESC;
```

- Mostra quanto um cliente específico gastou em cada forma de pagamento, mas apenas nas formas em que ele fez mais de um pedido, ordenando do maior para o menor valor

## Consulta 15

```sql
SELECT * FROM cliente ORDER BY nome;
```

```sql
SELECT * FROM cliente ORDER BY nome ASC;
```

- Mostra todos os clientes em ordem alfabética

## Consulta 16

```sql
SELECT cliente.nome, count(pedido.pedido_id) as total_pedidos FROM cliente
JOIN pedido ON cliente.cliente_id = pedido.cliente_id
GROUP BY cliente.nome
ORDER BY total_pedidos DESC;
```

- Mostra o nome de cada cliente e quantos pedidos ele fez, ordenando do que mais pediu para o que menos pediu

## Consulta 17

```sql
SELECT DISTINCT tipo FROM forma_pagamento;
```

- Mostra todas as formas de pagamento diferentes que existem no sistema

## Consulta 18

```sql
SELECT DISTINCT nome FROM vendedor;
```

- Mostra todos os nomes diferentes de vendedores cadastrados

## Consulta 19

```sql
SELECT DISTINCT nome FROM client;
```

- Mostra todos os nomes de clientes distintos

## Consulta 20

```sql
SELECT * FROM pedido WHERE pedido_id BETWEEN 1 AND 10;
```

- Mostra os dados dos pedidos de 1 a 10

## Consulta 21

```sql
SELECT pedido.pedido_id, count(item_pedido.item_pedido_id) as total_itens FROM pedido
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
WHERE pedido.pedido_id BETWEEN 1 AND 10
GROUP BY pedido.pedido_id
ORDER BY total_itens;
```

- Mostra a quantidade de itens em cada pedido de 1 a 10, em ordem crescente de quantidade

## Consulta 22

```sql
SELECT * FROM pedido WHERE cliente_id IN (SELECT cliente_id FROM cliente WHERE nome = 'João');
```

- Mostra os dados dos pedidos feitos por clientes que se chamam João

## Consulta 23

```sql
SELECT * FROM pedido
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
WHERE pedido.cliente_id IN (SELECT cliente_id FROM cliente WHERE nome = 'João');
```

- Mostra os dados dos pedidos feitos por João, incluindo a forma de pagamento usada em cada um

## Consulta 24

```sql
SELECT forma_pagamento.tipo, sum(item.preco) as total FROM cliente
JOIN pedido ON cliente.cliente_id = pedido.cliente_id
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
JOIN item ON item_pedido.item_id = item.item_id
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
WHERE cliente.cliente_id = 1
AND forma_pagamento.forma_pagamento_id IN (SELECT forma_pagamento.forma_pagamento_id FROM pedido
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
GROUP BY forma_pagamento.forma_pagamento_id
HAVING count(pedido.pedido_id) > 1)
GROUP BY forma_pagamento.tipo;
```

- Mostra quanto um cliente específico gastou em cada forma de pagamento, mas apenas nas formas em que houve mais de um pedido

## Consulta 25

```sql
SELECT forma_pagamento.tipo, sum(item.preco) as total FROM cliente
JOIN pedido ON cliente.cliente_id = pedido.cliente_id
JOIN item_pedido ON pedido.pedido_id = item_pedido.pedido_id
JOIN item ON item_pedido.item_id = item.item_id
JOIN forma_pagamento ON pedido.forma_pagamento_id = forma_pagamento.forma_pagamento_id
WHERE cliente.cliente_id = 1
AND forma_pagamento.forma_pagamento_id IN (1, 2)
GROUP BY forma_pagamento.tipo;
```

- Mostra o valor total gasto por um cliente específico, mas apenas nos pedidos pagos com as formas de pagamento 1 ou 2, agrupando por forma de pagamento
