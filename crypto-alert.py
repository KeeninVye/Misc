import requests, sys, time, json, argparse
from slackclient import SlackClient

#Colors class to help print colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():

	LTC_a = 2.09463715
	BTC_a = 0.0325

	slack_token = "xoxp-44651723427-45506309061-283958618423-4ce528b6ca244398269e8c858021e61a"
	sc = SlackClient(slack_token)
	while True:
		ADA_r 		= requests.get("https://min-api.cryptocompare.com/data/price?fsym=ADA&tsyms=USD")
		BTC_r		= requests.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD")
		LTC_r		= requests.get("https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD")

		ADA_data 	= ADA_r.json()
		ADA_usd		= ADA_data['USD']

		BTC_data 	= BTC_r.json()
		BTC_usd		= BTC_data['USD']

		LTC_data 	= LTC_r.json()
		LTC_usd		= LTC_data['USD']

		#print USD
		#print format(BTC, '.9f')
		if ADA_usd < 0.11:
			print(bcolors.OKGREEN +"BUY!"+bcolors.ENDC)
			sc.api_call("chat.postMessage",channel="@keenin",text="BUY ADA! :tada:")
		
		if ADA_usd < 0.09:
			print(bcolors.OKGREEN +"BUY!"+bcolors.ENDC)
			sc.api_call("chat.postMessage",channel="@keenin",text="HOLY SH!T BUY ADA! :tada:")

		print bcolors.HEADER + "LTC to USD:\t"+bcolors.OKGREEN+str(LTC_usd*LTC_a)+bcolors.ENDC
		print bcolors.HEADER + "BTC to USD:\t"+bcolors.OKGREEN+str(BTC_usd*BTC_a)+bcolors.ENDC
		print bcolors.HEADER + "Total:\t\t"+bcolors.OKGREEN+str(((BTC_usd*BTC_a)+(LTC_usd*LTC_a)))+bcolors.ENDC

		time.sleep(10)

if __name__ == "__main__":
    #Parse through commandline arguments
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-c", "--config", type=str, help="Path to the configuration file.")
    #args = parser.parse_args()

    #Parse the config that was passed in
    #with open(args.config) as config_file:
    #    config = json.load(config_file)
    main()#config)
