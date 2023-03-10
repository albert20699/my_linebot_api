import argparse
import sys
import asyncio
from ChatGPT_lite.ChatGPT import Chatbot
from flask import Flask, request

app = Flask(__name__)


async def async_main(args):
    if args.session_token is None:
        print("Please provide a session token")
        sys.exit(1)

    chat = Chatbot(args.session_token, args.bypass_node)
    await asyncio.gather(chat.wait_for_ready())

    while True:
        try:
            prompt = input("You: ")
            if prompt == "!exit":
                break
            response = await chat.ask(prompt)
            print(f"\nBot: {response['answer']}\n")
        except KeyboardInterrupt:
            break
    # Close sockets
    chat.close()
    # exit
    sys.exit(0)


def sync_main(args):
    chat = Chatbot(args.session_token, args.bypass_node)
    # Create loop
    loop = asyncio.new_event_loop()
    # Set
    asyncio.set_event_loop(loop)
    # Run
    loop.run_until_complete(chat.wait_for_ready())
    while True:
        try:
            prompt = input("You: ")
            if prompt == "!exit":
                break
            response = loop.run_until_complete(chat.ask(prompt))
            print(f"\nBot: {response['answer']}\n")
        except KeyboardInterrupt:
            break
    # Close sockets
    chat.close()
    # stop asyncio event loop
    loop.stop()
    # exit
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session_token', type=str, default=None)
    parser.add_argument('--bypass_node', type=str,
                        default="https://gpt.pawan.krd")
    parser.add_argument('--async_mode', action='store_true')
    args = parser.parse_args()
    args.session_token="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..YEszWI_4hTL50OUy.TP-6xQS32lxwSA84u1w6ITTWFQaktZOwo14Dm5le0oA4hSTBpLy_1GAfXvqYt6UpgLwWItJJXi2P96sUE5DCCZdJZ2acZxSKXTElZVof46F7wdazXxEsTJYGr7arbKSg75a44Ss4EUop0-LbXkrrQqkkOe16qLvxqDxzF6XjgRNDB7-rxx8DGsStO1UK-Byi02hZtu7Lu8ZLiz0Goxi6kplFqjIHyPUeuEL_qVSEklWB8Suqy3IdSaERg8DG8lfJBWXxinczzc3d5UrcQSCYggBdkAkGM3Jh4n9PoyT_wVwR7bWQ7KQjm29xrDYPAe91aPjze5wKYT756SWH9se9CUPwb90nm-MsNDGR5DuvGoOM8lV80FTb0ZyF8rZ2-yCKGyMz2LTaW5DRhst2WcPMB1qVL7rLcqKz6FR7HEQZV9NqPniP3rie4P7dKeCH4GNe7I60D2NlodveL8xPsS3S4cg8tFQQdVNkFNsFI4NNs_637OjUdS8JcP1d2_kggDMRjN60I5xiPIfgzHXQqjm7Hf3f5I50AcHL6c1aDr1ctnRvB99GYyLUtxYKpqIZqkzwYY9v6IPItm7iLpAkQDFvRbEikzZydB5eZpql7wRJjGMdq5EPCAPyKzvvXQ8nhZsZrD-u2UYdo2pSkui0swxGCLAzDC5Mde4qC5EACcxOanYZyoTxkdnbiwzdFXVYlsldHUW12uqqnBGGIr5zbz0uXJGLD5pHSQPWP_UxFBBGD98nax7gyEwl_DXkVcEpZI5kWc3Y-SpD7I8ye71IzOsjemecZQY9-eyH6_KU5mEBHnnpGJ6a_5mf7oMvdvhs2v-yBKeGYaYSUuoJP4E7wxQJFuEQXoB12NP6eKN12b4vh5enXCjHVHdru2IAJKNKZZjsH85gQi5IdnARyNeT8p4xCuObYFYNLCS1VSHBYNH4hVvYI2c1qQCgfCFIp-kwaCTuBDEdj1EbKVMAWB0nv7uS5QOzQbIsuZpXCLGhki1Q4SS3FXAuKxQJEJswWo86e-CX7ywBTIlJQF3COisVpn8dD1feKaktAoHbLsipNgHN6ozHHVOBmFo0fDhfCzlfDLwWIGZztvcOnpYU-NEmFi-G71r2E6ICZ1RvmrmnfVp1QptIVbNcP709BgtiH3U3SOgqpdzgMSNbUC9bUd8wPVAkakm6DU-mvfmP-ptH3b_oRvqV1PzFBycWPW883YCSBmI61QsM_DHJVKpfKbAfN53NDF0CCO1JyIIRmdYRLcx5R1E_1vJaM79HKDme9i4NwyICrYK238jkgVsCxGVPGe_xFZxJlN_SVQKNLdlcYuMyA1o8UaEBpBCHU6IFdh5zFYQE-vpjdhkzhXHQgObTyH8lwFj-CAqxTQdU1HKzqV4O16jicx-Or635CkXMv4mL7OJrowxsR0EvzrUBuMZBaN_rAN5AWLcdN7UCS_obDS5CxPpE4Nx3GwJRBK7QVcE8YLp2qbRPdo9Fe4V0JjIDQw29uLhG4alH6a1MZow57h7VaUHZ4SdA-ydOU1YaeI1txUby6jJ6MRcON2P5dgOknZLH_0_OQJ2MdV_D1_YX_joTteh8dHmSgHkvSWcI2DQDlCRoIARuC1Srw-2scoKJS8uOioAuwunu5PGmMLyQp_ypZrv0r2VvGESZ54hu-B0DpJglp8lNfUsSC4KXPH2tdC8BCE5wSDQQpFJQyyrMT_tBrv-qEDtqJTunXVbm3OKDeCmTGaRdiQcfUff9reeyLiX-lvyjv15d4GAEFb3V3ZAa7bGp1YxJhpBI9pcDkJH57PefYSxBhl-3tBIAT7yaezfrxwpqvUPtUirfUphXiQPUFZW-uMapsFIV6XAxK58fRM54GzUdrHYftxlMY1KPOwColsm-aNoLz6ttu1BFbubWtA7av2vTFIUhIMehGWaQQg2z1STfHeTTIm2Y5QHo4R6qy88uDuw9efNCor3CTXYSB_qUvIkvjckHYK_I2ixP_2iXgZfdtwUpHzAnETYCJCvT8CtmzSzMsCCZlZxcBA2DOaqO_GotF0KNO7Mlknu4s20-WIGgpCCNH3ikYXl64OMgwj5hRmj_97gXO2QMwxOfngqq6OPCJhUG7GZ8d47kYRdIA-QMjSi0ZdO5kzwfPMkZocfI7T_76XJCUpoWdukCZEevqgYBD-c4qtAz-AVkMNPKhd3zfwOzTq-s6hCjTOSG1qV5M5jK2OyIHw4fmCLUtIBpeQxXbPmv2Jd90l1jBDKTcB1qqyXXvmQIX8tQDhwzl6KF6rcvsiEnCVRS_h4nrIOuPIGT64rUmAfKvxuK-_gY1XEugKqFOLG-ck62aj-Bg8DRIXTykuiT5_hDzcWnaqodvFiH-N3B4XiXMoDTdT2bKWDkkZj2RbgBRPyHiLDKVA2qX_caVjhtHO8wLNcPOF8FNA52pyaqUWoCc4dD1yDMtKfD-hVx9YcuAxoaBdGP110RA8em8iLpLmnn-8c2_vvBwi_x2upxBWHxZCtAIOVln76OyVhdm1RIoe1XcW039YtaKu1a4aPnTQuHHZNMPRT8qBlr2jAhbCmVy0H2k9ZKba-U4wphGKB8PcexmNG932MQAHuMDdkz1NdPzQXbDZSufb5vgAjoEBa4LhUqqzpmnHIhM-oiZTDlEQHmxYnD41io5HIDtuKvehpcUR7FpVBBrQ.68k9h5qBW6jv5CL3fmhezQ"
    if args.session_token is None:
        print("Please provide a session token")
        sys.exit(1)

    print("Starting. Please wait...")
    if args.async_mode:
        asyncio.run(async_main(args))
    else:
        sync_main(args)


if __name__ == "__main__":
    main()