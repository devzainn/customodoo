# from models import general
from . import general
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
import logging
_logger = logging.getLogger(__name__)


class HmsAppointment(models.Model):
    _inherit = 'hms.appointment'

    # encounter_subject = fields.Char('Encounter Subject')
    pemeriksaan_penunjang = fields.Selection([
        ('lab', 'Lab'),
        ('rad', 'Rad')
    ], string='Pemeriksaan Penunjang')

    # rujukan = fields.Selection([
    #     ('puskesmas', 'Puskemas'),
    #     ('klinik', 'Klinik'),
    #     ('bidan', 'Bidan'),
    #     ('rs_d', 'Rumah Sakit Kelas D Pratama/Setara'),
    #     ('faskes', 'Faskes Penunjang')
    # ], string='Referral Hospital')

    # detail_rujukan = fields.Text('Referral Hospital Details')

    obat_obatan_id = fields.Many2one('prescription.order', string='Obat-Obatan')
    nama_obat = fields.Char('Nama Obat')
    bentuk = fields.Char('Bentuk')
    jumlah_obat = fields.Integer('Jumlah Obat')
    metode = fields.Char('Metode')
    dosis_obat_yang_diberikan = fields.Integer('Dosis Obat Yang Diberikan')
    unit = fields.Integer('Unit')
    frekuensi = fields.Integer('Frekuensi')
    aturan_tambahan = fields.Char('Aturan Tambahan')
    diet = fields.Char('Diet')
    keadaan_umum = fields.Char('Keadaan Umum')
    pasien_id = fields.Many2one('hms.patient', string="Patient")
    objective = fields.Text('Objective')
    planning = fields.Text('Planning')

    outside_appointment_nurse = fields.Boolean()
    location_nurse = fields.Char()
    chief_complain_nurse = fields.Text()
    objective_nurse = fields.Text()
    planning_nurse = fields.Text()
    present_illness_nurse = fields.Text()
    past_history_nurse = fields.Text()
    diseases_code = fields.Char('Diseases')
    diseases_ids = fields.Many2many('hms.diseases', string='ICD-10 Diseases Secondary')
    diseases_ids_primary = fields.Many2one('hms.diseases', string='ICD-10 Diseases Primary')

    assess_nurse_id = fields.Many2one('master.data', string='Assessment Nurse')
    
    no_rm = fields.Char(string='No. RM')
    is_hamil = fields.Boolean(string="Hamil")
    gender = fields.Char(string='Gender')
    keterangan_kesehatan = fields.Selection([('sehat','Sehat'),('sakit','Sakit'),],string="Keterangan Kesehatan")

    # CPPT
    soap_sbar = fields.Selection(string='SOAP/SBAR', selection=[('soap', 'SOAP'), ('sbar', 'SBAR'),], default='soap', required=True)
    custom_user_id = fields.Many2one(comodel_name='res.users', string='User', default=lambda self: self.env.user, compute='_compute_custom_user_id')
    custom_role_id = fields.Many2many(comodel_name='security.role', string='Roles', default=lambda self: self.env.user.security_role_ids, compute='_compute_custom_user_id')

    # SOAP FIELD START HERE
    dokter_konsul_id = fields.Many2one('hms.physician', string='Dr. Konsul', domain=[('peran', '=', 'dokter')])
    subjective_cppt = fields.Text('Subjective CPPT')
    objective_cppt = fields.Text('Objective CPPT')
    
    # custom_nurse_ids = fields.One2many(comodel_name='master.data', inverse_name='custom_pemeriksaan_id', string='Nurse')
    # nurse_id = fields.Many2one('master.data', string='Nurse')

    # costum_data_nurse_ids = fields.Many2many(
    #     comodel_name='master.data', 
    #     string='Nurse'
    #     )

    gizi_id = fields.Many2one('master.diagnosa_gizi', string='Assessment')

    # diagnosa_id = fields.Many2one('hms.diseases', string='Diagnosa')
    diagnosa_pasien_ids = fields.Many2many(
        comodel_name='hms.diseases', 
        string='Dianosa Pasien'
        )
    
    interverensi = fields.Text('Interverensi')
    monitoring = fields.Text('Monitoring')
    evaluasi = fields.Text('Evaluasi')

    planning_cppt = fields.Text('Planning')

    # SBAR FIELD START HERE
    situation = fields.Text('Situation')
    background = fields.Text('Background')
    assessment = fields.Text('Assessment')
    recomendation = fields.Text('Recomendation')
    instruction = fields.Text('Instruction')
    review = fields.Text('Review')

    master_vital_cppt_ids = fields.One2many(
        comodel_name='mcs_hms.detailtandavital_cppt',
        inverse_name='appointment_igd_id',
        string='Patient Vital Sign',
    )

    cppt_suster_dokter_ids = fields.One2many(comodel_name='cppt.patient', inverse_name='appointment_id', string='CPPT Suster Dokter')

    def _compute_custom_user_id(self):
        for rec in self:
            rec.custom_user_id = self.env.user.id if self.env.user else None
            rec.custom_role_id = self.env.user.security_role_ids

    def action_view_default_vital_cppt(self):
        self.ensure_one() 

        default_vital = self.env['master.default_vital'].search([('layanan_id', '=', self.department_id.id), ('default', '=', True)], limit=1)
        if default_vital:
            
            self.default_vital_id = default_vital.id
            vital_saved = self.env['mcs_hms.detailtandavital_cppt'].search([('appointment_igd_id','=',self.id)])
            self.master_vital_cppt_ids = [(5,0,0)]
            if vital_saved: 
                master_vital_data = [(0, 0, {'vital_id': vital.vital_id.id, 'nilai': vital.nilai, 'keterangan': vital.keterangan}) for vital in vital_saved]
                self.master_vital_cppt_ids = master_vital_data
                for master_vital_data in self.master_vital_cppt_ids:
                    vital = self.env['master.tanda_vital'].browse(master_vital_data['vital_id'].id)
                    master_vital_data['uom_id'] = vital.satuan.id
            else:    
                vital_ids = default_vital.vital_ids
                master_vital_data = [(0, 0, {'vital_id': vital.id, 'nilai': 0, 'keterangan': ''}) for vital in vital_ids]

                self.master_vital_cppt_ids = master_vital_data
                for master_vital_data in self.master_vital_cppt_ids:
                    vital = self.env['master.tanda_vital'].browse(master_vital_data['vital_id'].id)
                    master_vital_data['uom_id'] = vital.satuan.id
        else:
            self.default_vital_id = False

        form_id = self.env.ref('mcs_hms_emergency.isi_ttv_default_vital_cppt_form_view').id
        return {
            'name': 'Default Vital',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hms.appointment',
            'views': [(form_id, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new'
        }

    def action_save_vital_sign_cppt(self):
        for rec in self:
            rec.write({
                'default_vital_id': rec.default_vital_id.id,
                'master_vital_cppt_ids': rec.master_vital_cppt_ids
            })
            self.fill_object_appointment_cppt()

    def fill_object_appointment_cppt(self):
        for rec in self:
            appointment_cppt = []
            number = 1
            for rec1 in rec.master_vital_cppt_ids:
                vital = ""
                if rec1.vital_id:
                    vital += "%s." %(number) + str(rec1.vital_id.name)
                if rec1.nilai:
                    vital += ": " + str(rec1.nilai)
                    if rec1.keterangan:
                        vital += ", " + rec1.keterangan
                    number += 1
                    appointment_cppt.append(vital)
            appointment_str = "\n".join(appointment_cppt)
            rec.objective_cppt = appointment_str or ""

    # def action_add_cppt_suster_dokter(self):
    #     for rec in self:
    #         patograf_obj = self.env['mcs_rs.patograf']
    #         rec.cppt_suster_dokter_ids = general.list_cppt_dokter_suster(parent=rec)
    #         if rec.dokter_konsul_id:
    #             rec.dokter_konsul_ids = [(4, rec.dokter_konsul_id.id)]
    #         for cst in general.fields_cppt_suster_dokter:
    #             if cst == 'custom_assessment_doctor_ids':
    #                 list_doctor = []
    #                 for doctor in rec[cst]:
    #                     doctor.write({'custom_ar_id': rec.arrival_id.id})
    #                     list_doctor.append([4, doctor.id])
    #                 rec.indication_ids = list_doctor
    #             rec[cst] = None
    #         for pd in rec.pemeriksaan_detil_ids:
    #             patograf = patograf_obj.search([('triase_id', '=', rec.id), ('vital_id', '=', pd.vital_id.id)])
    #             copy_pemeriksaan = {
    #                 'vital_id': pd.vital_id.id,
    #                 'nilai': pd.nilai,
    #                 'uom_id': pd.uom_id.id,
    #                 'keterangan': pd.keterangan
    #             }
    #             if patograf:
    #                 patograf.pemeriksaan_detail_ids = [(0, 0, copy_pemeriksaan)]
    #             else:
    #                 patograf_obj.create({
    #                     'triase_id': rec.id,
    #                     'vital_id': pd.vital_id.id,
    #                     'pemeriksaan_detail_ids': [(0, 0, copy_pemeriksaan)]
    #                 })

    def action_add_cppt(self):
        for rec in self:
            rec.cppt_suster_dokter_ids = general.list_cppt_patient(parent=rec)
            # for pd in rec.master_vital_ids:
            #     get_pemeriksaan = {
            #         'vital_id' : pd.vital_id.id,
            #         'nilai' : pd.nilai,
            #         'uom_id' : pd.uom_id.id,
            #         'keterangan' : pd.keterangan
            #     }

    @api.onchange('patient_id')
    def _onchange_patient_id_inherit(self):
        self.no_rm = self.patient_id.code
        self.gender = self.patient_id.gender

    #update penambahan fungsi untuk mengupdate diseases_code
    def action_radiology_request(self):
        res = super(HmsAppointment,self).action_radiology_request()
        context = res.get('context',{})
        diseases_code = self.diseases_code
        gender = self.gender
        hamil = self.is_hamil
        context.update({
            'default_diseases_code': diseases_code,
            'default_is_hamil':hamil,
            'default_gender':gender,
        })
        # raise ValidationError(("%s" % context))
        res['context'] = context
        return res

    def dupp_asses_doc(self):
        self.outside_appointment = self.outside_appointment_nurse
        self.location = self.location_nurse
        self.chief_complain = self.chief_complain_nurse
        self.objective = self.objective_nurse
        self.planning = self.planning_nurse
        self.present_illness = self.present_illness_nurse
        self.past_history = self.past_history_nurse
        
    is_soap_doc = fields.Boolean(compute='_compute_is_soap_doc', string='SOAP DOC')
    
    @api.depends('objective')
    def _compute_is_soap_doc(self):
        for rec in self:
            check = True  # Assume True initially
            # print("ID: %s \n\n Objective: %s" % (rec.id,rec.objective))
            # _logger.info("ID: %s \n\n Objective: %s" % (rec.id,rec.objective))
            if not rec.objective:
                check = False
            # if rec.is_cito:  # TODO ERROR
            #     check = True
            rec.is_soap_doc = check

    cara_pembayaran = fields.Selection([
        ('personal', 'Umum'),
        ('asuransi', 'Asuransi'),
        ('korporat', 'Perusahaan'),
        ('bpjs', 'BPJS Kesehatan')
    ], string='Cara Pembayaran')

    cara_pulang = fields.Selection([
        ('persetujuan_dokter', 'Atas persetujuan Dokter'),
        ('dirujuk', 'Dirujuk'),
        ('aps', 'Atas Permintaan Sendiri'),
        ('meninggal', 'Meninggal'),
        ('lain_lain', 'Lain-lain'),
    ], 'Cara Pulang')

    encounter_status = fields.Selection([
        ('planned', 'Planned'),
        ('arrived', 'Arrived'),
        ('triaged', 'Triaged'),
        ('inprogress', 'Inprogress'),
        ('onleave', 'Onleave'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')
    ], string='Encounter Status')

    tipe_registrasi = fields.Selection([
        ('rajal', 'Rawat Jalan'),
        ('ranap', 'Rawat Inap'),
        ('igd', 'IGD'),
        ('support', 'Support')
    ], string='Tipe Registrasi')

    master_appointment_id = fields.Many2one('master.status.observation', string='Master Status Observation')
    master_data_id = fields.Many2many('master.data', string='Master Data')  # TODO FIX
    # master_data_ids = fields.Many2many('master.data', string='Master Data') #penambahan atas permintaan kak popi
    state = fields.Selection(selection_add=[
        ('confirm', 'Confirmed'),('nurse', 'Nurse Station'),('waiting', 'Waiting'), ('in_consultation', 'Physician')
    ], string='state', ondelete={'nurse': 'set default', 'confirm': 'set default'})
    # rujukan = fields.Selection(
    #     string='Rujukan',
    #     selection=[('puskesmas', 'Puskesmas'),
    #                ('klinik', 'Klinik'),
    #                ('bidan', 'Bidan'),
    #                ('rskd', 'Rumah Sakit Kelas D Pratama / setara'),
    #                ('faskes_penunjang', 'Faskes Penunjang'),
    #                 ('dll', 'Lain-lain')
    #                ])
    rujukan = fields.Char('Rujukan')
    keterangan = fields.Text(string="Keterangan")

    @api.onchange('tipe_registrasi')
    def onchange_registrasi(self):
        if self.tipe_registrasi == 'igd':
            # self.physician_id.required=False
            return {'domain' : {'department_id': [('department_type', '=', 'emergency_department')]}}
        else :
            return {'domain' : {'department_id': []}}
    def btn_nurse_station(self):
        self.state = 'nurse'
    # @api.constrains('schedule_slot_id')
    # def schedule_slot(self):
    #     for rec in self:
    #         if not rec.schedule_slot_id :
    #             raise ValidationError('Schedule Kosong')

    # fungsi kit lines
    def get_acs_kit_lines(self):
        if not self.acs_kit_id:
            raise UserError("Please Select Kit first.")

        consumable_list = []
        plist = []
        count = 0
        for cons in self.consumable_line_ids:
            consumable_list.append({
                'product_id': cons.product_id.id,
                'product_uom': cons.product_uom.id,
                'qty': cons.qty,
                'price_unit': cons.product_id.list_price
            })
        self.consumable_line_ids.unlink()
        lines = []
        for line in self.acs_kit_id.acs_kit_line_ids:
            kali = line.product_qty * self.acs_kit_qty
            if consumable_list:
                for consumable_line in consumable_list:
                    plist.append(int(consumable_line['product_id']))
                    if line.product_id.id == int(consumable_line['product_id']):
                        lines.append([0,0,{ 
                            'product_id': consumable_line['product_id'],
                            'product_uom': consumable_line['product_uom'],
                            'price_unit': consumable_line['price_unit'],
                            'qty': consumable_line['qty'] + 1,
                        }])
                    count += 1
            else:
                lines.append((0,0,{
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_id.id,
                    'qty': kali,
                    'price_unit': line.product_id.list_price
                }))
        self.consumable_line_ids = lines

    def acs_appointment_inv_product_data(self, with_product=True):
        product_data = []
        if with_product:
            product_id = self.product_id
            if not product_id:
                raise UserError(_("Please Set Consultation Service first."))

            product_data = [{'product_id': product_id}]

        if self.consumable_line_ids:
            product_data.append({
                'name': _("Consumed Product/services"),
            })
            for consumable in self.consumable_line_ids:
                product_data.append({
                    'product_id': consumable.product_id,
                    'quantity': consumable.qty,
                    'price_unit': consumable.price_unit,
                    'lot_id': consumable.lot_id and consumable.lot_id.id or False,
                })

        if self._context.get('with_procedure'):
            if self.procedure_to_invoice_ids:
                product_data.append({
                    'name': _("Patient Procedure Charges"),
                })
                for procedure in self.procedure_to_invoice_ids:
                    product_data.append({
                        'product_id': procedure.product_id,
                        'price_unit': procedure.price_unit,
                    })

        return product_data

    # fungsi rec count pada smartbutton lab request
    def _rec_count(self):
        for rec in self:
            c = 0
            for res in rec.lab_request_ids:
                if res.patient_id == rec.patient_id:
                    c += 1
            rec.request_count = c
            rec.test_count = len(rec.test_ids)

    def appointment_confirm(self):
        res = super(HmsAppointment, self).appointment_confirm()
        if self.patient_id:
            product_id = self.patient_id.registration_product_id or self.env.user.company_id.patient_registration_product_id
            lines = [(0, 0, {
                'product_id': product_id.id,
                'product_uom': product_id.uom_id.id,
                'qty': 1,
                'price_unit': product_id.list_price
            })]
            self.consumable_line_ids = lines
            
            if not self.invoice_id and self.tipe_registrasi != 'mcu':
                self.create_invoice() 
        return res

    def appointment_waiting(self):
        res = super(HmsAppointment, self).appointment_waiting()
        if self.tipe_registrasi == 'rajal' and (not self.chief_complain_nurse or not self.objective_nurse or not self.planning_nurse or not self.past_history_nurse):
            raise ValidationError(_("Harap isi terlebih dahulu SOAP Perawat"))

        objective = "Weight: %s, Height: %s, Temp: %s, HR: %s, RR: %s, Systolic/Diastolic BP: %s, SpO2: %s, RBS: %s" \
                    % (self.weight, self.height, self.temp, self.hr, self.rr, self.systolic_bp, self.spo2, self.rbs)
        self.objective = objective
        return res

    def consultation_done(self):
        res = super(HmsAppointment, self).consultation_done()
        self.date_to = fields.Datetime.now()
        # if not self.invoice_id and (self.cara_pembayaran == "korporat" or self.cara_pembayaran == "bpjs"):
        #     self.create_invoice()
        return res

    patient_tb = fields.Char(compute='_compute_patient_tb', string='patient_tb')
    
    @api.depends('diseases_ids_primary','diseases_ids')
    def _compute_patient_tb(self):
        for rec in self:
            string = False
            diseases_history = rec.patient_id.patient_diseases_ids
            stopper = 0
            stopper_2 = 0
            stopper_3 = 0
            if len(rec.diseases_ids) > 0:
                for record in rec.diseases_ids:
                    if record.is_tb and stopper == 0:
                        stopper = 1
                        string = "Pasien TB Baru"
                        for records in diseases_history:
                            if records.disease.is_tb and stopper_2 == 0:
                                string = "Pasien TB"
                                stopper = 1
                            
            if rec.diseases_ids_primary.is_tb:
                string = "Pasien TB Baru"
                for records in diseases_history:
                    if records.disease.is_tb and stopper_3 == 0:
                        string = "Pasien TB"

            rec.patient_tb = string 

class Diseases(models.Model):
    _inherit = 'hms.diseases'

    def name_get(self):
        result = []
        for record in self:
            code = record.code or ''
            name = code + " - " + record.name
            result.append((record.id, name))

        return result
    
    is_tb = fields.Boolean('Tuberkulosis', default=False)


class MasterDiagnosis(models.Model):
    _name = 'master.diagnosis'
    description = 'Master Diagnosis'

    encounter_diagnosis = fields.Char('Encounter Diagnosis')
    code = fields.Char('Code')
    keterangan = fields.Text('Keterangan')


class MasterStatusObservation(models.Model):
    _name = 'master.status.observation'
    description = 'Master Status Observation'

    # Status Observasi
    lvl = fields.Integer('lvl')
    observation_status = fields.Char('Observation Status')
    keterangan = fields.Text('keterangan')


class MasterData(models.Model):
    _name = 'master.data'
    _rec_name = 'observation_display_name'
    _description = 'Master Data'

    observation_code = fields.Char('Code', required=True)
    observation_display_name = fields.Char('Assessment Nurse', required=True)
    keterangan = fields.Text('Information')
    custom_pemeriksaan_id = fields.Many2one(comodel_name='hms.appointment', string='Custom Pemeriksaan')
    custom_pemeriksaan_id_dua = fields.Many2one(comodel_name='hms.appointment', string='Custom Pemeriksaan')

    category_id = fields.Many2one(comodel_name='master.diagnosis_keperawatan_kategori', string='Category')
    sub_category_id = fields.Many2one(comodel_name='master.diagnosis_keperawatan_kategori', string='Sub Category')

    def name_get(self):
        result = []
        for record in self:
            code = record.observation_code or ''
            name = record.observation_code + " - " + record.observation_display_name
            result.append((record.id, name))

        return result


class EncounterClass(models.Model):
    _name = 'encounter.class'
    description = 'Encounter Class'

    encounter_class_code = fields.Char('Encounter Class Code')
    encounter_class_display = fields.Char('Encounter Class Display')
    keterangan = fields.Char('Keterangan')


class PatientEvaluation(models.Model):
    _inherit = 'acs.patient.evaluation'

    @api.model
    def create(self, values):
        res = super(PatientEvaluation, self).create(values)
        if res.appointment_id and res.appointment_id.state == 'nurse':
            objective = "Weight: %s, Height: %s, Temp: %s, HR: %s, RR: %s, Systolic/Diastolic BP: %s, SpO2: %s, RBS: %s" \
                        % (res.weight, res.height, res.temp, res.hr, res.rr, res.systolic_bp, res.spo2, res.rbs)
            res.appointment_id.objective_nurse = objective
        return res

class MasterTandaVital(models.Model):
    _name = 'master.tanda_vital'
    _description = 'Vital Sign Criteria'
    _order = 'sequence, id'

    name = fields.Char('Tanda Vital')
    satuan = fields.Many2one('uom.uom', string='Satuan')
    deskripsi = fields.Text(string='Deskripsi', translate=True)  
    sequence = fields.Integer(string='Sequence', default=10)
    # nilai = fields.Float('Nilai')
    # keterangan = fields.Text('Keterangan')
    
class DefaultTandaVital(models.Model):
    _name = 'master.default_vital'
    _description = 'Template Vital Sign'

    name = fields.Char('Nama')
    default = fields.Boolean('Default')
    layanan_id = fields.Many2one('hr.department', string='Layanan')
    deskripsi = fields.Text('Deskripsi')

    vital_ids = fields.Many2many('master.tanda_vital', string='Tanda Vital')

class CpptPatient(models.Model):
    _name = 'cppt.patient'
    _description = 'CPPT Patient'
    _rec_name = 'title'

    name = fields.Char('')
    title = fields.Char('')
    body = fields.Char('')
    display_type = fields.Selection(string='', selection=[('line_section', "Section"), ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    name_fields = fields.Char(string='Name Fields')

    vital_ids = fields.Many2many('master.tanda_vital', string='Tanda Vital', ondelete='cascade')
    appointment_id = fields.Many2one(comodel_name='hms.appointment', string='Appointment')

class DetailTandaVitalCppt(models.Model):
    _name = 'mcs_hms.detailtandavital_cppt'
    _description = 'Detail Tanda Vital CPPT'

    name = fields.Char('Name')
    vital_id = fields.Many2one(comodel_name='master.tanda_vital', string='Tanda Vital',
                               ondelete='set null', index=True, contex={}, domain=[])
    nilai = fields.Char(string='Nilai')
    uom_id = fields.Many2one(related='vital_id.satuan', string='Satuan')
    keterangan = fields.Char(string='Keterangan', translate=True)
    appointment_igd_id = fields.Many2one('hms.appointment', string='IGD Vital')
    
    