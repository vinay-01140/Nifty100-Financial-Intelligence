-- =========================================================
-- Sprint 1 - Day 7
-- exploratory_queries.sql
-- Nifty100 Financial Intelligence
-- =========================================================

-- ---------------------------------------------------------
-- Q1. Total companies loaded
-- ---------------------------------------------------------
SELECT COUNT(*) AS total_companies
FROM companies;


-- ---------------------------------------------------------
-- Q2. Row counts for all major tables
-- ---------------------------------------------------------
SELECT 'companies' AS table_name, COUNT(*) AS row_count FROM companies
UNION ALL
SELECT 'profitandloss', COUNT(*) FROM profitandloss
UNION ALL
SELECT 'balancesheet', COUNT(*) FROM balancesheet
UNION ALL
SELECT 'cashflow', COUNT(*) FROM cashflow
UNION ALL
SELECT 'analysis', COUNT(*) FROM analysis
UNION ALL
SELECT 'documents', COUNT(*) FROM documents
UNION ALL
SELECT 'prosandcons', COUNT(*) FROM prosandcons
UNION ALL
SELECT 'stock_prices', COUNT(*) FROM stock_prices
UNION ALL
SELECT 'financial_ratios', COUNT(*) FROM financial_ratios
UNION ALL
SELECT 'market_cap', COUNT(*) FROM market_cap
UNION ALL
SELECT 'sectors', COUNT(*) FROM sectors
UNION ALL
SELECT 'peer_groups', COUNT(*) FROM peer_groups;


-- ---------------------------------------------------------
-- Q3. Companies with most P&L years
-- ---------------------------------------------------------
SELECT 
    c.id,
    c.company_name,
    COUNT(p.year) AS pnl_years
FROM companies c
LEFT JOIN profitandloss p
    ON c.id = p.company_id
GROUP BY c.id, c.company_name
ORDER BY pnl_years DESC, c.id
LIMIT 15;


-- ---------------------------------------------------------
-- Q4. Companies with less than 5 years in any major table
-- ---------------------------------------------------------
SELECT 
    c.id,
    c.company_name,
    COALESCE(p.pnl_years, 0) AS pnl_years,
    COALESCE(b.bs_years, 0) AS bs_years,
    COALESCE(cf.cf_years, 0) AS cf_years
FROM companies c
LEFT JOIN (
    SELECT company_id, COUNT(*) AS pnl_years
    FROM profitandloss
    GROUP BY company_id
) p ON c.id = p.company_id
LEFT JOIN (
    SELECT company_id, COUNT(*) AS bs_years
    FROM balancesheet
    GROUP BY company_id
) b ON c.id = b.company_id
LEFT JOIN (
    SELECT company_id, COUNT(*) AS cf_years
    FROM cashflow
    GROUP BY company_id
) cf ON c.id = cf.company_id
WHERE COALESCE(p.pnl_years, 0) < 5
   OR COALESCE(b.bs_years, 0) < 5
   OR COALESCE(cf.cf_years, 0) < 5
ORDER BY c.id;


-- ---------------------------------------------------------
-- Q5. Top 10 companies by latest market cap
-- ---------------------------------------------------------
SELECT 
    m.company_id,
    c.company_name,
    m.year,
    m.market_cap_crore
FROM market_cap m
JOIN companies c
    ON m.company_id = c.id
WHERE (m.company_id, m.year) IN (
    SELECT company_id, MAX(year)
    FROM market_cap
    GROUP BY company_id
)
ORDER BY m.market_cap_crore DESC
LIMIT 10;


-- ---------------------------------------------------------
-- Q6. Top 10 companies by latest ROE from financial_ratios
-- ---------------------------------------------------------
SELECT
    f.company_id,
    c.company_name,
    f.year,
    f.return_on_equity_pct
FROM financial_ratios f
JOIN companies c
    ON f.company_id = c.id
WHERE (f.company_id, f.year) IN (
    SELECT company_id, MAX(year)
    FROM financial_ratios
    GROUP BY company_id
)
ORDER BY f.return_on_equity_pct DESC
LIMIT 10;


-- ---------------------------------------------------------
-- Q7. Average OPM by company from profitandloss
-- ---------------------------------------------------------
SELECT
    p.company_id,
    c.company_name,
    ROUND(AVG(p.opm_percentage), 2) AS avg_opm_pct
FROM profitandloss p
JOIN companies c
    ON p.company_id = c.id
GROUP BY p.company_id, c.company_name
ORDER BY avg_opm_pct DESC
LIMIT 15;


-- ---------------------------------------------------------
-- Q8. Sector-wise company counts
-- ---------------------------------------------------------
SELECT
    broad_sector,
    COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC, broad_sector;


-- ---------------------------------------------------------
-- Q9. Companies with highest latest debt-to-equity
-- ---------------------------------------------------------
SELECT
    f.company_id,
    c.company_name,
    f.year,
    f.debt_to_equity
FROM financial_ratios f
JOIN companies c
    ON f.company_id = c.id
WHERE (f.company_id, f.year) IN (
    SELECT company_id, MAX(year)
    FROM financial_ratios
    GROUP BY company_id
)
ORDER BY f.debt_to_equity DESC
LIMIT 10;


-- ---------------------------------------------------------
-- Q10. Document coverage by company
-- ---------------------------------------------------------
SELECT
    d.company_id,
    c.company_name,
    COUNT(*) AS document_count
FROM documents d
JOIN companies c
    ON d.company_id = c.id
GROUP BY d.company_id, c.company_name
ORDER BY document_count DESC, d.company_id
LIMIT 20;