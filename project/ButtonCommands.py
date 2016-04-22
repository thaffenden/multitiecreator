"""
Commands to import into element creation for when the buttons are clicked.
"""
from os import startfile, path
from csv import DictWriter
from tkinter import END
from ConfigParser import PlanTypesList, ProviderList


class SetSelected(object):

    def __init__(self, new_list, og_list, selected_items):
        self.new_list = new_list
        self.og_list = og_list
        self.selected_items = selected_items

    def add_to_new_list(self):
        self.new_list.insert(END, str(self.selected_items))
        self.remove_from_old_list()

    def remove_from_old_list(self):
        remove = self.og_list.curselection()
        self.og_list.delete(remove)


class RemoveSelected(SetSelected):
    """
    Works in the same way as setting the selected, just in reverse.
    """
    def __init__(self, new_list, og_list, selected_items):
        super().__init__(new_list, og_list, selected_items)


class ClearAll(object):

    def __init__(self, new_list, og_list):
        self.new_list = new_list
        self.og_list = og_list

    def providers(self):
        self.new_list.delete(first=0, last=self.new_list.size())
        self.og_list.delete(first=0, last=self.og_list.size())
        SelectAll(new_list=self.og_list).add_providers_to_list()

    def plans(self):
        self.new_list.delete(first=0, last=self.new_list.size())
        self.og_list.delete(first=0, last=self.og_list.size())
        SelectAll(new_list=self.og_list).add_plans_to_list()


class SelectAll(object):

    def __init__(self, new_list):
        self.new_list = new_list
        self.provider_dict = ProviderList().read_config()
        self.plan_dict = PlanTypesList().read_config()

    def add_providers_to_list(self):
        print("Adding Providers")
        provider_list = list(self.provider_dict.keys())
        provider_list.sort(key=lambda x: str(x).lower())

        for item in provider_list:
            if item == "SIPP":
                item = "@SIPP"
            self.new_list.insert(END, str(item))

    def add_plans_to_list(self):
        print("Adding Plans")
        plan_list = list(self.plan_dict.keys())
        plan_list.sort(key=lambda x: str(x).lower())

        for item in plan_list:
            self.new_list.insert(END, str(item))


class Generate(object):

    def __init__(self, client_id, provider_list, plan_list):
        self.provider_dict = ProviderList().read_config()
        self.plan_dict = PlanTypesList().read_config()

        self.client_id = client_id
        self.entry_val = None

        self.provider_list = provider_list
        self.plan_list = plan_list

    def create_csv(self):
        self._verify_client_id()
        self._get_selected_providers()
        self._get_selected_plans()
        value_dict = self._create_dict()
        print(value_dict)

        header_values = ["TenantId", "ProviderName", "RefProdProviderId",
                         "PlanType", "RefPlanType2ProdSubTypeId"]

        created_file = path.abspath("{}-MULTI TIE.csv".format(self.entry_val))
        with open(created_file, 'w') as csvfile:
            writer = DictWriter(csvfile, fieldnames=header_values,
                                delimiter=',', lineterminator='\n')
            writer.writeheader()
            for row in value_dict:
                writer.writerow(row)

        startfile(created_file)

    def _verify_client_id(self):
        self.entry_val = self.client_id.get()
        if len(self.entry_val) < 4:
            raise ValueError("Please enter the client ID")
        else:
            return self.entry_val

    def _get_selected_providers(self):
        self.selected_providers = self.provider_list.get(
                0, self.provider_list.size())

    def _get_selected_plans(self):
        self.selected_plans = self.plan_list.get(0, self.plan_list.size())

    def _create_dict(self):
        csv_dict = []
        for provider in self.selected_providers:
            for plan in self.selected_plans:
                if provider == "16":
                    provider = 16
                elif provider == "@SIPP":
                    provider = "SIPP"

                csv_dict.append(
                        {"TenantId": self.entry_val,
                         "ProviderName": provider,
                         "RefProdProviderId": self.provider_dict[provider],
                         "PlanType": plan,
                         "RefPlanType2ProdSubTypeId": self.plan_dict[plan]})
        return csv_dict






