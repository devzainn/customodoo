from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from datetime import datetime

class CustomModuleScanController(http.Controller):

    @http.route('/scan_form', auth='public', website=True)
    def scan_form(self, **kw):
        return request.render('custom_module_scan.custom_module_scan_landing_page')

    @http.route('/submit_scan_data', auth='public', type='http', website=True, methods=['POST'])
    def submit_scan_data(self, **post):
        employee_barcode = post.get('employee_barcode')
        kartu_proses_barcode = post.get('kartu_proses_barcode')

        print("Employee Barcode: %s" % employee_barcode)
        print("Kartu Proses Barcode: %s" % kartu_proses_barcode)

        employee = request.env['hr.employee'].search([('barcode', '=', employee_barcode)], limit=1)
        if not employee:
            error_message = "Employee with this Badge ID not found!"
            return request.render('custom_module_scan.custom_module_scan_landing_page', {
                'error_message': error_message,
            })

        kartu_proses = request.env['kartu.proses'].search([('name', '=', kartu_proses_barcode)], limit=1)
        if not kartu_proses:
            error_message = "Kartu Proses with this ID not found!"
            return request.render('custom_module_scan.custom_module_scan_landing_page', {
                'error_message': error_message,
            })

        if kartu_proses.state != 'wip':
            error_message = "The state of kartu proses is not WIP, scanning is not allowed."
            return request.render('custom_module_scan.custom_module_scan_landing_page', {
                'error_message': error_message,
            })

        return request.redirect('/process_scanning?kartu_proses_id=%d&employee_barcode=%s' % (kartu_proses.id, employee_barcode))

    @http.route('/process_scanning', auth='public', website=True)
    def process_scanning(self, **kw):
        kartu_proses_id = int(kw.get('kartu_proses_id'))
        kartu_proses = request.env['kartu.proses'].browse(kartu_proses_id)

        employee_barcode = kw.get('employee_barcode')

        proses_ids = kartu_proses.proses_ids

        proses_data = []
        machines_to_display = []
        show_dropdown = False
        dropdown_proses_id = None

        partner = request.env['res.partner'].search([('ref', '=', kartu_proses.kode_customer)], limit=1)

        all_done = True

        for proses in proses_ids:
            if proses.is_done:
                status = 'Selesai'
            elif not proses.is_done and not show_dropdown:
                status = 'Sedang Diproses'
                machines_to_display = proses.proses_master_id.mesin_ids
                show_dropdown = True 
                dropdown_proses_id = proses.id 
                all_done = False
            else:
                status = 'Belum Dimulai'
                all_done = False

            proses_info = {
                'proses_name': proses.proses_master_id.name,
                'mesin_names': [mesin.name for mesin in proses.proses_master_id.mesin_ids],
                # 'status': proses.is_done
                'status': status
            }

            if not proses.is_done and not show_dropdown:
                machines_to_display = proses.proses_master_id.mesin_ids
                show_dropdown = True 
                dropdown_proses_id = proses.id 

            proses_data.append(proses_info)

        employee = request.env['hr.employee'].search([('barcode', '=', employee_barcode)], limit=1)

        return request.render('custom_module_scan.process_scanning_page', {
            'proses_data': proses_data,  
            'kartu_proses': kartu_proses,
            'employee': employee,
            'machines': machines_to_display,
            'dropdown_proses_id' : dropdown_proses_id,
            'partner': partner,
            'all_done': all_done
        })

    @http.route('/submit_machine_selection', auth='public', type='http', website=True, methods=['POST'])
    def submit_machine_selection(self, **post):
        kartu_proses_id = int(post.get('kartu_proses_id'))
        kartu_proses = request.env['kartu.proses'].browse(kartu_proses_id)
        employee_barcode = post.get('employee_barcode')
        partner = request.env['res.partner'].search([('ref', '=', kartu_proses.kode_customer)], limit=1)

        machine_id = post.get('machine_id')
        dropdown_proses_id = post.get('dropdown_proses_id')
        manual_date = post.get('manual_date')

        print("Employee Barcode SUBMIT PROSES: %s" % employee_barcode)
        print("Kartu Proses SUBMIT PROSES: %s" % kartu_proses_id)
        print("Machine ID yang dipilih: ", machine_id)
        print("Proses IDs yang dipilih: ", dropdown_proses_id)
        print("Manual Date: ", manual_date)

        employee = request.env['hr.employee'].search([('barcode', '=', employee_barcode)], limit=1)
        if not employee:
            raise UserError("Employee not found!")

        is_manager = employee.manager

        scan_successful = False
        error_message = None 

        if dropdown_proses_id:
            print("Masuk ke dalam IF dengan key: %s" % dropdown_proses_id)

            tanggal_hari_ini = datetime.now()

            proses = request.env['kartu.proses'].search([('proses_ids', '=', int(dropdown_proses_id))], limit=1)

            if proses:
                machine = request.env['mrp.machine'].browse(int(machine_id))

                kartu = request.env['kartu.proses'].browse(int(kartu_proses_id))

                if is_manager:
                    if manual_date: 
                        try:
                            manual_date_obj = datetime.strptime(manual_date, '%Y-%m-%dT%H:%M')
                            print("manual_date_obj awal:", manual_date_obj)
                            manual_date_obj = manual_date_obj.strftime('%d/%m/%Y %H:%M:%S')
                            print("manual_date_obj kedua:", manual_date_obj)
                            manual_date_obj = datetime.strptime(manual_date_obj, '%d/%m/%Y %H:%M:%S')
                            print("manual_date_obj setelah diparse lagi:", manual_date_obj)
                        except ValueError:
                            error_message = "Please provide a valid date in the correct format (DD/MM/YYYY HH:MM:SS)."
                        
                        wip_date = kartu.wip_date
                        print("wip_date:", wip_date)

                        if isinstance(wip_date, str):
                            try:
                                wip_date = datetime.strptime(wip_date, '%Y-%m-%d %H:%M:%S')
                                print("wip_date setelah diparse:", wip_date)
                            except ValueError:
                                print("Format tanggal salah pada wip_date!")
                                error_message = "Invalid date format in WIP date!"
                        
                        if wip_date and manual_date_obj < wip_date:
                            print("Manual date cannot be earlier than the WIP date!")
                            error_message = "The manual date cannot be earlier than the WIP date!"

                    else:
                        error_message = "Please provide a valid manual date."
                    
                    tanggal_hari_ini = manual_date_obj if error_message is None else datetime.today().date()
                else:
                    manual_date_obj = tanggal_hari_ini

                    print("Date Otomoatis Hari Ini Non Manager:", manual_date_obj)

                    wip_date = kartu.wip_date
                    print("wip_date non manager:", wip_date)

                    if isinstance(wip_date, str):
                        try:
                            wip_date = datetime.strptime(wip_date, '%Y-%m-%d %H:%M:%S')
                            print("wip_date setelah diparse:", wip_date)
                        except ValueError:
                            print("Format tanggal salah pada wip_date!")
                            error_message = "Invalid date format in WIP date!"
                    
                    if wip_date and manual_date_obj < wip_date:
                        print("Manual date cannot be earlier than the WIP date!")
                        error_message = "The manual date cannot be earlier than the WIP date!"

                if error_message is None:
                    tanggal_hari_ini = manual_date_obj if error_message is None else datetime.today().date()
                    scan_successful = True

                    for proses_item in proses.proses_ids:
                        if proses_item.id == int(dropdown_proses_id):
                            proses_item.write({
                                'actual_mesin_id': machine.id,
                                'is_done': True,
                                'tanggal': tanggal_hari_ini,
                            })
                            current_proses_master_id = proses_item.proses_master_id.id
                            print("Proses Master ID dari proses_item yang dikerjakan:", current_proses_master_id)
                            print("Proses IDS(?):", proses_item.id)
                            print("Tanggal Yang Akan WIP UPDATE:", tanggal_hari_ini)

                            kartu.write({
                                'process_id': current_proses_master_id,
                                'wip_date': tanggal_hari_ini
                            })
                            
                            break 

                    kartu.write({
                        'wip_date': tanggal_hari_ini
                    })

                    test_development_proses = kartu.flowproses_ids.filtered(
                        lambda x: x.proses_master_id.id == current_proses_master_id
                    )

                    test_development_proses_id = test_development_proses.id if test_development_proses else None
                    print("ACTUAL MACHINE ID(?):", machine.id)
                    new_produksi = request.env['produksi'].create({
                        'kp_id': kartu.id,
                        'operator_id': employee.id,
                        'karu': employee.id if employee.is_karu else False,
                        'proses': current_proses_master_id,
                        'name': request.env['ir.sequence'].next_by_code('produksi.2'),
                        'test_development_proses_id': test_development_proses_id,
                        'actual_mesin_id' : machine.id,
                        'employee_id' : employee.id,
                    })
                    print("Record produksi berhasil dibuat dengan ID:", new_produksi.id)

                    proses_ids = proses.proses_ids
                    proses_data = []
                    machines_to_display = []
                    show_dropdown = False
                    dropdown_proses_id = None
                    all_done = True

                    kartu_proses_id = request.env['kartu.proses'].browse(kartu_proses_id)
                    print("INI ADAA GAK KARTU PROSES:", kartu_proses_id.name)

                    employee = request.env['hr.employee'].search([('barcode', '=', employee_barcode)], limit=1)
                    for proses in proses_ids:
                        
                        if proses.is_done:
                            status = 'Selesai'
                        elif not proses.is_done and not show_dropdown:
                            status = 'Sedang Diproses'
                            machines_to_display = proses.proses_master_id.mesin_ids
                            show_dropdown = True 
                            dropdown_proses_id = proses.id 
                            all_done = False
                        else:
                            status = 'Belum Dimulai'
                            all_done = False

                        proses_info = {
                            'proses_name': proses.proses_master_id.name,
                            'mesin_names': [mesin.name for mesin in proses.proses_master_id.mesin_ids],
                            'status': status
                        }

                        if not proses.is_done and not show_dropdown:
                            machines_to_display = proses.proses_master_id.mesin_ids
                            show_dropdown = True 
                            dropdown_proses_id = proses.id 

                        proses_data.append(proses_info)


                    return request.render('custom_module_scan.process_scanning_page', {
                        'scan_successful': scan_successful,
                        'error_message': error_message, 
                        'kartu_proses': kartu_proses_id,
                        'employee': employee,
                        'machines': machines_to_display,  
                        'proses_data': proses_data,  
                        'dropdown_proses_id' : dropdown_proses_id,
                        'partner': partner
                    })
                                    
                else:
                    print("Error terjadi, tidak menulis data ke database")

            else:
                print("Proses dengan ID %s tidak ditemukan." % dropdown_proses_id)

            if error_message:
                print("CHECK INI APA YAA:", proses.proses_ids)
                proses_ids = proses.proses_ids
                proses_data = []
                machines_to_display = []
                show_dropdown = False
                dropdown_proses_id = None
                all_done = True

                kartu_proses_id = request.env['kartu.proses'].browse(kartu_proses_id)
                print("INI ADAA GAK KARTU PROSES:", kartu_proses_id.name)

                employee = request.env['hr.employee'].search([('barcode', '=', employee_barcode)], limit=1)
                for proses in proses_ids:
                    
                    if proses.is_done:
                        status = 'Selesai'
                    elif not proses.is_done and not show_dropdown:
                        status = 'Sedang Diproses'
                        machines_to_display = proses.proses_master_id.mesin_ids
                        show_dropdown = True 
                        dropdown_proses_id = proses.id 
                        all_done = False
                    else:
                        status = 'Belum Dimulai'
                        all_done = False

                    proses_info = {
                        'proses_name': proses.proses_master_id.name,
                        'mesin_names': [mesin.name for mesin in proses.proses_master_id.mesin_ids],
                        'status': status
                    }

                    if not proses.is_done and not show_dropdown:
                        machines_to_display = proses.proses_master_id.mesin_ids
                        show_dropdown = True 
                        dropdown_proses_id = proses.id 

                    proses_data.append(proses_info)

                return request.render('custom_module_scan.process_scanning_page', {
                    'scan_successful': scan_successful,
                    'error_message': error_message,  
                    'kartu_proses': kartu_proses_id,
                    'employee': employee,
                    'machines': machines_to_display,  
                    'proses_data': proses_data,  
                    'dropdown_proses_id' : dropdown_proses_id,
                    'partner': partner
                })
                
        return request.redirect('/scan_form')
        # return request.redirect('/process_scanning?kartu_proses_id=%d&employee_barcode=%s' % (kartu_proses_id, employee_barcode)) 