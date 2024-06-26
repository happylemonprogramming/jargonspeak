# Libraries
import json
# import ssl
import time
# import uuid
import sys
from pynostr.event import Event
from pynostr.relay_manager import RelayManager
# from pynostr.filters import FiltersList, Filters
# from pynostr.message_type import ClientMessageType
from pynostr.key import PrivateKey
import os


# Environment variables
private_key = os.environ["nostrdvmprivatekey"]   

# Relays
relay_manager = RelayManager(timeout=6)
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")

# Private Key
# private_key = PrivateKey()
# private_object = PrivateKey.from_nsec(private_key)
# private_hex = private_object.hex()
# public_hex = private_object.public_key.hex()

def nostrreply(private_key,kind,content,noteID,pubkey_ref,bolt11=None, amount=None, eventInput=None, test=False, jobrequest = None):
    private_object = PrivateKey.from_nsec(private_key)
    private_hex = private_object.hex()

    # # Filters
    # filters = FiltersList([Filters(authors=[public_hex], limit=100)])

    # # Subscriptions
    # subscription_id = uuid.uuid1().hex
    # relay_manager.add_subscription_on_all_relays(subscription_id, filters)

    # Post Construction
    kind = int(kind)
    # "tags":[["e","b2..."],["p","be..."]]
    if test: 
        tags = eventInput
    elif bolt11!=None and amount!=None: # for payment request
        tags = [["status", "payment-required", "Swann DVM"], ["amount", f"{amount}", f"{bolt11}"], ["e", f"{noteID}"], ["p", f"{pubkey_ref}"]]
    elif eventInput!=None: 
        tags = [["i", f"{eventInput}", "event"]]
    elif isinstance(pubkey_ref, list): # if multiple pubkeys
        tags = [["e", f"{noteID}"]]
        for pubkey in pubkey_ref:
            tags.append(["p", f"{pubkey}"])
    else:
        tags = [["request", f"{jobrequest}"], ["e", f"{noteID}"], ["p", f"{pubkey_ref}"]]
    # Replace single quotes with double quotes
    tags = str(tags)
    tags = tags.replace("'", "\"")

    # Convert the string to a list using JSON
    print("Tags before conversion:", tags)
    tags = json.loads(tags)
    # tags = json.dumps(tags)
    print(tags)
    event = Event(
                kind = kind, 
                tags = tags,
                content = content
                )
    print(event)

    # Publish
    event.sign(private_hex)
    relay_manager.publish_event(event)
    relay_manager.run_sync()
    time.sleep(5) # allow the messages to send
    while relay_manager.message_pool.has_ok_notices():
        ok_msg = relay_manager.message_pool.get_ok_notice()
        print(ok_msg)
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        print(event_msg.event.to_dict())
    print('Event Published')
    return "Event Published"

