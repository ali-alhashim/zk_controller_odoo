
from odoo import http, fields as odoo_fields
from odoo.http import request
from datetime import timedelta
from pytz import timezone, UTC

import logging

_logger = logging.getLogger(__name__)

class ZkController(http.Controller):

    @http.route('/iclock/cdata', type='http', auth='none', methods=['GET'], csrf=False, cors='*')
    def heartBeat(self,**kwargs):
        """
        This method will receive
        GET /iclock/cdata?SN=BRC7201260067&options=all&language=69&pushver=2.4.0&DeviceType=middle%20east&PushOptionsFlag=1
        the device tell to server I can i send you post request
        """
        _logger.info(f"Return the response with body ok for {request.params.get('SN')}")
        # Return the response with body
        return request.make_response("OK", headers=[('Content-Type', 'text/plain')])
    


    @http.route('/iclock/devicecmd', type='http', auth='none', methods=['POST'], csrf=False, cors='*')
    def devicecmd(self,**kwargs):
        _logger.info(f"Return the response with body ok for {request.params.get('SN')}")
        # Return the response with body
        return request.make_response("OK", headers=[('Content-Type', 'text/plain')])
    
    @http.route('/iclock/getrequest', type='http', auth='none', methods=['GET'], csrf=False, cors='*')
    def getrequest(self,**kwargs):
        # Heart Beat
        _logger.info(f"Return the response with body ok for {request.params.get('SN')}")
        return request.make_response("OK", headers=[('Content-Type', 'text/plain')])

    


    @http.route('/iclock/cdata', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def zk_attendance(self, **kwargs):
        """
        This method will receive attendance data from the ZK device.
        """
        _logger.info("This method will receive attendance data from the ZK device.")
        # Extract query parameters
        serial_number = request.params.get('SN')
        table = request.params.get('table')
        stamp = request.params.get('Stamp')

        _logger.info(f"Received request from device SN: {serial_number}, Table: {table}, Stamp: {stamp}")

        # Ensure the table is ATTLOG before processing attendance logs
        if table == 'ATTLOG':
            # Get the body data (tab-separated values)
            body = request.params.get('data')
            # If the body is empty, try to get it from the raw HTTP request
            if not body:
                body = request.httprequest.data.decode('utf-8')  # Decode to string if needed


            # Log the received data
            _logger.info(f"Received attendance data: {body}")

            # Process each line in the payload
            try:
                for line in body.splitlines():
                    fields = line.split('\t')
                    if len(fields) >= 3:
                        user_id_raw = fields[0]  # Employee ID sent by the ZK device (without letters or leading zeros)
                        check_time_str = fields[1]  # Check-in/check-out time as a string
                        bio_type = fields[3]  # Biometric type (1 for fingerprint, 15 for face, etc.)

                        _logger.info(f"Processing raw user ID: {user_id_raw}, Time: {check_time_str}, Biometric Type: {bio_type}")

                    

                        # Convert check_time_str to a datetime object
                        check_time = odoo_fields.Datetime.from_string(check_time_str)
                        device_tz = timezone('Asia/Kuwait')  # Adjust based on the ZK device's time zone
                        local_time = device_tz.localize(check_time, is_dst=None)
                        utc_time = local_time.astimezone(UTC)
                        naive_utc_time = utc_time.replace(tzinfo=None)

                        # Search for the employee by matching barcodes that end with the user_id_raw
                        employee = request.env['hr.employee'].sudo().search([('barcode', 'like', '%' + user_id_raw)], limit=1)

                        if employee:
                            _logger.info(f"Matched employee: {employee.name} with barcode: {employee.barcode}")
                            
                            # Find attendance records for the same employee on the same day
                            attendance = request.env['hr.attendance'].sudo().search([
                                ('employee_id', '=', employee.id),
                                ('check_in', '>=', naive_utc_time.date()),  # Filter for the same day
                                ('check_in', '<', naive_utc_time.date() + timedelta(days=1))
                            ], limit=1)

                            # Handle Check-in if today's check-in is empty
                            if attendance and attendance.check_in:  # There is already a check-in for today
                                _logger.info(f"Employee {employee.name} has already checked in today.")
                            else:
                                # No check-in for today, create or update the check-in
                                if attendance:
                                    attendance.sudo().write({
                                        'check_in': naive_utc_time,
                                    
                                    })
                                    _logger.info(f"Updated check-in for {employee.name} at {naive_utc_time}.")
                                else:
                                    # No attendance record exists, so create a new one
                                    request.env['hr.attendance'].sudo().create({
                                        'employee_id': employee.id,
                                        'check_in': naive_utc_time,
                                        'in_mode' : 'zk-device',
                                        
                                    })
                                    _logger.info(f"Created check-in for {employee.name} at {naive_utc_time}.")

                            # Handle Check-out (if provided) and if it's a later time
                            if attendance:
                                # Update check-out if this is a later check-out
                                if not attendance.check_out or attendance.check_out < naive_utc_time:
                                    attendance.sudo().write({
                                        'check_out': naive_utc_time,
                                    
                                    })
                                    _logger.info(f"Updated check-out for {employee.name} to {naive_utc_time}.")
                            else:
                                _logger.warning(f"Received check-out for {employee.name} without a check-in.")
                        else:
                            _logger.warning(f"Employee with ID {user_id_raw} not found.")
            except Exception as e:
                _logger.warning(e)

        return "OK"




