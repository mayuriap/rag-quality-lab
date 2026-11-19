-- Seed data for Northbridge Bank (FICTIONAL).
-- Note: product SAV-EASY-01 has an EXPIRED rate row on purpose, to test effective dating.

INSERT INTO products VALUES
('CA-EVERYDAY', 'Everyday Current Account', 'current_account', 0, 'none', 'none', NULL, NULL, NULL, 0,
 '18 or over and UK resident. Sole or joint (max 2 holders).', 'No interest on credit balances.',
 '2026-09-01', NULL, '2026-09-01 09:00:00'),
('CA-PLUS', 'Everyday Plus Current Account', 'current_account', 0, 'none', 'none', NULL, NULL, NULL, 3,
 '18 or over and UK resident.', 'Includes worldwide travel insurance and mobile phone insurance. No non-sterling fee on card purchases.',
 '2026-09-01', NULL, '2026-09-01 09:00:00'),
('SAV-EASY-01', 'Easy Access Saver', 'savings', 2.85, 'AER', 'variable', NULL, 1, 250000, 0,
 'UK resident aged 16 or over.', 'Interest calculated daily, paid monthly. Unlimited penalty-free withdrawals.',
 '2026-06-01', '2026-09-30', '2026-09-30 17:00:00'),
('SAV-EASY-02', 'Easy Access Saver', 'savings', 3.10, 'AER', 'variable', NULL, 1, 250000, 0,
 'UK resident aged 16 or over.', 'Interest calculated daily, paid monthly. Unlimited penalty-free withdrawals.',
 '2026-10-01', NULL, '2026-10-01 08:00:00'),
('SAV-FIX-12M', 'Fixed Rate Bond - 1 Year', 'savings', 4.05, 'AER', 'fixed', 12, 1000, 500000, 0,
 'UK resident aged 18 or over.', 'Deposits only in the first 14 days. No withdrawals before the end of the term. Can close within 14 days without penalty.',
 '2026-10-01', NULL, '2026-10-01 08:00:00'),
('SAV-REG-12M', 'Regular Saver', 'savings', 5.50, 'AER', 'fixed', 12, 25, NULL, 0,
 'Must hold a Northbridge Everyday Current Account.', 'Pay in 25 to 300 GBP per calendar month. One penalty-free withdrawal; any further withdrawal closes the account.',
 '2026-10-01', NULL, '2026-10-01 08:00:00'),
('ISA-CASH', 'Cash ISA', 'isa', 3.35, 'AER', 'variable', NULL, 1, NULL, 0,
 'UK resident aged 18 or over.', 'Tax-free interest. Annual ISA allowance of 20,000 GBP per tax year across all ISAs.',
 '2026-10-01', NULL, '2026-10-01 08:00:00');

INSERT INTO fees VALUES
('FEE-001', 'CA-EVERYDAY', 'Non-sterling transaction fee (card purchases)', 2.75, 'percent', 'Applies to debit card purchases in a foreign currency.', '2026-09-01', NULL, '2026-09-01 09:00:00'),
('FEE-002', 'CA-EVERYDAY', 'Non-sterling transaction fee (cash withdrawals)', 2.75, 'percent', 'Applies to cash withdrawals abroad.', '2026-09-01', NULL, '2026-09-01 09:00:00'),
('FEE-003', 'CA-EVERYDAY', 'Foreign cash withdrawal fee', 1.50, 'GBP', 'Charged per cash withdrawal abroad, on top of the non-sterling transaction fee.', '2026-09-01', NULL, '2026-09-01 09:00:00'),
('FEE-004', 'CA-EVERYDAY', 'CHAPS payment', 20.00, 'GBP', 'Per payment. Must be requested in branch or by phone.', '2026-09-01', NULL, '2026-09-01 09:00:00'),
('FEE-005', 'CA-PLUS', 'Foreign cash withdrawal fee', 1.50, 'GBP', 'Charged per cash withdrawal abroad.', '2026-09-01', NULL, '2026-09-01 09:00:00'),
('FEE-006', 'CA-PLUS', 'CHAPS payment', 20.00, 'GBP', 'Per payment. Must be requested in branch or by phone.', '2026-09-01', NULL, '2026-09-01 09:00:00');