if __name__ == '__main__':
    kind = 5250
    content = 'Builders be buildin'
    noteID = '976abdfffa674d7ddb60ec269a10241d9df2a7d815cf1df4d4a8e1eccabce550'
    pubkey_ref = 'be7358c4fe50148cccafc02ea205d80145e253889aa3958daafa8637047c840e'
    nostrreply(private_key,kind,content,noteID,pubkey_ref,eventInput=noteID)

    # from pynostr.key import PublicKey
    # pubkey = "npub1hee433872q2gen90cqh2ypwcq9z7y5ugn23etrd2l2rrwpruss8qwmrsv6"
    # pubhex = PublicKey.from_npub(pubkey).hex()
    # kind = 3
    # content = '{"wss://nostr.wine":{"write":true,"read":true},"wss://eden.nostr.land":{"write":true,"read":true},"wss://relay.damus.io":{"write":true,"read":true},"wss://nos.lol":{"write":true,"read":true}}'
    # tags = [['p', '7c3be2769c76eecd6c6e27276722dfae0d8ad201825253452153b90093c41654'], ['p', '472be9f9264eea1254f2b2f7cd2da0c319dae4fe4cd649f0424e94234dcacf97'], ['p', 'c6209b5936aea5092e677e3817b25329e1fb5f206ea8b8e97c59d4ab35ac6e0c'], ['p', 'ec6e36d5c9eb874f1db4253ef02377f7cc70697cda40fbfb24ded6b5d14cce4c'], ['p', '37359e92ece5c6fc8d5755de008ceb6270808b814ddd517d38ebeab269836c96'], ['p', '641ac8fea1478c27839fb7a0850676c2873c22aa70c6216996862c98861b7e2f'], ['p', 'b99dbca0184a32ce55904cb267b22e434823c97f418f36daf5d2dff0dd7b5c27'], ['p', '3fde182cc7e6efa69a393b16ef41b10c03928df3b96acf4f0eb03f9fca63a09a'], ['p', '4657dfe8965be8980a93072bcfb5e59a65124406db0f819215ee78ba47934b3e'], ['p', 'd7f3a2d8b777433926e2395d3159892e8479e871a800e401f047fb08ad17f32b'], ['p', 'fca0338ac5406205ff94d636ca2cabe7d483c0e4b114e7a4f26d99183679afef'], ['p', 'c1651ae9616f87373ba00af0d97dc46902564e1fc1e5b6c4083383d91e83506b'], ['p', '2aa3b5aa7798a02e00f3c3bac93c5e274198f9f3f7cd07b2dc1604afcd0e161f'], ['p', '92de68b21302fa2137b1cbba7259b8ba967b535a05c6d2b0847d9f35ff3cf56a'], ['p', '935dc9483d36f24456a9150dd3f89758e6c41fe204d85b8476a41b636af43a24'], ['p', '922945779f93fd0b3759f1157e3d9fa20f3fd24c4b8f2bcf520cacf649af776d'], ['p', '883fea4c071fda4406d2b66be21cb1edaf45a3e058050d6201ecf1d3596bbc39'], ['p', '58c741aa630c2da35a56a77c1d05381908bd10504fdd2d8b43f725efa6d23196'], ['p', '29fbc05acee671fb579182ca33b0e41b455bb1f9564b90a3d8f2f39dee3f2779'], ['p', 'fe7f6bc6f7338b76bbf80db402ade65953e20b2f23e66e898204b63cc42539a3'], ['p', '8967f290cc7749fd3d232fb7110c05db746a31fce0635aeec4e111ad8bfc810d'], ['p', '9b0d3c1f2897ee102c4336fac892c748d310f8857724870f087642a30fde30d9'], ['p', '4cdbf5bcd7f015a3ebc6853e6566732f9c11357b6e43d6b2edce742fbe9847f4'], ['p', '99bb5591c9116600f845107d31f9b59e2f7c7e09a1ff802e84f1d43da557ca64'], ['p', 'e1055729d51e037b3c14e8c56e2c79c22183385d94aadb32e5dc88092cd0fef4'], ['p', '9936a53def39d712f886ac7e2ed509ce223b534834dd29d95caba9f6bc01ef35'], ['p', '04c915daefee38317fa734444acee390a8269fe5810b2241e5e6dd343dfbecc9'], ['p', '85080d3bad70ccdcd7f74c29a44f55bb85cbcd3dd0cbb957da1d215bdb931204'], ['p', '9b00d7352b5f42ed1980fc69bfab51c3f415bde617800b44cee235a227934c3b'], ['p', 'c7617e84337c611c7d5f941b35b1ec51f2ae6e9f41aac9616092d510e1c295e0'], ['p', 'a341f45ff9758f570a21b000c17d4e53a3a497c8397f26c0e6d61e5acffc7a98'], ['p', 'bc385dfbeaa4131fefb92f84a9c50e4bc4260e2da5183f7113aecd5f1d301abf'], ['p', 'b9a537523bba2fcdae857d90d8a760de4f2139c9f90d986f747ce7d0ec0d173d'], ['p', 'ea2e3c814d08a378f8a5b8faecb2884d05855975c5ca4b5c25e2d6f936286f14'], ['p', '870744363b1a5986d6773b5706dde258c039f6d34a5ffc270915033a6a67c82c'], ['p', '3eeb3de14ec5c48c6c4c9ff80908c4186170eabb74b2a6705a7db9f9922cd61e'], ['p', 'e88a691e98d9987c964521dff60025f60700378a4879180dcbbb4a5027850411'], ['p', 'f8e6c64342f1e052480630e27e1016dce35fc3a614e60434fef4aa2503328ca9'], ['p', '6538925ebfb661f418d8c7d074bee2e8afd778701dd89070c2da936d571e55c3'], ['p', '05933d8782d155d10cf8a06f37962f329855188063903d332714fbd881bac46e'], ['p', 'b07d216f2f0422ec0252dd81a6513b8d0b0c7ef85291fbf5a85ef23f8df78fa7'], ['p', 'a5e93aef8e820cbc7ab7b6205f854b87aed4b48c5f6b30fbbeba5c99e40dcf3f'], ['p', 'aef0d6b212827f3ba1de6189613e6d4824f181f567b1205273c16895fdaf0b23'], ['p', '1989034e56b8f606c724f45a12ce84a11841621aaf7182a1f6564380b9c4276b'], ['p', '8d0d521dde92c8aaa10c3276fc5760eda765438f4885b70d096a49f969628fca'], ['p', '1bdeb7c42c558c1cc286d7b46e464acbfa83df7b58987cadfbeacc83fb4b9d91'], ['p', '0fe0b18b4dbf0e0aa40fcd47209b2a49b3431fc453b460efcf45ca0bd16bd6ac'], ['p', 'c9b19ffcd43e6a5f23b3d27106ce19e4ad2df89ba1031dd4617f1b591e108965'], ['p', '5fd8c6a375c431729a3b78e2080ffff0a1dc63f52e2a868a801151190a31f955'], ['p', '2a2c0f22aac6fe3b557e5354d643598b2635a82ccd63c342d541fa571456b2da'], ['p', '9ba8c688f091ca48de2b0f9bc998e3bc36a0092149f9201767da592849777f1c'], ['p', 'b05fbd69ff9d54d9e59502b9baa5987d08660c0166b7a58056d89f29998ed733'], ['p', '15e3a72e35cf5955f11b6c47e4d5632961c968250c15914f3c435844b06e88c2'], ['p', '32e1827635450ebb3c5a7d12c1f8e7b2b514439ac10a67eef3d9fd9c5c68e245'], ['p', '772bd267dffbff318d1a89f257c3371410111a8b89571dbbefa77af6bfa179f3'], ['p', 'c49d52a573366792b9a6e4851587c28042fb24fa5625c6d67b8c95c8751aca15'], ['p', '787338757fc25d65cd929394d5e7713cf43638e8d259e8dcf5c73b834eb851f2'], ['p', '5be6446aa8a31c11b3b453bf8dafc9b346ff328d1fa11a0fa02a1e6461f6a9b1'], ['p', '3b6a3d3bb3358836a64d1c80292b96e7698ec35a2e5ca451defa6bd3af3eeb84'], ['p', 'a305cc8926861bdde5c71bbb6fd394bb4cea6ef5f5f86402b249fc5ceb0ce220'], ['p', 'd70d50091504b992d1838822af245d5f6b3a16b82d917acb7924cef61ed4acee'], ['p', 'aa55a479ad6934d0fd78f3dbd88515cd1ca0d7a110812e711380d59df7598935'], ['p', 'd8bcfacfcd875d196251b0e9fcd6932f960e22e45d3e6cc48c898917aa97645b'], ['p', '51058f77cc511ad67002192c94ecb44835a1209453f4737076cb1076e3a7dd3f'], ['p', '3d2e51508699f98f0f2bdbe7a45b673c687fe6420f466dc296d90b908d51d594'], ['p', 'c63c5b4e21b9b1ec6b73ad0449a6a8589f6bd8542cabd9e5de6ae474b28fe806'], ['p', 'eab0e756d32b80bcd464f3d844b8040303075a13eabc3599a762c9ac7ab91f4f'], ['p', 'bf2376e17ba4ec269d10fcc996a4746b451152be9031fa48e74553dde5526bce'], ['p', 'b9003833fabff271d0782e030be61b7ec38ce7d45a1b9a869fbdb34b9e2d2000'], ['p', 'b8e6bf46e109314616fe24e6c7e265791a5f2f4ec95ae8aa15d7107ad250dc63'], ['p', '27f211f4542fd89d673cfad15b6d838cc5d525615aae8695ed1dcebc39b2dadb'], ['p', 'c037a6897df86bfd4df5496ca7e2318992b4766897fb18fbd1d347a4f4459f5e'], ['p', '0c6e9795d1bab19202b1ad6776af0e851065588fdec6fa558a5ef0afda6ce6cf'], ['p', 'df173277182f3155d37b330211ba1de4a81500c02d195e964f91be774ec96708'], ['p', '7b3f7803750746f455413a221f80965eecb69ef308f2ead1da89cc2c8912e968'], ['p', 'cedab81be42ef47dbde653f4ba7ab25ac3aa32cfc2b672ee0f89c0faf882f13e'], ['p', '59fbee7369df7713dbbfa9bbdb0892c62eba929232615c6ff2787da384cb770f'], ['p', '8ab235fe03e4efa7bf01babbca5210de7eac01aba6e630993d9b684c5eb3d84e'], ['p', '68d81165918100b7da43fc28f7d1fc12554466e1115886b9e7bb326f65ec4272'], ['p', '076161ca22da5a2ab8c74465cbf08f79f3e7e8bb31f4dc211bd94319ebade03d'], ['p', 'ca9d68eb25620fc755e1b8c76b5f155f4c7e96d99c532c109a8b36d208bdce55'], ['p', '83e818dfbeccea56b0f551576b3fd39a7a50e1d8159343500368fa085ccd964b'], ['p', '0089f11c5e3e3547a2c7276a87128cd805583e0c1247386f493d83a9d3c7405b'], ['p', 'ef151c7a380f40a75d7d1493ac347b6777a9d9b5fa0aa3cddb47fc78fab69a8b'], ['p', 'c7dccba4fe4426a7b1ea239a5637ba40fab9862c8c86b3330fe65e9f667435f6'], ['p', 'c2622c916d9b90e10a81b2ba67b19bdfc5d6be26c25756d1f990d3785ce1361b'], ['p', 'd5aaee075266c533a4c8928f98b74f88809a779491f2a9675e625e85d6ccb5e8'], ['p', 'f44291a9dad184ecb7a2fe14d72553f11b7eda875afc50bbe3514f21166b3fb5'], ['p', '43e87f5c42c5b13c193bf1e6f29740caa143ce01228ae4bd4b06254834580caa'], ['p', '66bd8fed3590f2299ef0128f58d67879289e6a99a660e83ead94feab7606fd17'], ['p', 'be1d89794bf92de5dd64c1e60f6a2c70c140abac9932418fee30c5c637fe9479'], ['p', '42b3db1ca9f73ea861cca1f5a9f74dadf97b6ff539cdf722ccae16119907dfe6'], ['p', '703e26b4f8bc0fa57f99d815dbb75b086012acc24fc557befa310f5aa08d1898'], ['p', 'bd9eb657c25b4f6cda68871ce26259d1f9bc62420487e3224905b674a710a45a'], ['p', '090254801a7e8e5085b02e711622f0dfa1a85503493af246aa42af08f5e4d2df'], ['p', '020f2d21ae09bf35fcdfb65decf1478b846f5f728ab30c5eaabcd6d081a81c3e'], ['p', 'b81f6b275ebd27a8f04ffd05dc16bc9fa329cb8d9c464bc7bdbf5068818e03c0'], ['p', '8c7c631279785d45090d29ea60020a078170057e0def3f183a5948babf4c1b33'], ['p', '8047df981a97dd41b48f554ac00e90bd62348fe65384c88ef29032d752857143'], ['p', 'e9e4276490374a0daf7759fd5f475deff6ffb9b0fc5fa98c902b5f4b2fe3bba2'], ['p', 'c7063ccd7e9adc0ddd4b77c6bfabffc8399b41e24de3a668a6ab62ede2c8aabd'], ['p', '6ad08392d1baa3f6ff7a9409e2ac5e5443587265d8b4a581c6067d88ea301584'], ['p', 'b9ceaeeb4178a549e8b0570f348b2caa4bef8933fe3323d45e3875c01919a2c2'], ['p', '1afe0c74e3d7784eba93a5e3fa554a6eeb01928d12739ae8ba4832786808e36d'], ['p', 'e41e883f1ef62485a074c1a1fa1d0a092a5d678ad49bedc2f955ab5e305ba94e'], ['p', '460c25e682fda7832b52d1f22d3d22b3176d972f60dcdc3212ed8c92ef85065c'], ['p', 'd3a15a0f5100f99efdccc68bea963383450558b1bb8b23b70a6bfa94cbb685b8'], ['p', '7e0c255fd3d0f9b48789a944baf19bf42c205a9c55199805eb13573b32137488'], ['p', '34d2f5274f1958fcd2cb2463dabeaddf8a21f84ace4241da888023bf05cc8095'], ['p', '3bf0c63fcb93463407af97a5e5ee64fa883d107ef9e558472c4eb9aaaefa459d'], ['p', '61066504617ee79387021e18c89fb79d1ddbc3e7bff19cf2298f40466f8715e9'], ['p', 'c48e29f04b482cc01ca1f9ef8c86ef8318c059e0e9353235162f080f26e14c11'], ['p', 'e1ff3bfdd4e40315959b08b4fcc8245eaa514637e1d4ec2ae166b743341be1af'], ['p', '6e1534f56fc9e937e06237c8ba4b5662bcacc4e1a3cfab9c16d89390bec4fca3'], ['p', '19fefd7f39c96d2ff76f87f7627ae79145bc971d8ab23205005939a5a913bc2f'], ['p', '4379e76bfa76a80b8db9ea759211d90bb3e67b2202f8880cc4f5ffe2065061ad'], ['p', '5df21e8ec11e21e7b710ac7d6c94427407ae69e93a7fcf0d0a3ee2fac4fdc84b'], ['p', '2af01e0d6bd1b9fbb9e3d43157d64590fb27dcfbcabe28784a5832e17befb87b'], ['p', '472f440f29ef996e92a186b8d320ff180c855903882e59d50de1b8bd5669301e'], ['p', '2779f3d9f42c7dee17f0e6bcdcf89a8f9d592d19e3b1bbd27ef1cffd1a7f98d1'], ['p', 'b0b8fbd9578ac23e782d97a32b7b3a72cda0760761359bd65661d42752b4090a'], ['p', '826e9f895b81ab41a4522268b249e68d02ca81608def562a493cee35ffc5c759'], ['p', 'b7996c183e036df27802945b80bbdc8b0bf5971b6621a86bf3569c332117f07d'], ['p', '875705d034963b8487a8246468612a854ed2b5af66be936e1e48c25ce96a750d'], ['p', '82341f882b6eabcd2ba7f1ef90aad961cf074af15b9ef44a09f9d2a8fbfbe6a2'], ['p', 'b9e76546ba06456ed301d9e52bc49fa48e70a6bf2282be7a1ae72947612023dc'], ['p', '8fe3f243e91121818107875d51bca4f3fcf543437aa9715150ec8036358939c5'], ['p', '6e468422dfb74a5738702a8823b9b28168abab8655faacb6853cd0ee15deee93'], ['p', '3b38b216f383d192a57c6d5871623ca776e06824c67117352758f976d4c16bbb'], ['p', '5a5788c56beecf470fa94e33a5610b63243dad60e03ecd75fd42d3ba4ff56733'], ['p', 'a1808558470389142e297d4729e081ab8bdff1ab50d0ebe22ffa78958f7a6ab7'], ['p', 'd61f3bc5b3eb4400efdae6169a5c17cabf3246b514361de939ce4a1a0da6ef4a'], ['p', '6c237d8b3b120251c38c230c06d9e48f0d3017657c5b65c8c36112eb15c52aeb'], ['p', '84dee6e676e5bb67b4ad4e042cf70cbd8681155db535942fcc6a0533858a7240'], ['p', 'af146f51634a5fb0abc592fbc2bed42cf740700990344a766a8999fe55eed1c6'], ['p', '693c2832de939b4af8ccd842b17f05df2edd551e59989d3c4ef9a44957b2f1fb'], ['p', '7579076d9aff0a4cfdefa7e2045f2486c7e5d8bc63bfc6b45397233e1bbfcb19'], ['p', '9579444852221038dcba34512257b66a1c6e5bdb4339b6794826d4024b3e4ce9'], ['p', '3efdaebb1d8923ebd99c9e7ace3b4194ab45512e2be79c1b7d68d9243e0d2681'], ['p', '6c535d95a8659b234d5a0805034f5f0a67e3c0ceffcc459f61f680fe944424bf'], ['p', 'dea520b22d8a7d6939889564ff3547cf3159db86a084d3d880331c4913c6e6a9'], ['p', '3ebc74907d1f928f209ef210e872cac033eaf3ff89e6853286d45d91e351ef9e'], ['p', 'c48b5cced5ada74db078df6b00fa53fc1139d73bf0ed16de325d52220211dbd5'], ['p', '5b871376476649b40ae0dcd9040aea3522991f0a8119967cddf0263184323d15'], ['p', '368f4e0027fd223fdb69b6ec6e1c06d1f027a611b1ed38eeb32493eb2878bb35'], ['p', 'fa984bd7dbb282f07e16e7ae87b26a2a7b9b90b7246a44771f0cf5ae58018f52'], ['p', '17717ad4d20e2a425cda0a2195624a0a4a73c4f6975f16b1593fc87fa46f2d58'], ['p', 'cbc5ef6b01cbd1ffa2cb95a954f04c385a936c1a86e1bb9ccdf2cf0f4ebeaccb'], ['p', 'c4eabae1be3cf657bc1855ee05e69de9f059cb7a059227168b80b89761cbc4e0'], ['p', 'ee0e01eb17fc6cb4cd2d9300d2f8945b51056514f156c6bc6d491b74496d161a'], ['p', 'edcd20558f17d99327d841e4582f9b006331ac4010806efa020ef0d40078e6da'], ['p', 'e03cfe011d81424bb60a12e9eb0cb0c9c688c34712c3794c0752e0718b369ef2'], ['p', 'd9faa7a6c2f722c439a49a1d31ba3165679dd0984dec0811c9d02bdb573ec7be'], ['p', 'e75692ec71174e698df1f3d1f5771855bcc4e6e568489d2eaad489d81064ace6'], ['p', '03a6e50be223dbb49e282764388f6f2ca8826eae8c5a427aa82bb1b61e51d5e6'], ['p', 'cbf904c0702a361911c46d79379a6a502bc3bd0b4c56d25389e62d3ebf4a7db8'], ['p', '2658362c3137eaa801fae404be36ffc80e16a61c43a891a3a046bec4b72e498a'], ['p', '148d1366a5e4672b1321adf00321778f86a2371a4bdbe99133f28df0b3d32fa1'], ['p', '1577e4599dd10c863498fe3c20bd82aafaf829a595ce83c5cf8ac3463531b09b'], ['p', '629c7b77f0dc465147dee6d8f5f04dcc9cc288f32f74ef3c70a889748283da35'], ['p', '15900613e120e4e9091daf51e6fd7d9edb7e02bc1f2ef35cdf9c580d080aac95'], ['p', '03b593ef3d95102b54bdff77728131a7c3bdfe9007b0b92cd7c4ad4a0021de25'], ['p', 'ff04a0e6cd80c141b0b55825fed127d4532a6eecdb7e743a38a3c28bf9f44609'], ['p', '17b209d34f8fd7c30fde779eb8c3b0c84f724d021ebe6007a5ba70093b2576da'], ['p', '92cbe5861cfc5213dd89f0a6f6084486f85e6f03cfeb70a13f455938116433b8'], ['p', '55f04590674f3648f4cdc9dc8ce32da2a282074cd0b020596ee033d12d385185'], ['p', '7f177706ad6e0aea75a9e3345d9ffdae67676faff249be657b596375e1ced391'], ['p', 'bef514bd58c8ceea4beb9e6b84a8d983935f7be26f49e14df68098f1ba64156e'], ['p', 'f728d9e6e7048358e70930f5ca64b097770d989ccd86854fe618eda9c8a38106'], ['p', '56a6b75373c8f7b93c53bcae86d8ffbaba9f2a1b38122054fcdb7f3bf645b727'], ['p', '604e96e099936a104883958b040b47672e0f048c98ac793f37ffe4c720279eb2'], ['p', '532d830dffe09c13e75e8b145c825718fc12b0003f61d61e9077721c7fff93cb'], ['p', 'e33fe65f1fde44c6dc17eeb38fdad0fceaf1cae8722084332ed1e32496291d42'], ['p', 'f2c96c97f6419a538f84cf3fa72e2194605e1848096e6e5170cce5b76799d400'], ['p', '4b7a381823c45acc296053f11f27735da17492d0f32a5515b51ea83bca295fb9'], ['p', 'a536ab1f7f3c0133baadbdf472b1ac7ad4b774ed432c1989284193572788bca0'], ['p', '6f35047caf7432fc0ab54a28fed6c82e7b58230bf98302bf18350ff71e10430a'], ['p', '9c612f8b770f0e3fd35cdac2bc57fcee8561e560504ea25c8b9eff8e03512b3e'], ['p', 'de885001fac7aab1a21a793b153c28ddc5a794a818fb4fb9f5ed89c33302f7d8'], ['p', '9279276bffb83cee33946e564c3600a32840269a8206d01ddf40c6432baa0bcb'], ['p', 'af2f682f512899852c6654ff065aa405a41d15e2b1cb6c9173123605744f06e6'], ['p', 'e9c0a9c12e3a04edd79afc77d89b6c6413cc942ef9e61c51e51283cbe9db0c8f'], ['p', 'e4c2fc0097894052668570909f37ae359488a7177f6a7f4b196cb7c11cbc552d'], ['p', 'da18e9860040f3bf493876fc16b1a912ae5a6f6fa8d5159c3de2b8233a0d9851'], ['p', '76c71aae3a491f1d9eec47cba17e229cda4113a0bbb6e6ae1776d7643e29cafa'], ['p', '97c70a44366a6535c145b333f973ea86dfdc2d7a99da618c40c64705ad98e322'], ['p', 'c1fc7771f5fa418fd3ac49221a18f19b42ccb7a663da8f04cbbf6c08c80d20b1'], ['p', 'eaf1a13a032ce649bc60f290a000531c4d525f6a7a28f74326972c4438682f56'], ['p', '36732cc35fe56185af1b11160a393d6c73a1fe41ddf1184c10394c28ca5d627b'], ['t', 'bounty']]

    # nostrreply(private_key,kind,content,noteID=None,pubkey_ref=None,eventInput=tags, test = True)
