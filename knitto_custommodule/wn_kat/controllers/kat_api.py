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
     
def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 404,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }
    
    
class KatApi(http.Controller):
    
    @http.route('/api/v1/kat/po/create',type='http', auth='none', methods=["POST"], csrf=False,)
    def create_pokat(self,**params):   
        try:
            
            response = None
            no_po           = params['no_po'] if 'no_po' in params else False
            tanggal         = params['tanggal'] if 'tanggal' in params else False
            id_supplier     = params['id_supplier'] if 'id_supplier' in params else False
            tanggal_kirim   = params['tanggal_kirim'] if 'tanggal_kirim' in params else False
            termin          = params['termin'] if 'termin' in params else False
            ppn             = params['ppn'] if 'ppn' in params else False
            catatan         = params['catatan'] if 'catatan' in params else False
            id_user         = params['id_user'] if 'id_user' in params else False
            jenis_kain      = params['jenis_kain'] if 'jenis_kain' in params else False
            status_hd       = params['status_hd'] if 'status_hd' in params else False
            
            no_detail       = params['no_detail'] if 'no_detail' in params else False
            id_kain         = params['id_kain'] if 'id_kain' in params else False
            jenis_kain_toko = params['jenis_kain_toko'] if 'jenis_kain_toko' in params else False
            nama_kain       = params['nama_kain'] if 'nama_kain' in params else False
            kualitas        = params['kualitas'] if 'kualitas' in params else False
            mesin           = params['mesin'] if 'mesin' in params else False
            gramasi         = params['gramasi'] if 'gramasi' in params else False
            roll            = params['roll'] if 'roll' in params else False
            berat           = params['berat'] if 'berat' in params else False
            harga           = params['harga'] if 'harga' in params else False
            id_warna        = params['id_warna'] if 'id_warna' in params else False
            nama_warna      = params['nama_warna'] if 'nama_warna' in params else False
            lebar           = params['lebar'] if 'lebar' in params else False
            status_dt       = params['status_dt'] if 'status_dt' in params else False

            # _logger.warning(history_ids)
            

            pokat           = request.env['knitto.po'].sudo().create({
                                "name":no_po,
                                "tanggal":tanggal,
                                "id_supplier":id_supplier,
                                "tanggal_kirim":tanggal_kirim,
                                "termin":termin,
                                "ppn":ppn,
                                "catatan":catatan,                                
                                "id_user":id_user,
                                "jenis_kain":jenis_kain,                                
                                "status_hd":status_hd,
                            })
            
            if pokat.id:
                pokated     = request.env['knitto.po.line'].sudo().create({
                                "no_detail":no_detail,
                                "order_id":pokat.id,
                                "no_po":pokat.name,
                                "id_kain":id_kain,
                                "jenis_kain":jenis_kain_toko,
                                "nama_kain":nama_kain,
                                "kualitas":kualitas,
                                "mesin": mesin,
                                "gramasi": gramasi,
                                "roll": roll,
                                "berat": berat,
                                "harga": harga,
                                "id_warna": id_warna,
                                "nama_warna": nama_warna,
                                "lebar": lebar,
                                "status_dt": status_dt,
                })
            
            if pokated.id:
                response ={
                    "success":True,
                    "Message": "Create PO Success !!!",
                    "data": {
                            "order no":pokat.name,
                            "id":pokat.id,
                            "tanggal":pokat.tanggal,
                            "id_supplier":pokat.id_supplier,
                            "kirim_date":pokat.tanggal_kirim,
                            "termin":pokat.termin,
                            "ppn":pokat.ppn,
                            "catatan":pokat.catatan,
                            "id_user":pokat.id_user,
                            "jenis_kain":pokat.jenis_kain,
                            "status":pokat.status_hd,
                            
                            "_no_po_detail":[{"id":line.id,"no_detail":line.no_detail,"no_po":line.no_po, "id_kain":line.id_kain, "jenis_kain":line.jenis_kain, "kualitas":line.kualitas, "mesin":line.mesin, "gramasi":line.gramasi, "roll":line.roll, "berat":line.berat, "harga":line.harga, "id_warna":line.id_warna, "lebar":line.lebar, "status":line.status_dt} for line in pokated]
                            }
                    }
            else:
                response ={
                    "success":False,
                    "Message": " Create PO Has Been Failed !!!",
                    "data": []
                }
                
            
            return Response(json.dumps(response,default=str),status=200,mimetype='application/json')
             
            
        except Exception as e:
            response={"success":False,"message":e,"length": 0,"data":[]}
            return Response(json.dumps(response,default=str),status=200,mimetype='application/json')


    @http.route('/api/v1/kat/po/search',type='http', auth='none', methods=["POST"], csrf=False,)
    def find_kartu_proses(self,**params):
        try:
            po = params['po'] if 'po' in params else False
            
            if po:
                order_kat = request.env['knitto.po'].sudo().search([('name','=',po)], limit=1)
                pokated_ids = request.env['knitto.po.line'].sudo().search([('order_id','=',order_kat.id)])
                if order_kat:
                    response = {
                        "success": True,
                        "message" : "Order Knitto Found",
                        "data" : {
                            "id":order_kat.id,
                            "name":order_kat.name,
                            "tanggal":order_kat.tanggal,
                            "id_supplier":order_kat.id_supplier,
                            "tanggal_kirim":order_kat.tanggal_kirim,
                            "termin":order_kat.termin,
                            "ppn":order_kat.ppn,
                            "catatan":order_kat.catatan,
                            "id_user":order_kat.id_user,
                            "jenis_kain":order_kat.jenis_kain,
                            "status":order_kat.status_hd,


                            "_list_detail":[{"id":line.id, "berat":line.berat, "no_po":line.no_po, "kualitas":line.kualitas, "jenis_kain":line.jenis_kain, "id_warna":line.id_warna, "no_detail":line.no_detail, "status_dt":line.status_dt, "roll":line.roll, "harga":line.harga, "gramasi":line.gramasi, "lebar":line.lebar, "nama_warna":line.nama_warna, "mesin":line.mesin, "nama_kain":line.nama_kain, "id_kain":line.id_kain} for line in pokated_ids] if len(pokated_ids) > 0 else [],
                        }
                    }
                    return Response(json.dumps(response,default=str),status=200,mimetype='application/json')
            
            response = {
                "success": False,
                "message": "Order Knitto Not Found",
                "data"   :False
            }   
        
            return Response(json.dumps(response,default=str),status=200,mimetype='application/json')
                
        
        except Exception as e:
            response={"success":False,"message":e,"length": 0,"data":[]}
            return Response(json.dumps(response,default=str),status=200,mimetype='application/json')



    #class PurchaseOrderApi(http.Controller):
    @http.route('/api/v2/kat/po/search', auth='none', method=['GET'], type='json', csrf=False)
    def search(self, **kwargs):
        purchase_obj = request.env['knitto.po']
        purchase_id  = purchase_obj.sudo().search([('name', '=', kwargs.get('no_po'))])
        pokated_ids = request.env['knitto.po.line'].sudo().search([('order_id','=',purchase_id.id)])

        line_data = []
        for line in pokated_ids:
        # for line in purchase_id.order_id:
            line_data.append({
                'no_detail':line.no_detail,
                'no_po':line.no_po,
                'id_kain':line.id_kain,
                'nama_kain':line.nama_kain,
                'jenis_kain':line.jenis_kain,
                'kualitas':line.kualitas,
                'mesin':line.mesin,
                'gramasi':line.gramasi,
                'roll':line.roll,
                'berat':line.berat,
                'harga':line.harga,
                'id_warna':line.id_warna,
                'nama_warna':line.nama_warna,
                'lebar':line.lebar,
                'status':line.status_dt
            })

        data = {
            'po_no':purchase_id.name,
            'tanggal':purchase_id.tanggal,
            'id_supplier':purchase_id.id_supplier,
            'tanggal_kirim':purchase_id.tanggal_kirim,
            'termin':purchase_id.termin,
            'ppn':purchase_id.ppn,
            'catatan':purchase_id.catatan,
            'id_user':purchase_id.id_user,
            'jenis_kain':purchase_id.jenis_kain,
            'status':purchase_id.status_hd,

            'details_pokat':line_data
        }
        return{
            'code':'200',
            'status':'success',
            'data':data
        }


    @http.route('/api/v2/kat/po/create', auth='user', methods=['POST'], type='json', csrf=False)
    def create(self, **params):        
        order = params.get('order')
        po_no = order[0]['po_no']
        tanggal = order[0]['tanggal']
        id_supplier = order[0]['id_supplier']
        jenis_kain = order[0]['jenis_kain']
        id_user = order[0]['id_user']
        ppn = order[0]['ppn']
        termin = order[0]['termin']
        catatan = order[0]['catatan']
        tanggal_kirim = order[0]['tanggal_kirim']
        status_hd = order[0]['status']

        po  = request.env['knitto.po'].sudo().search([('name','=',po_no)])

        if po:
            return{
            'status':'Nomor PO sudah terdaftar'
            }
            # pokated_ids = request.env['knitto.po.line'].sudo().search([('order_id','=',po.id)])

            # line_data = []
            # for line in pokated_ids:
            # # for line in purchase_id.order_id:
            #     line_data.append({
            #         'no_detail':line.no_detail,
            #         'no_po':line.no_po,
            #         'id_kain':line.id_kain,
            #         'nama_kain':line.nama_kain,
            #         'jenis_kain':line.jenis_kain,
            #         'kualitas':line.kualitas,
            #         'mesin':line.mesin,
            #         'gramasi':line.gramasi,
            #         'roll':line.roll,
            #         'berat':line.berat,
            #         'harga':line.harga,
            #         'id_warna':line.id_warna,
            #         'nama_warna':line.nama_warna,
            #         'lebar':line.lebar,
            #         'status':line.status_dt
            #     })

            # data = {
            #     'po_no':po.name,
            #     'tanggal':po.tanggal,
            #     'id_supplier':po.id_supplier,
            #     'tanggal_kirim':po.tanggal_kirim,
            #     'termin':po.termin,
            #     'ppn':po.ppn,
            #     'catatan':po.catatan,
            #     'id_user':po.id_user,
            #     'jenis_kain':po.jenis_kain,
            #     'status':po.status_hd,

            #     'details_pokat':line_data
            # }
            # return{
            #     'code':'200',
            #     'status':'success',
            #     'data':data
            # }

        else:
            order_ids = order[0]['order_ids']
            vals_line = []
            for line in order_ids:
                vals_line.append((0, 0, {
                    'no_detail':line.get('no_detail'),
                    'no_po':po_no,
                    'id_kain':line.get('id_kain'),
                    'nama_kain':line.get('nama_kain'),
                    'jenis_kain':line.get('jenis_kain'),
                    'kualitas':line.get('kualitas'),
                    'mesin':line.get('mesin'),
                    'gramasi':line.get('gramasi'),
                    'roll':line.get('roll'),
                    'berat':line.get('berat'),
                    'harga':line.get('harga'),
                    'id_warna':line.get('id_warna'),
                    'nama_warna':line.get('nama_warna'),
                    'lebar':line.get('lebar'),
                    'status_dt':line.get('status')
                }))

            po_vals = {
                'name':po_no,
                'tanggal':tanggal,
                'id_supplier':id_supplier,  
                'jenis_kain':jenis_kain, 
                'id_user':id_user,
                'ppn':ppn,  
                'termin':termin,   
                'catatan':catatan,
                'tanggal_kirim':tanggal_kirim, 
                'status_hd':status_hd,
                'order_ids':vals_line
            }
            new_algoritma_pembelian = request.env['knitto.po'].sudo().create(po_vals)

            return {
                'code ':'200',
                'status':'success',
                'message':po_vals
            }       
