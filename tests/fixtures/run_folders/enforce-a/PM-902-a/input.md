# Case 901: Leaking kitchen valve

Synthetic case for scorer tests.

## Case details

- Source role: Tenant
- Created: 2026-09-01 10:00:00 UTC
- Property: 1 Test Street, Testtown, AB1 2CD

## Initial request

The valve under the kitchen sink is dripping. Can someone take a look?

## History (events 1 to 6)

### 2026-09-01 10:05:00 UTC — event 1

- Channel: Update
- From: Agency
- To: Landlord

Repair request received for 1 Test Street, AB1 2CD.

### 2026-09-02 09:00:00 UTC — event 2

- Channel: Update
- From: Agency
- To: Agency

Landlord approval confirmed. Proceed to provider selection.

### 2026-09-03 11:00:00 UTC — event 3

- Channel: Email
- From: Test Plumbing
- To: Agency

Quote to replace the kitchen valve at 1 Test Street: £180.00 including VAT.

### 2026-09-04 08:30:00 UTC — event 4

- Channel: Update
- From: Agency
- To: Test Plumbing

Quote of £180.00 approved by the landlord. Please book with the tenant.

### 2026-09-10 16:00:00 UTC — event 5

- Channel: SMS
- From: Tenant
- To: Agency

The plumber came today and the leak has stopped. Thanks.

### 2026-09-12 12:00:00 UTC — event 6

- Channel: Email
- From: Test Plumbing
- To: Agency

Invoice for work at 1 Test Street, AB1 2CD: £240.00. Extra fittings were needed.
