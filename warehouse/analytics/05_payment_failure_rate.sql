-- Payment failure rate by payment method

SELECT
    payment_method,
    COUNT(*) AS total_payment_attempts,
    COUNT(*) FILTER (WHERE payment_status = 'success') AS successful_payments,
    COUNT(*) FILTER (WHERE payment_status = 'failed') AS failed_payments,
    COUNT(*) FILTER (WHERE payment_status = 'refunded') AS refunded_payments,
    ROUND(
        COUNT(*) FILTER (WHERE payment_status = 'failed')::NUMERIC
        / NULLIF(COUNT(*), 0),
        4
    ) AS payment_failure_rate
FROM warehouse.fact_payments
GROUP BY payment_method
ORDER BY payment_failure_rate DESC;