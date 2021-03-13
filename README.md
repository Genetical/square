# square.py

An API wrapper for square.


## Installing
**Python 3.7 or higher is required.**

This package is not available on PyPi yet.
You can setup the development environment by doing the following:

```shell
    pip install poetry
    git clone https://github.com/Genetical/square
    cd square.py
    poetry install
    tox
```
If you wish to package the repository, do `poetry build` then you can use `pip install`.

## TODO List
- [ ] Payments
    - [ ] List Payments
    - [ ] Create payment
    - [ ] Cancel payment by idempotency key
    - [ ] Get payment
    - [ ] Cancel payment
    - [ ] Complete payment
    - [ ] V1 List payments
    - [ ] V1 Retrieve payment
    - [ ] Refunds
        - [ ] List payment refunds
        - [ ] Refund payment
        - [ ] Get payment refund
        - [ ] V1 List refunds
        - [ ] V1 Create refund
    - [ ] Disputes
        - [ ] List disputes
        - [ ] Retrieve dispute
        - [ ] Accept dispute
        - [ ] List dispute evidence
        - [ ] Remove dispute evidence
        - [ ] Retrieve dispute evidence
        - [ ] Create dispute evidence file
        - [ ] Create dispute evidence text
        - [ ] Submit evidence
    - [ ] Checkout
        - [ ] Create checkout
    - [ ] Apple Pay
        - [ ] Register domain
- [ ] Terminal
    - [ ] Create terminal checkout
    - [ ] Search terminal checkouts
    - [ ] Get terminal checkout
    - [ ] Cancel terminal checkout
    - [ ] Create terminal refund
    - [ ] Search terminal refunds
    - [ ] Get terminal refund
    - [ ] Cancel terminal refund
- [ ] Orders
    - [ ] Create order
    - [ ] Batch retrieve orders
    - [ ] Calculate order
    - [ ] Search orders
    - [ ] Retrieve order
    - [ ] Update order
    - [ ] Pay order
- [ ] Subscriptions
    - [ ] Create subscriptions
    - [ ] Search subscriptions
    - [ ] Retrieve subscription
    - [ ] Update subscription
    - [ ] Cancel subscription
    - [ ] List subscription events
- [ ] Invoices
    - [ ] List invoices
    - [ ] Create invoice
    - [ ] Search invoices
    - [ ] Delete invoice
    - [ ] Get invoice
    - [ ] Update invoice
    - [ ] Cancel invoice
    - [ ] Publish invoice
- [ ] Items
    - [ ] Catalog
        - [ ] Batch delete catalog objects
        - [ ] Batch retrieve catalog objects
        - [ ] Batch upsert catalog objects
        - [ ] Create catalog image
        - [ ] Catalog info
        - [ ] List catalog
        - [ ] Upsert catalog object
        - [ ] Delete catalog object
        - [ ] Retrieve catalog object
        - [ ] Search catalog objects
        - [ ] Search catalog items
        - [ ] Update item modifier lists
        - [ ] Update item taxes
    - [ ] Inventory
        - [ ] Retrieve inventory adjustment
        - [ ] Batch change inventory
        - [ ] Batch retrieve inventory changes
        - [ ] Batch retrieve inventory counts
        - [ ] Retrieve inventory physical count
        - [ ] Retrieve inventory count
        - [ ] Retrieve inventory changes
- [x] Customers
    - [x] List Customer
    - [x] Create Customer
    - [x] Search Customer
    - [x] Delete Customer
    - [x] Retrieve Customer
    - [x] Update Customer
    - [x] Create Customer Card
    - [x] Delete Customer Card
    - [x] Remove group from Customer
    - [x] Add Group to Customer
    - [x] Groups
        - [x] List Groups
        - [x] Create Group
        - [x] Delete Group
        - [x] Retrieve Group
        - [x] Update Group
    - [x] Segments
        - [x] List Customer Segments
        - [x] Retrieve Customer Segments
- [ ] Loyalty
    - [ ] Create loyalty account
    - [ ] Search loyalty accounts
    - [ ] Retrieve loyalty account
    - [ ] Accumulate loyalty points
    - [ ] Adjust loyalty points
    - [ ] Search loyalty events
    - [ ] List loyalty programs
    - [ ] Calculate loyalty points
    - [ ] Create loyalty reward
    - [ ] Search loyalty rewards
    - [ ] Delete loyalty reward
    - [ ] Retrieve loyalty reward
    - [ ] Redeem loyalty reward
- [ ] Bookings
    - [ ] Create booking
    - [ ] Search availability
    - [ ] Retrieve business booking profile
    - [ ] List team member booking profiles
    - [ ] Retrieve team member booking profile
    - [ ] Retrieve booking
    - [ ] Update booking
    - [ ] Cancel booking
- [ ] Business
    - [ ] Merchants
        - [ ] List merchants
        - [ ] Retrieve merchant
    - [ ] Locations
        - [ ] List locations
        - [ ] Create location
        - [ ] Retrieve location
        - [ ] Update location
    - [ ] Devices
        - [ ] List device codes
        - [ ] Create device code
        - [ ] Get device code
    - [ ] Cash drawers
        - [ ] List cash drawer shifts
        - [ ] Retrieve cash drawer shift
        - [ ] List cash drawer shift events
- [ ] Team
    - [ ] Team
        - [ ] Create team member
        - [ ] Bulk create team members
        - [ ] Bulk update team members
        - [ ] Search team members
        - [ ] Retrieve team member
        - [ ] Update team member
        - [ ] Retrieve wage setting
        - [ ] Update wage setting
    - [ ] Labor
        - [ ] List break types
        - [ ] Create break type
        - [ ] Delete break type
        - [ ] Get break type
        - [ ] Update break type
        - [ ] Create shift
        - [ ] Search shifts
        - [ ] Delete shift
        - [ ] Update shift
        - [ ] List team member wages
        - [ ] Get team member wage
        - [ ] List workweek configs
        - [ ] Update workweek config
- [ ] Financials
    - [ ] Bank Accounts
        - [ ] List bank accounts
        - [ ] Get bank account by V1 ID
        - [ ] Get bank account
    - [ ] Settlements
        - [ ] V1 List settlements
        - [ ] V1 Retrieve settlement
- [ ] Auth
    - [ ] OAuth
        - [ ] Authorize
        - [ ] Revoke token
        - [ ] Obtain token
    - [ ] Mobile Authorization
        - [ ] Create mobile authorization code
