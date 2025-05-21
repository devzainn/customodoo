from __future__ import division
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)
import math
import io
import pytz
import ast
import json
from pytz import timezone
from odoo import http, _, exceptions, fields
from odoo.http import request,Response
from datetime import datetime,timedelta
from psycopg2 import IntegrityError
from odoo.tools import mute_logger,DEFAULT_SERVER_DATETIME_FORMAT
import os
try:
    import json
except Exception as e:
     _logger.error(e)


class OrgatexApi(http.Controller):

    @http.route('/api/orgatex/get', type='http', methods=["GET"], auth="public", csrf=False)
    def get_line_data(self, **params):
        try:
            record_id = params.get('id')
            if not record_id:
                response = {
                    "message": "error",
                    "error": "Missing 'id' parameter"
                }
                return http.Response(
                    json.dumps(response),
                    status=400,
                    mimetype='application/json'
                )

            dyeing_record = request.env['color.kitchen.dyeing'].sudo().search([('id', '=', int(record_id))], limit=1)
            
            if not dyeing_record:
                response = {
                    "message": "error",
                    "error": "Record not found"
                }
                return http.Response(
                    json.dumps(response),
                    status=404,
                    mimetype='application/json'
                )

            data = []
            for line in dyeing_record.line_ids:
                data.append({
                    "product_name": line.product_id.name if line.product_id else "No Product",
                    "qty_receipt": line.qty_receipt if hasattr(line, 'qty_receipt') else 0.0
                })

            response = {
                "message": "success",
                "record_id": dyeing_record.id,
                "length": len(data),
                "data": data
            }
            return http.Response(
                json.dumps(response, default=str),
                status=200,
                mimetype='application/json'
            )

        except Exception as e:
            _logger.warning("Error in get_line_data: %s", e)
            response = {
                "message": "error",
                "error": str(e)
            }
            return http.Response(
                json.dumps(response),
                status=500,
                mimetype='application/json'
            )

    @http.route('/api/orgatex/post', type='json', methods=["POST"], auth="public", csrf=False)
    def post_to_wn_orgatex(self, **params):
        try:
            line_data = params.get('data')
            if not line_data or not isinstance(line_data, list):
                return {"message": "error", "error": "Invalid or missing 'data' parameter"}

            for line in line_data:
                no_program = line.get('no_program')
                product_name = line.get('product_name')
                qty_receipt = line.get('qty_receipt')

                if not product_name or qty_receipt is None:
                    continue

                request.env['wn.orgatex'].sudo().create({
                    'no_program': no_program,
                    'product_name': product_name,
                    'qty_receipt': qty_receipt,
                })

            return {
                "message": "success",
                "data_count": len(line_data),
                "detail": "Data successfully posted to wn.orgatex"
            }

        except Exception as e:
            _logger.error("Error in POST to wn.orgatex: %s", e)
            return {"message": "error", "error": str(e)}


    @http.route('/api/temporary/extends', type='json', auth='public', methods=['POST'], csrf=False)
    def create_temporary_extends(self, **post):
        """
        API Endpoint untuk menerima data dan menyimpan ke tabel temporary.extends
        """
        try:
            # Ambil data dari payload
            payload = request.jsonrequest
            _logger = request.env['ir.logging']
            _logger.info("Payload received: %s", payload)

            # Validasi data wajib
            required_fields = ['data_id', 'qty_receipt', 'qty_actual']
            for field in required_fields:
                if field not in payload:
                    return {'status': 'error', 'message': "Field '{}' is required.".format(field)}

            # Buat record di temporary.extends
            record = request.env['temporary.extends'].sudo().create({
                'data_id': payload.get('data_id'),
                'qty_receipt': payload.get('qty_receipt'),
                'qty_actual': payload.get('qty_actual'),
            })

            # Response sukses
            return {
                'status': 'success',
                'message': 'Record successfully created in temporary.extends.',
                'record_id': record.id,
            }

        except Exception as e:
            # Tangani error
            return {'status': 'error', 'message': str(e)}


# import requests
# from odoo.exceptions import UserError

# def _post_data_to_wn_orgatex(self):
#     try:
#         for record in self:
#             data_to_post = []
#             for line in record.line_ids:
#                 data_to_post.append({
#                     'no_program': line.no_program,
#                     'product_name': line.product_id.name,
#                     'qty_receipt': line.qty,
#                 })

#             _logger.info("Data to Post: %s", data_to_post)

#             for data in data_to_post:
#                 _logger.info("Posting Data to wn.orgatex: %s", data)
                
#                 # Create record in wn.orgatex table
#                 orgatex_record = self.env['wn.orgatex'].sudo().create({
#                     'no_program': data['no_program'],
#                     'product_name': data['product_name'],
#                     'qty_receipt': data['qty_receipt'],
#                     'batch_ref': record.batch_ref,
#                     'source_id': record.id,
#                 })

#                 # Prepare payload for API
#                 payload = {
#                     'data_id': orgatex_record.id,
#                     'qty_receipt': orgatex_record.qty_receipt,
#                     'qty_actual': 0.0  # Default value
#                 }

#                 # Send data to external API
#                 try:
#                     api_url = "https://yourdomain.com/api/temporary/extends"  # Ganti dengan URL API
#                     headers = {'Content-Type': 'application/json'}
#                     response = requests.post(api_url, json=payload, headers=headers)

#                     if response.status_code == 200:
#                         _logger.info("Data successfully sent to external API: %s", payload)
#                     else:
#                         _logger.error("Failed to send data to external API. Status: %s, Response: %s",
#                                       response.status_code, response.text)
#                         raise UserError(_("Failed to send data to external API: %s") % response.text)

#                 except Exception as api_error:
#                     _logger.error("API Error: %s", api_error)
#                     raise UserError(_("Error while sending data to external API: %s") % api_error)

#             _logger.info("Data successfully posted to wn.orgatex and sent to external API.")

#     except Exception as e:
#         _logger.error("Error posting data: %s", e)
#         raise UserError(_("Error posting data: %s") % e)



# from odoo import http
# from odoo.http import request
# import json
# from odoo.exceptions import ValidationError

# class TemporaryExtendsAPI(http.Controller):
#     @http.route('/api/temporary/extends', type='json', auth='public', methods=['POST'], csrf=False)
#     def create_temporary_extends(self, **post):
#         """
#         API Endpoint untuk menerima data dan menyimpan ke tabel temporary.extends
#         """
#         try:
#             # Ambil data dari payload
#             payload = request.jsonrequest
#             _logger = request.env['ir.logging']
#             _logger.info("Payload received: %s", payload)

#             # Validasi data wajib
#             required_fields = ['data_id', 'qty_receipt', 'qty_actual']
#             for field in required_fields:
#                 if field not in payload:
#                     return {'status': 'error', 'message': f"Field '{field}' is required."}

#             # Buat record di temporary.extends
#             record = request.env['temporary.extends'].sudo().create({
#                 'data_id': payload.get('data_id'),
#                 'qty_receipt': payload.get('qty_receipt'),
#                 'qty_actual': payload.get('qty_actual'),
#             })

#             # Response sukses
#             return {
#                 'status': 'success',
#                 'message': 'Record successfully created in temporary.extends.',
#                 'record_id': record.id,
#             }

#         except Exception as e:
#             # Tangani error
#             return {'status': 'error', 'message': str(e)}
