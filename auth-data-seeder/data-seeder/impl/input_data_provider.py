
from typing import List
from model.auth_data import DemographicsModel
import csv
from dynaconf import Dynaconf
import json
from pydantic import create_model


class SeedDataReader(object):

    def __init__(self, seeder_config: Dynaconf):
        self.file_path = seeder_config.input.file_path
        self.separator = seeder_config.input.separator

    
    def read_and_parse_data(self) -> List:

        print ('Started Reading the input file.')
        data_list = []
        with open(self.file_path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='|')
            for line in csv_reader:
                line['name'] = SeedDataReader._get_json_obj(line['name'])
                line['gender'] = SeedDataReader._get_json_obj(line['gender'])
                line['addressLine1'] = SeedDataReader._get_json_obj(line['addressLine1'])
                line['addressLine2'] = SeedDataReader._get_json_obj(line['addressLine2'])
                line['addressLine3'] = SeedDataReader._get_json_obj(line['addressLine3'])
                line['city'] = SeedDataReader._get_json_obj(line['city'])
                line['province'] = SeedDataReader._get_json_obj(line['province'])
                line['region'] = SeedDataReader._get_json_obj(line['region'])
                line['zone'] = SeedDataReader._get_json_obj(line['zone'])

                data_list.append(DemographicsModel(**line))

        print ('Completed reading data from input file. Total Number of rows found: ' + str(len(data_list)))
        return data_list

    def read_and_parse_dyn_data(self) -> List:

        print ('Started Reading the input file with dynamic fields.')
        data_list = []
        with open(self.file_path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='|')
            if 'id' not in csv_reader.fieldnames:
                print ('Error: "id" column is not available in input CSV.')
                raise ValueError('"id" column is not available in input CSV')

            for line in csv_reader:
                DynamicDemoModel = create_model('DynamicDemoModel', **line)
                data_list.append(DynamicDemoModel)

        print ('Completed reading data from input file. Total Number of rows found: ' + str(len(data_list)))
        return data_list

    @staticmethod
    def _get_json_obj(field_value: str):
        if not field_value or len(field_value.strip()) == 0:
            return list()
        
        return json.loads(field_value)


        