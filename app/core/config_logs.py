import os
import datetime

LOG_DIR = "logs/kiotviet"

def get_log_file_name(base_name):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"{base_name}_{date_str}.log")

LOG_FILE_CUSTOMER_BASE = "processed_items_customer"
LOG_FILE_INVOICE_BASE = "processed_items_invoice"
LOG_FILE_PRODUCT_BASE = "processed_items_product"

class ProcessedItemLogger:
    def __init__(self, log_file_base):
        self.log_file_base = log_file_base
        self.update_log_file()

    def update_log_file(self):
        self.log_file = get_log_file_name(self.log_file_base)
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

    def get_last_processed_item(self):
        self.update_log_file()
        if not os.path.exists(self.log_file):
            return 0
        with open(self.log_file, "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                return int(last_line) if last_line else 0
            else:
                return 0

    def log_processed_item(self, item_id):
        self.update_log_file()
        with open(self.log_file, "a") as file:
            file.write(f"{item_id}\n")

class ProcessedItemLoggerCustomers(ProcessedItemLogger):
    def __init__(self):
        super().__init__(LOG_FILE_CUSTOMER_BASE)

class ProcessedItemLoggerInvoices(ProcessedItemLogger):
    def __init__(self):
        super().__init__(LOG_FILE_INVOICE_BASE)

class ProcessedItemLoggerProducts(ProcessedItemLogger):
    def __init__(self):
        super().__init__(LOG_FILE_PRODUCT_BASE)