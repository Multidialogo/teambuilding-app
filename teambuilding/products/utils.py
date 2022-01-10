def make_receipt(orders):
    receipt = 'Product, Amount, Price, Customer'

    for order in orders:
        receipt = receipt + "\n%s, %s, %s, %s" % (
            str(order.purchaseOption.product), order.purchaseOption.amount, str(order.purchaseOption.price_cents),
            str(order.customer))

    return receipt
