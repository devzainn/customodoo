from odoo import models, fields, api
import requests
import json
from odoo import http
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class HmsPatient(models.Model):
    _inherit = 'hms.patient'
    description = 'Inherit Hms Patient'
    _translate = True
    
    _sql_constraints = [
        (
            "gov_code_uniq",
            "unique (gov_code)",
            "Nomor KTP tidak boleh sama dengan data yang sudah ada disistem",
        )
    ]
    # Address Lengkap
    rukun_tetangga = fields.Char('RT')
    rukun_warga = fields.Char('RW')
    kabupaten_id = fields.Many2one(comodel_name='res.kabupaten',
                                   string="Kabupaten/Kota", ondelete='set null', index=True, contex={}, domain=[])
    kecamatan_id = fields.Many2one(comodel_name='res.kecamatan',
                                   string="Kecamatan", ondelete='set null', index=True, contex={}, domain=[])
    kelurahan_id = fields.Many2one(comodel_name='res.kelurahan',
                                   string="Kelurahan", ondelete='set null', index=True, contex={}, domain=[])
    ktp = fields.Binary('KTP', attachment=True)
    bebas_biaya = fields.Binary('Bebas Biaya', attachment=True)
    national_custom_mcs = fields.Selection([
        ('wni', 'WNI'),
        ('wna', 'WNA')
    ], string='Nationality')
    # kode_pos = fields.Char(related='kelurahan_id.zip', string="Kode Pos")

    accupation_id = fields.Many2one('master.job.patient', string='Pekerjaan')
    religion_id = fields.Many2one('master.religion.patient', string='Agama')

    @api.onchange('accupation_id')
    def _onchange_accupation_id(self):
        self.occupation = self.accupation_id.name
    
    @api.onchange('religion_id')
    def _onchange_religion_id(self):
        self.religion = self.religion_id.name

    education_select = fields.Selection([
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sederajat', 'SLTA/Sederajat'),
        ('d1', 'D1'),
        ('d2', 'D2'),
        ('d3','D3'),
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3','S3')
    ], string='Education')
    
    @api.onchange('education_select')
    def _onchange_education_select(self):
        string = False
        if self.education_select =="sd":
            string = "SD"
        if self.education_select == "smp":
            string ="SMP"
        if self.education_select == "sma":
            string = "SMA"
        if self.education_select == "s1":
            string = "S1"
        if self.education_select == "s2":
            string = "S2"
        if self.education_select == "s3":
            string = "S3"
        self.education = string
        
    def button_generate_api(self, **kw):
        url = "http://localhost:8069/api"

        data_patient = [
            {
                "name": "Salman",
                "code": "adsa12"
            },
            {
                "name": "Jajang",
                "code": "asdkk1"
            }
        ]
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json", "Catch-Control": "no-cache"}

        response = requests.post(
            url, verify=False, json=json.dumps(data_patient), headers=headers)

        create_data = http.request.env['hms.patient'].sudo().create(
            data_patient)
        # for c in create_data:
        #     if c[0]['name'] == c[0]['name']:
        #         c = c.unlink()

        if response.status_code == "200":
            print(response.json)

        else:
            print("Gagal mengambil data json")
        # patient = []
        # for data in data_patient:
        #     patient.append(data)
        #     # print(patient, "==================")

        # http.request.env['hms.patient'].sudo().create(patient)

        # return patient

    # Isi field country dengan default country Indonesia
    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search(
            [('code', '=', 'ID')], limit=1)
        return country

    country_id = fields.Many2one(
        'res.country', string='Country', default=_get_default_country)

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id:  # kalau state_id ada isinya
            return {'domain': {'kabupaten_id': [('state_id', '=', self.state_id.id)]}}
        else:
            return {'domain': {'kabupaten_id': []}}

    @api.onchange('kabupaten_id')
    def _onchange_kabupaten_id(self):
        if self.kabupaten_id:  # kalau kabupaten id ada isinya
            return {'domain': {'kecamatan_id': [('kabupaten_id', '=', self.kabupaten_id.id)]}}
        else:
            return {'domain': {'kecamatan_id': []}}

    @api.onchange('kecamatan_id')
    def _onchange_kecamatan_id(self):
        if self.kecamatan_id:  # kalau kecamatan id ada isinya
            return {'domain': {'kelurahan_id': [('kecamatan_id', '=', self.kecamatan_id.id)]}}
        else:
            return {'domain': {'kelurahan_id': []}}

    @api.onchange('kelurahan_id')
    def _oncchange_kelurahan_id(self):
        self.zip = self.kelurahan_id.zip

    bahasa_yang_dikuasai_ids = fields.Many2many(
        'res.country', string='Bahasa Yang Dikuasai')

    identification_code = fields.Integer('Identification Code')
    nomor_induk_kependudukan = fields.Integer('Nomor Induk Kependudukan(NIK)')
    passport_number = fields.Integer('Passport Number')
    nama_ibu_kandung = fields.Char('Nama Ibu Kandung')
    tempat_lahir = fields.Char('Tempat Lahir')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    jenis_kelamin = fields.Selection([
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Jenis Kelamin')
    agama = fields.Selection([
        ('islam', 'Islam'),
        ('kristen', 'Protestan'),
        ('katolik', 'Katolik'),
        ('hindu', 'Hindu'),
        ('budha', 'Budha'),
        ('konghucu', 'Konghucu'),
        ('penghayat', 'Penghayat'),
        ('dll', 'DLL')
    ], string='Agama')
    nomor_telepon = fields.Integer('Nomor Telepon')
    nomor_handphone = fields.Char('Nomor Handphone')
    pendidikan = fields.Char('Pendidikan')
    pekerjaan = fields.Char('Pekerjaan')
    status_pernikahan = fields.Char('Status Pernikahan')
    code_print = fields.Char(compute='_compute_code_print', string='Cetakan No RM', store=False)
    
    @api.depends('code')
    def _compute_code_print(self):
        for rec in self:
            if rec.code:
                separated_string = '-'.join(rec.code[i:i+2] for i in range(0, len(rec.code), 2))
                rec.code_print = separated_string
            else:
                rec.code_print = False
    

    def name_get(self):
        result = []
        for record in self:
            # name = '[' + record.code + ']' + ' ' + record.name
            name = record.name
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        new_seq = self.env["ir.sequence"].next_by_code("new.patient.cust.seq") or "0"
        res = super(HmsPatient,self).create(vals)
        new_seq = int(new_seq)
        str_number = str(new_seq)
        while len(str_number) < 8:
            str_number = "0" + str_number

        norm = ""
        while str_number:
            norm += str_number[len(str_number) - 2:]
            str_number = str_number[:len(str_number) - 2]
        res.code = norm
        # raise ValidationError(("New Seq: %s\n\n Code: %s" % (norm,res.code)))
        return res

class HmsPatienReligion(models.Model):
    _name="master.religion.patient"
    _description = 'Master Data Agama Pasien'

    name = fields.Char('Nama Agama')

class HmsPatienJob(models.Model):
    _name="master.job.patient"
    _description = 'Master Data Pekerjaan Pasien'

    name = fields.Char('Nama Pekerjaan')