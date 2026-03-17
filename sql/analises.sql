-- 1: Ticket médio por estado

SELECT 
    c.customer_state AS estado,
    COUNT(DISTINCT o.order_id) AS total_pedidos,
    ROUND(AVG(oi.price)::NUMERIC, 2) AS ticket_medio,
    ROUND(SUM(oi.price)::NUMERIC, 2) AS receita_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY ticket_medio DESC;

-- 2. Top 10 categorias por receita (CTE)

WITH receita_categorias AS (
    SELECT 
        ct.product_category_name_english AS categoria,
        COUNT(DISTINCT o.order_id) AS total_pedidos,
        ROUND(SUM(oi.price)::NUMERIC, 2) AS receita_total,
        ROUND(AVG(oi.price)::NUMERIC, 2) AS preco_medio
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN products p ON oi.product_id = p.product_id
    JOIN category_translation ct ON p.product_category_name = ct.product_category_name
    WHERE o.order_status = 'delivered'
    GROUP BY ct.product_category_name_english
)
SELECT *,
    ROUND(100.0 * receita_total / SUM(receita_total) OVER(), 2) AS pct_receita
FROM receita_categorias
ORDER BY receita_total DESC
LIMIT 10;

-- 3. Tempo médio de entrega por categoria (window function)

WITH entrega_categoria AS (
    SELECT
        ct.product_category_name_english AS categoria,
        ROUND(AVG(
            EXTRACT(DAY FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))
        )::NUMERIC, 1) AS dias_entrega_medio,
        ROUND(AVG(oi.price)::NUMERIC, 2) AS preco_medio,
        COUNT(DISTINCT o.order_id) AS total_pedidos
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    JOIN category_translation ct ON p.product_category_name = ct.product_category_name
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY ct.product_category_name_english
)
SELECT *,
    RANK() OVER (ORDER BY dias_entrega_medio ASC) AS ranking_entrega,
    ROUND(AVG(dias_entrega_medio) OVER(), 1) AS media_geral_dias
FROM entrega_categoria
ORDER BY dias_entrega_medio ASC
LIMIT 15;

-- 4. Taxa de recompra de clientes

WITH pedidos_por_cliente AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_pedidos
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    total_pedidos AS qtd_pedidos,
    COUNT(*) AS total_clientes,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS pct_clientes
FROM pedidos_por_cliente
GROUP BY total_pedidos
ORDER BY total_pedidos;