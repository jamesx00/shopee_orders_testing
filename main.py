import requests
import pandas as pd
from tqdm import tqdm


host = r"http://localhost:8000"
path = r"/api/method/shopee_open_api.webhook.webhook.listener"
filename = "orders-2022-01.xlsx"


def run_tests():
	body = {}
	body['shop_id'] = 179832629
	body['code'] = 3
	body['data'] = {}
	df = pd.read_excel(filename)
	order_ids = df["หมายเลขคำสั่งซื้อ"].unique()
	successful_ids = open("success.txt").read().split('\n')
	failed_ids = open("fail.txt").read().split('\n')
	completed_ids = successful_ids + failed_ids

	for order_sn in tqdm(order_ids):
		if order_sn in completed_ids:
			continue

		body['data']['ordersn'] = order_sn
		r = requests.post(host + path, json=body)
		if r.status_code != 200:
			with open('fail.txt', 'a') as file:
				file.write(f"{order_sn}\n")
		else:
			with open('success.txt', 'a') as file:
				file.write(f"{order_sn}\n")


if __name__ == "__main__":
	run_tests()
