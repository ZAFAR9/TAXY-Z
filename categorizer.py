"""
TAXY-Z — Transaction Categorizer
==================================
Core categorization engine. Classifies each bank transaction
into Essential, Non-Essential, Income, Transfer, or Business buckets.

Usage:
    from categorizer import categorize
    category = categorize("DoorDash purchase", -45.00)
"""

def categorize(desc: str, amt: float) -> str:
    """
    Categorize a single transaction.

    Args:
        desc: Raw transaction description from bank statement
        amt:  Transaction amount (negative = expense, positive = income)

    Returns:
        Category string (e.g. 'Essential – Groceries', 'NON-ESSENTIAL – Food Delivery (DoorDash)')
    """
    d = desc.upper()

    # ── INCOME ──────────────────────────────────────────────────────────────
    if amt > 0:
        if 'MERCHANT BNKCD DEPOSIT' in d:           return 'Income – Business (POS)'
        if 'EPX ST' in d and 'MERCH SETL' in d:    return 'Income – Business (POS)'
        if 'BANKCARD 8710' in d and any(x in d for x in ['DEP','BTOT','MTOT DEP']): return 'Income – Business (POS)'
        if 'FARMERS INSURAN PAYMENT' in d:          return 'Income – Insurance Payment'
        if 'ATM CASH DEPOSIT' in d:                 return 'Income – ATM Cash Deposit'
        if 'AUTOSAVE' in d:                         return 'Income – Autosave Transfer'
        if 'INTEREST' in d:                         return 'Income – Interest'
        if 'REVERSAL' in d:                         return 'Income – Refunds/Returns'
        if 'RETURN' in d and 'CARD PURCHASE' in d:  return 'Income – Refunds/Returns'
        if 'ZELLE' in d and 'FROM' in d:            return 'Income – Zelle Received'
        if 'ONLINE TRANSFER FROM' in d or 'ODP TRANSFER FROM' in d: return 'Income – Internal Transfer'
        if 'DEPOSIT' in d:                          return 'Income – Cash/Check Deposit'
        return 'Income – Other'

    # ── ESSENTIAL EXPENSES ──────────────────────────────────────────────────
    if 'BANK OF AMERICA MORTGAGE' in d:             return 'Essential – Mortgage'
    if 'PATELCO' in d:                              return 'Essential – Loan Payment'
    if 'BEST PROPERTY MA' in d or 'APPFOLIO' in d: return 'Essential – Rent Paid'
    if 'PG&E' in d or 'EBM*UD' in d or 'EBMUD' in d: return 'Essential – Utilities'
    if 'COMCAST' in d or 'ATT*BILL' in d or 'AT&T' in d or \
       'METRO BY T-MOBILE' in d or 'T-MOBILE' in d: return 'Essential – Utilities (Phone/Internet)'
    if 'DISCOVERY BAY' in d and 'DISPOSAL' in d:    return 'Essential – Utilities'
    if 'TOWN OF DISCOVERY BAY' in d:                return 'Essential – Utilities'
    if 'COAL-' in d:                                return 'Essential – Utilities'
    if 'GEICO' in d:                                return 'Essential – Insurance (Auto)'
    if 'PAC-LIFE-INS' in d or 'PACIFIC LIFE' in d: return 'Essential – Insurance (Life)'
    if 'TRANSAMERICA' in d:                         return 'Essential – Insurance (Life)'
    if 'HOMEOWNERS INSURANCE' in d or 'AMERICAN HM SHLD' in d or \
       'AHS.COM' in d or 'FRONTDOORHOME' in d:     return 'Essential – Insurance (Home)'
    if 'CHOICE HOME WARRANTY' in d:                 return 'Essential – Insurance (Home)'
    if 'METLIFE PET' in d:                          return 'Essential – Insurance (Pet)'
    if 'RLI INSURANCE' in d or 'WFGINSURANCE' in d: return 'Essential – Insurance (Other)'
    if 'ADT SECURITY' in d:                         return 'Essential – Home Security'
    if 'KAISER' in d:                               return 'Essential – Health (Kaiser)'
    if 'WALGREENS' in d or 'CVS' in d:             return 'Essential – Pharmacy'
    if 'RAYMOND CHAN DDS' in d or 'LONE TREE DR' in d: return 'Essential – Health (Dental)'
    if 'CENTRAL BOULEVARD VET' in d or 'DISCOVERY BAY VET' in d or \
       'EAST BAY VETERINARY' in d or 'ASPCA' in d: return 'Essential – Health (Vet)'
    if any(x in d for x in ['SAFEWAY','TRADER JOE','RALEYS','WHOLE FOODS',
       'LAKESHORE NATURAL','WINDMILL FARMS','APNA BAZAR','NEW INDIA BAZAR',
       'INDIA CASH & CARRY','OAKLAND HALAL MEAT','LUCKY #','KROGER',
       'SS MART','INSTACART','INSTACAR','IC* SAFEWAY']):
        if 'VIA INSTACAR' in d or 'INSTACART' in d or 'INSTACAR' in d: return 'Essential – Groceries'
        if 'FUEL' not in d: return 'Essential – Groceries'
    if 'DOLLAR TR' in d or 'DOLLAR TREE' in d or 'TARGET' in d: return 'Essential – Groceries'
    if 'AMERICAN EXPRESS ACH' in d or 'PAYMENT TO CHASE CARD' in d or \
       'SYNCB PAYMENT' in d:                        return 'Essential – Credit Card Payment'
    if 'ENLIGHTIUM' in d or 'YOUNGWONKS' in d or 'LAUREL SPRINGS' in d or \
       'NORRISEDUCA' in d:                          return 'Essential – Education (School)'
    if 'FD *CA DMV' in d or 'CA DMV' in d or 'STATE OF CALIF DMV' in d: return 'Essential – Auto (DMV)'
    if 'FRANCHISE TAX BO' in d:                     return 'Essential – Taxes'
    if 'ECOGUARD PEST' in d or 'STANLEY STEEMER' in d: return 'Essential – Home Maintenance'
    if 'BAYVALLEY MECHANICA' in d:                  return 'Essential – Auto Repair'
    if 'LOGICALEASE' in d:                          return 'Essential – Equipment Lease'
    if 'BORNSTEIN' in d or 'LAW OFFICES' in d:     return 'Essential – Legal'
    if any(x in d for x in ['LAKESHORE 76','CHEVRON','ARCO','SHELL','7-ELEVEN',
       'SAFEWAY FUEL','DIAMOND GAS','QUIK STOP','A&P SERVICE STA',
       'COUNTRY JUNCTION','SINCLAIR','FUEL 24','GRAND FUEL','COSTCO GAS']): return 'Essential – Auto (Gas)'

    # ── BUSINESS COSTS ──────────────────────────────────────────────────────
    if any(x in d for x in ['MERCHANT BNKCD DISCOUNT','MERCHANT BNKCD FEE',
       'FDMS ANNUAL FEE','EPX FE']) or \
       ('BANKCARD 8710' in d and any(x in d for x in ['DISCOUNT','DISC','ADJ'])) or \
       'GRAVITY PAYMENTS' in d or 'GRAV EXCEPTIONS' in d: return 'Business – Merchant Fees'
    if 'FDGL LEASE' in d or ('FDMS' in d and 'PYMT' in d): return 'Business – Equipment Lease'

    # ── SAVINGS / TRANSFERS ──────────────────────────────────────────────────
    if 'AUTOSAVE SAVINGS' in d:                     return 'Savings Transfer'
    if 'ONLINE TRANSFER TO' in d or 'ODP TRANSFER TO' in d: return 'Internal Transfer'
    if 'CHECK #' in d or (d.startswith('CHECK') and '#' in d): return 'Check Written'
    if 'ONLINE DOMESTIC WIRE' in d and 'FEE' not in d: return 'Transfer – Domestic Wire Out'

    # ── NON-ESSENTIAL ────────────────────────────────────────────────────────
    # Food delivery
    if any(x in d for x in ['DOORDASH','DOORDASHINC','DD DOORDASH','DD *DOORDASH',
       'DOORDASHDOUBLEDAS']):                        return 'NON-ESSENTIAL – Food Delivery (DoorDash)'

    # Restaurants
    RESTAURANTS = [
        'RESTAURANT','MESSOB','EUROMIX','BIRYANI','ENSSARO','CANTINA','HULA WOK',
        'THAI TASTE','PEKING GARDEN','KUPPANNA','MOUNTAIN MIKES','IN N OUT',
        'MCDONALD','BLUEWATER GRILL','COFFEE','STARBUCKS','MONKEY KING','CONNIES',
        'TST*','VINO VOLO','BISTRO','DADS BBQ','JACK IN THE BOX','MATSUYAMA',
        'PIZZA','TAQUERIA','CAFE ROMANAT','GYROS CUISINE','FENTONS CREAMERY',
        'HUNAN','RAMEN 101','SLOW HAND BBQ','FLIPSIDE BURGER','POPEYES','STARBIRD',
        'BURGER KING','CARLS JR','ADDIS ETHIOPIAN','GOJO ETHIOPIAN','MESKIE',
        'SAMURAI JAPANESE','PERSIAN NIGHTS','CHAPALA MEXICAN','CHICK-FIL-A',
        'SPICE BLEND','TIMELESS COFFEE','K BANCHAN','INDIA CLAY OVEN',
        'DESTA ETHIOPIAN','BRU WESTERVILLE','IBEXETHI','MINIETHI','VEGANMOB',
        'CALIFORNIA FINE WINES','MR. LIQUOR','FOUR LEGS BREWING',
    ]
    if any(x in d for x in RESTAURANTS):            return 'NON-ESSENTIAL – Restaurants & Dining Out'

    # Subscriptions
    if 'AMAZON PRIME' in d or 'AMZN RENTAL' in d:  return 'NON-ESSENTIAL – Subscriptions (Amazon Prime)'
    if 'PRIME VIDEO' in d or 'FUNIMATION' in d or 'CRUNCHYROLL' in d: return 'NON-ESSENTIAL – Subscriptions (Streaming)'
    if any(x in d for x in ['PLAYSTATION','STEAM GAMES','ROBLOX','ARENABREAKOUT']): return 'NON-ESSENTIAL – Subscriptions (Gaming)'
    if 'TEAMSNAP' in d:                             return 'NON-ESSENTIAL – Subscriptions (Kids Sports)'
    if 'APPLE.COM/BILL' in d or 'PP*APPLE.COM' in d: return 'NON-ESSENTIAL – Subscriptions (Apple)'
    if 'GOOGLE STOR' in d or 'PP*GOOGLE' in d:     return 'NON-ESSENTIAL – Subscriptions (Google)'
    if 'MICROSOFT' in d or 'MSBILL' in d:          return 'NON-ESSENTIAL – Subscriptions (Microsoft)'
    if 'TITLE LOCK' in d:                           return 'NON-ESSENTIAL – Subscriptions (Title Lock)'
    if 'PURITYHAIR' in d:                           return 'NON-ESSENTIAL – Subscriptions (Hair Care)'
    if 'KINDLE' in d:                               return 'NON-ESSENTIAL – Subscriptions (Kindle)'
    if 'HOSTGATOR' in d or 'GODADDY' in d:         return 'NON-ESSENTIAL – Subscriptions (Web Hosting)'
    if 'OPENROUTER' in d:                           return 'NON-ESSENTIAL – Subscriptions (AI/Tech)'
    if 'PATREON' in d or 'DASHPASS' in d or 'RENTAPPLICATION' in d or \
       'CLOVER APP' in d:                           return 'NON-ESSENTIAL – Subscriptions (Other)'

    # Shopping
    if any(x in d for x in ['AMZN MKTP','AMAZON MKTP','AMAZON MKTPL']) or \
       ('AMAZON.COM' in d and 'PRIME' not in d):   return 'NON-ESSENTIAL – Shopping (Amazon)'
    if any(x in d for x in ['MACY','NORDSTROM','H&M','KIMONO','GAP US','CASSARAS']): return 'NON-ESSENTIAL – Shopping (Clothing)'
    if any(x in d for x in ['SEPHORA','SALLY BEAUTY','US HAIR','GLAMOR BEAUTY']): return 'NON-ESSENTIAL – Shopping (Beauty)'
    if 'GIVEN GOLD' in d:                           return 'NON-ESSENTIAL – Shopping (Jewelry)'
    if any(x in d for x in ['BLICK ART','MICHAELS']):return 'NON-ESSENTIAL – Shopping (Arts & Crafts)'
    if any(x in d for x in ['NZXT','APPLE & MAC']): return 'NON-ESSENTIAL – Shopping (Electronics)'
    if any(x in d for x in ['QUALITY CARPETS','UHURU FURNITURE']): return 'NON-ESSENTIAL – Shopping (Home/Furniture)'
    if 'WAL-MART' in d or 'WALMART' in d:          return 'NON-ESSENTIAL – Shopping (Walmart)'
    if any(x in d for x in ['BIG 5 SPORTING','EAST BAY SPORTS','MIKE MURPHY BASEBALL']): return 'NON-ESSENTIAL – Shopping (Sports Equipment)'
    if '1800FLOWERS' in d or 'AVAS FLOWERS' in d:  return 'NON-ESSENTIAL – Shopping (Gifts/Flowers)'
    if 'EXTRA SPACE' in d:                          return 'NON-ESSENTIAL – Shopping (Storage Unit)'
    if 'EBAY' in d:                                 return 'NON-ESSENTIAL – Shopping (eBay)'
    if any(x in d for x in ['COLE HARDWARE','ROSS STORES','ENTOURAGE YEARBOOKS',
       'DHONDUP GIFT','ARTS AFRICAINS']):            return 'NON-ESSENTIAL – Shopping (Misc)'

    # Travel
    if any(x in d for x in ['SOUTHWEST','SPIRIT AIRL','FRONTIER AI','ALASKA AIR',
       'DELTA AIR','ASAPTICKETS','UNITED AIRLINES']): return 'NON-ESSENTIAL – Travel (Flights)'
    if 'EXPEDIA' in d or 'RENTALCAR' in d:          return 'NON-ESSENTIAL – Travel (Booking)'
    if 'AIRBNB' in d:                               return 'NON-ESSENTIAL – Travel (Airbnb)'
    if 'WESTIN' in d or 'MARRIOTT' in d or 'HILTON' in d or \
       ('HOTEL' in d and 'PAYPAL' not in d):        return 'NON-ESSENTIAL – Travel (Hotel)'
    if any(x in d for x in ['CATALINA','AVALON','DESCANSO','ISLAND SPA']): return 'NON-ESSENTIAL – Travel (Catalina)'
    if 'PARKING' in d or 'PARK METER' in d or 'PROPARK' in d or 'IMPARK' in d: return 'NON-ESSENTIAL – Travel (Parking)'
    if 'ALLIANZ INSURANCE' in d or 'SPIRIT TRAVEL GUARD' in d: return 'NON-ESSENTIAL – Travel (Insurance)'

    # Entertainment
    if any(x in d for x in ['OAKLAND ZOO','AMK OAKLAND COL','MYFEVO']): return 'NON-ESSENTIAL – Entertainment (Events)'
    if 'SANDBOX VR' in d or 'K1 SPEED' in d:       return 'NON-ESSENTIAL – Entertainment (Activities)'

    # Education extras
    if 'ROSETTA STONE' in d or 'KUNDUZ' in d:      return 'NON-ESSENTIAL – Education (Language/Learning App)'
    if 'EXAMFX' in d or 'PSI SERVICES' in d:       return 'NON-ESSENTIAL – Education (Licensing Exams)'
    if any(x in d for x in ['US SPORTS CAMPS','BRENTWOOD PONY']): return 'NON-ESSENTIAL – Education (Kids Sports)'
    if any(x in d for x in ['SAN JOSE STATE','STANFORD UNIV','COASTLINEACADEMY']): return 'NON-ESSENTIAL – Education (Online Courses)'

    # Transfers out
    if 'ZELLE' in d:                                return 'Transfer – Zelle Out'
    if 'VENMO' in d:                                return 'Transfer – Venmo Out'
    if 'TAPTAP SEND' in d or 'RIA FINANCIAL' in d or 'RIAMONEYTRANSFER' in d: return "NON-ESSENTIAL – Int'l Money Transfer"
    if 'IDT' in d or 'BOSS REVOLUTION' in d or 'IDT BOSS' in d: return "NON-ESSENTIAL – Int'l Calling (IDT)"
    if 'PAYPAL' in d:                               return 'NON-ESSENTIAL – PayPal (misc)'

    # Bank fees
    if any(x in d for x in ['NON-CHASE ATM FEE','WIRE FEE','SERVICE FEE',
       'CARD REPLACEMENT','STOP PAYMENT','LEGAL PROCESSING FEE',
       'DEPOSITED ITEM RETURNED','OFFICIAL CHECKS']):return 'Essential – Bank Fees'

    if 'NON-CHASE ATM WITHDRAW' in d or 'WITHDRAWAL' in d: return 'Cash Withdrawal'
    if any(x in d for x in ['PET FOOD EXPRESS','PET SUPPLIES PLUS','PETCO']): return 'NON-ESSENTIAL – Pet Supplies'
    if 'TAMMYS NAILS' in d or 'CURVCORRECT' in d:  return 'NON-ESSENTIAL – Personal Care'
    if 'USPS' in d or 'UPS STORE' in d:            return 'NON-ESSENTIAL – Shipping'
    if 'LYFT' in d or 'CLIPPER' in d:              return 'NON-ESSENTIAL – Transport'

    return 'NON-ESSENTIAL – Other/Uncategorized'
