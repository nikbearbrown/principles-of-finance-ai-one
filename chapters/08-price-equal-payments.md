# A Payment Schedule Has a First Date

A salesperson quotes “three payments of $100.” Before calculating the price today, ask whether the first one is due now or in a year. Three installments is a count, not a schedule.

## Two finite schedules, one rate

At the illustrative effective annual rate of 5%, a series paying $100 at the ends of years one, two and three is worth:

`100/1.05 + 100/1.05² + 100/1.05³ ≈ $272.32`.

This is an **ordinary annuity**. Move each payment one period earlier and the dates are now 0, 1 and 2. That **annuity due** is worth about $285.94 today. Since all three receipts are shifted by one year, the ordinary-annuity value multiplied by 1.05 gives the annuity due. This is a timing identity at the same rate, not an increase in the amount paid.

For (n) end-of-period payments (C) and nonzero rate (r), the ordinary-annuity factor is `[1 − (1+r)^(-n)]/r`. You can build it by summing the individual discount factors and subtracting a copy of the sum shifted by one term. At zero interest the payments do not need discounting; value is (nC). An unending series with first payment a period from now and constant positive discount rate has value (C/r) under the assumption it can continue. Here that would be $2,000, not an appropriate value for three payments.

## Take a loan payment apart

Suppose a separate two-year loan advances $600 today at 10% annually and is repaid by two equal end-of-year payments. The PV of the payments must equal the amount advanced at the quoted rate, absent other costs or benefits. Divide $600 by the two-year annuity factor. Payment is about $345.71. The first year's interest is $60. About $285.71 goes to principal, so about $314.29 remains. The second year's interest is about $31.43, leaving that year's rounded payment to close the principal. Keep unrounded balances until the end; a rounded cents payment may require a last adjustment.

This is a payment decomposition, not a rule that all borrowing costs go down over time. An interest-only loan, an adjustable rate or a fee changes the schedule. Verify the last row: the closing balance should be zero under the terms specified here.

**Teardown.** A response assigns half of each payment to principal because there are two equal payments. Check both the first-year interest and the final balance. Equal payments do not imply equal reductions in principal.

**Transfer.** At 5%, compute the PV of the same three $100 payments when the first is at year two. Compare it with the ordinary-annuity value and explain which factor accounts for the difference.

[Contents](../README.md)
