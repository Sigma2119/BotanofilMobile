import requests
import time
import random

get_data = lambda id, password: requests.post('http://f0782959.xsph.ru/getdata.php', data={'id': id, 'password': password})

add_controller = lambda password: requests.post('http://f0782959.xsph.ru/addcontroller.php', data={'password': password})

send_command = lambda id, password, command: requests.post('http://f0782959.xsph.ru/updatecommand.php', data={'id': id, 'password': password, 'command': command}) # on_water/off_water | on_light/off_light

send_data = lambda id, password, data: requests.post('http://f0782959.xsph.ru/updatedata.php', data={'id': id, 'password': password, 'data': data})

change_password = lambda id, password, new_password: requests.post('http://f0782959.xsph.ru/updatepassword.php', data={'id': id, 'password': password, 'new_password': new_password})

update_settings = lambda id, password, settings: requests.post('http://f0782959.xsph.ru/updatesettings.php', data={'id': id, 'password': password, 'settings': settings})

if __name__ == "__main__":
    id = '2'
    password = 'admin'

    water = False
    flight = False

    while True:
        try:
            send_data(id, password, '{"hum": "' + str(random.randint(0,100)) + '", "com": "' + str(random.randint(0,100)) + '"}')

            r = get_data(id, password)
            if r.status_code == 200:
                json = r.json()
                print(json)
                
                if (str(json['Commands']['Water']) == '1' or str(json['Commands']['Water']) == '2') and water == False:
                    print('Вода включена')
                    water == True

                elif water:
                    print('Вода выключена')
                    water = False
                
                if (str(json['Commands']['Light']) == '1' or str(json['Commands']['Light']) == '2') and flight == False:
                    print('Свет включен')
                    flight = True

                elif flight:
                    print('Свет выключен')
                    flight = False

            else:
                pass
                # print(r.status_code)
            
            time.sleep(30)
        except requests.exceptions.ConnectionError:
            time.sleep(5)