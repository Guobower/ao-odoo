# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
"""
Description
-----------
This script intends to be used to reclassify consumables that are
held with real-time inventory valuation to periodical.

Dependencies
------------
None

"""
import xmlrpclib

username = raw_input("User name: ")
pwd = raw_input("Password: ")
dbname = raw_input("Database name: ")
server_url = raw_input("Server URL: ")

server_xmlrpc_common = '%s/xmlrpc/common' % server_url
server_xmlrpc_object = '%s/xmlrpc/object' % server_url

# Get the uid
sock_common = xmlrpclib.ServerProxy(server_xmlrpc_common)

uid = sock_common.login(dbname, username, pwd)

# replace localhost with the address of the server
sock = xmlrpclib.ServerProxy(server_xmlrpc_object)

# Identify consumable products that have real-time inventory valuation
args = [('type', '=', 'consu'),
        ('valuation', '=', 'real_time')]
product_ids = sock.execute(dbname, uid, pwd, 'product.template', 'search',
                           args)

# Select ir.property records
args = [('name', '=', 'cost method'),
        ('res_id', 'in', ['product.template,%s' % product_id for product_id
                          in product_ids])]

ir_property_ids = sock.execute(dbname, uid, pwd, 'ir.property', 'search',
                           args)


sock.execute(dbname, uid, pwd, 'ir.property', 'write',
             product_ids, {'value_text': 'manual_periodic'})

print '%s Consumables reclassified to periodic valuation' % len(product_ids)
