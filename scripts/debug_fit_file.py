#!/usr/bin/env python3
'''Debug a .fit file offline'''

from fitparse import FitFile
from fitparse.processors import StandardUnitsDataProcessor

su_processor = StandardUnitsDataProcessor()
fitfile = FitFile('./sample_data/2020-05-01-12-11-27.fit',
                  data_processor=su_processor,
                  check_crc=False)
for record in fitfile.get_messages(with_definitions=False):
    print(f"record.header.local_mesg_num: {record.header.local_mesg_num}")
    if record.mesg_type and record.mesg_type.name == 'file_id':
        manufacturer = record.get_value('manufacturer')
        product = record.get_value('garmin_product')
        print(f"device: {manufacturer} -- {product}")
    elif record.mesg_type and record.mesg_type.name == 'file_creator':
        software_version = record.get_value('software_version')
        hardware_version = record.get_value('hardware_version')
        print(f"versions: {software_version} -- {hardware_version}")
    elif record.mesg_type and record.mesg_type.name == 'event':
        event_group = record.get_value('event_group')
        timestamp = record.get_value('timestamp')
        print(f"event: {event_group} -- {timestamp}")
        for record_data in record:
            print(f" * {record_data.name}: {record_data.value}")
    elif record.mesg_type and record.mesg_type.name == 'record':
        if 'name' in record.mesg_type.__dir__():
            print(f"record.mesg_type.name: {record.mesg_type.name}")
        else:
            print(f"record.mesg_type: {record.mesg_type}")
        for record_data in record:
            if record_data.units and record_data.value is not None:
                print(f" * {record_data.name}: {record_data.value} {record_data.units}")
