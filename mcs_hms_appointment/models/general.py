from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from pytz import timezone
import pytz

def _days_month_year(fields_date=None, fields_datetime=None):
    days = None
    datetimes = None
    if fields_date:
        datetimes = (datetime.strptime(str(fields_date.strftime('%Y-%m-%d')), '%Y-%m-%d'))
    elif fields_datetime:
        # datetimes = fields_datetime + timedelta(hours=7)
        datetimes = pytz.UTC.localize(fields_datetime).astimezone(timezone('Asia/Jakarta'))
        datetimes = (datetime.strptime(str(datetimes.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S'))
    if datetimes:
        days = datetimes.strftime('%d %B %Y %H:%M:%S')
    return days

def list_cppt_patient(parent,handover=False):
    def lists(lines=False, title=False, body=False, name_fields=False):
        vals = {
            'title' : title,
            'body' : body,
            'name' : title,
            'name_fields' : name_fields,
            # 'custom_ar_id' : parent.arrival_id.id
        }
        # if parent.custom_user_id:
        #     peran = parent.custom_user_id.employee_id.peran
        #     if peran == 'dokter':
        #         vals['peran'] = 'Dokter'
        #     elif peran == 'suster':
        #         vals['peran'] = 'Suster'
        if lines:
            vals['display_type'] = 'line_section'
        return vals
    vals = []
    name = ''
    if parent.custom_user_id:
        name = str(parent.custom_user_id.display_name)
    vals.append([0,0, lists(lines=True, title=name)])
    vals.append([0,0, lists(title='Tanggal dan Waktu',body=_days_month_year(fields_datetime=fields.datetime.now()))])  
    if parent.custom_user_id:
        vals.append([0,0,
            lists(title='User',
                    body=parent.custom_user_id.display_name)
        ])
    if parent.custom_role_id:
        role_list = []
        for role in parent.custom_role_id:
            role_list.append(role.display_name)
        role_list = ', '.join(role_list)
        vals.append([0,0, lists(title='Roles', body=role_list)])
    if parent.dokter_konsul_id:
        vals.append([0,0, 
            lists(title='Konsul', body=parent.dokter_konsul_id.name)])
    if parent['subjective_cppt']:
        vals.append([0,0,lists(title='Subjective',
                    body=parent['subjective_cppt'],
                    name_fields='subjective_cppt')]) 
    if parent['objective_cppt']: 
        vals.append([0,0,lists(title='Objective',
            body=parent['objective_cppt'],
            name_fields='objective_cppt')]) 
    if parent['master_data_id']:
        nurse = []
        for asn in parent['master_data_id']:
            nurse_l = str(asn.observation_display_name)
            if asn.category_id:
                nurse_l += ', category: ' + str(asn.category_id.name)
            if asn.keterangan:
                nurse_l += ', info: ' + str(asn.keterangan)
            nurse.append(str(nurse_l))
        nurse = '\n'.join(nurse)
        vals.append([0,0,
            lists(title='Assessment Nurse', body=nurse, name_fields=['master_data_id'])
        ])
        
    if parent['gizi_id']:
        gizi = []
        for asg in parent['gizi_id']:
            gizi_l = str(asg.kode)
            if asg.category_id:
                gizi_l += ', ' + str(asg.name)
            if asg.keterangan:
                gizi_l += ', ' + str(asg.deskrispi)
            gizi.append(str(gizi_l))
        gizi = '\n'.join(gizi)
        vals.append([0,0,
            lists(title='Assessment Gizi', body=gizi, name_fields=['gizi_id'])
        ])

    if parent['diagnosa_pasien_ids']:
        diseases = []
        for ds in parent['diagnosa_pasien_ids']:
            diseases_l = str(ds.name)
            if ds.category:
                diseases_l += ' - ' + str(ds.category.name)
            diseases.append(str(diseases_l))
        diseases = '\n'.join(diseases)
        vals.append([0,0,
            lists(title='Diagnosa', body=diseases, name_fields=['diagnosa_pasien_ids'])
        ])

    if parent['interverensi']:
        vals.append([0,0,lists(title='Interverensi',
                    body=parent['interverensi'],
                    name_fields='interverensi')]) 
    if parent['monitoring']:
        vals.append([0,0,lists(title='Monitoring',
                    body=parent['monitoring'],
                    name_fields='monitoring')]) 
    if parent['evaluasi']:
        vals.append([0,0,lists(title='Evaluasi',
                    body=parent['evaluasi'],
                    name_fields='evaluasi')]) 
    if parent['planning_cppt']:
        vals.append([0,0,lists(title='Planning',
                    body=parent['planning_cppt'],
                    name_fields='planning_cppt')]) 

    if parent['situation']:
        vals.append([0,0,lists(title='Situation',
                    body=parent['situation'],
                    name_fields='situation')]) 
    if parent['background']:
        vals.append([0,0,lists(title='Background',
                    body=parent['background'],
                    name_fields='background')]) 
    if parent['assessment']:
        vals.append([0,0,lists(title='Assessment',
                    body=parent['assessment'],
                    name_fields='assessment')]) 
    if parent['recomendation']:
        vals.append([0,0,lists(title='Recomendation',
                    body=parent['recomendation'],
                    name_fields='recomendation')])

    if parent['instruction']:
        vals.append([0,0,lists(title='Instruction',
                    body=parent['instruction'],
                    name_fields='instruction')]) 
    if parent['review']:
        vals.append([0,0,lists(title='Review',
                    body=parent['review'],
                    name_fields='review')])  
    return vals