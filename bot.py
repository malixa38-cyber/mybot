import requests
import time
import re
import os
import html
import json
from datetime import datetime

# ============== Configuration ==============
# --- আপনার প্রয়োজনীয় তথ্য এখানে দিন ---
BOT_TOKEN = '8400016903:AAFoa2BuZvspYrcpMVmEa8DpR_e7-5VC82w'       # আপনার বট টোকেন
CHAT_ID = '-1003061883450'             # আপনার গ্রুপের চ্যাট আইডি
SESSION_ID = '0rt2r95olkp5kef02rsifkm7hv'     # আপনার লগইন সেশন আইডি

# --- টেলিগ্রাম বাটনের জন্য তথ্য ---
CHANNEL_BUTTON_TEXT = "YOUR CHANELL NAME"     # প্রথম বাটনের লেখা
CHANNEL_USERNAME = "@pakcybertech"   # আপনার চ্যানেলের ইউজারনেম (শুধু ইউজারনেম, @ ছাড়া)

SUPPORT_BUTTON_TEXT = " Numner Chanenl"         # দ্বিতীয় বাটনের লেখা
SUPPORT_USERNAME = "SAME AS FRIST " # আপনার সাপোর্টের ইউজারনেম (শুধু ইউজারনেম, @ ছাড়া)
# ===========================================

# --- দেশের ডেটা ---
COUNTRY_DATA = {
    '93': ('Afghanistan', '🇦🇫'), '355': ('Albania', '🇦🇱'), '213': ('Algeria', '🇩🇿'), '1': ('USA', '🇺🇸'), '376': ('Andorra', '🇦🇩'), 
    '244': ('Angola', '🇦🇴'), '54': ('Argentina', '🇦🇷'), '374': ('Armenia', '🇦🇲'), '61': ('Australia', '🇦🇺'), '43': ('Austria', '🇦🇹'), 
    '994': ('Azerbaijan', '🇦🇿'), '973': ('Bahrain', '🇧🇭'), '880': ('Bangladesh', '🇧🇩'), '375': ('Belarus', '🇧🇾'), '32': ('Belgium', '🇧🇪'), 
    '501': ('Belize', '🇧🇿'), '229': ('Benin', '🇧🇯'), '975': ('Bhutan', '🇧🇹'), '591': ('Bolivia', '🇧🇴'), '387': ('Bosnia & Herzegovina', '🇧🇦'), 
    '267': ('Botswana', '🇧🇼'), '55': ('Brazil', '🇧🇷'), '673': ('Brunei', '🇧🇳'), '359': ('Bulgaria', '🇧🇬'), '226': ('Burkina Faso', '🇧🇫'), 
    '257': ('Burundi', '🇧🇮'), '855': ('Cambodia', '🇰🇭'), '237': ('Cameroon', '🇨🇲'), '235': ('Chad', '🇹🇩'), '56': ('Chile', '🇨🇱'), 
    '86': ('China', '🇨🇳'), '57': ('Colombia', '🇨🇴'), '243': ('DR Congo', '🇨🇩'), '242': ('Congo', '🇨🇬'), '506': ('Costa Rica', '🇨🇷'), 
    '385': ('Croatia', '🇭🇷'), '53': ('Cuba', '🇨🇺'), '357': ('Cyprus', '🇨🇾'), '420': ('Czechia', '🇨🇿'), '45': ('Denmark', '🇩🇰'), 
    '253': ('Djibouti', '🇩🇯'), '1809': ('Dominican Republic', '🇩🇴'), '593': ('Ecuador', '🇪🇨'), '20': ('Egypt', '🇪🇬'), '503': ('El Salvador', '🇸🇻'), 
    '240': ('Equatorial Guinea', '🇬🇶'), '291': ('Eritrea', '🇪🇷'), '372': ('Estonia', '🇪🇪'), '251': ('Ethiopia', '🇪🇹'), '679': ('Fiji', '🇫🇯'), 
    '358': ('Finland', '🇫🇮'), '33': ('France', '🇫🇷'), '241': ('Gabon', '🇬🇦'), '220': ('Gambia', '🇬🇲'), '995': ('Georgia', '🇬🇪'), 
    '49': ('Germany', '🇩🇪'), '233': ('Ghana', '🇬🇭'), '30': ('Greece', '🇬🇷'), '502': ('Guatemala', '🇬🇹'), '224': ('Guinea', '🇬🇳'), 
    '509': ('Haiti', '🇭🇹'), '504': ('Honduras', '🇭🇳'), '852': ('Hong Kong', '🇭🇰'), '36': ('Hungary', '🇭🇺'), '354': ('Iceland', '🇮🇸'), 
    '91': ('India', '🇮🇳'), '62': ('Indonesia', '🇮🇩'), '98': ('Iran', '🇮🇷'), '964': ('Iraq', '🇮🇶'), '353': ('Ireland', '🇮🇪'), 
    '972': ('Israel', '🇮🇱'), '39': ('Italy', '🇮🇹'), '1876': ('Jamaica', '🇯🇲'), '81': ('Japan', '🇯🇵'), '962': ('Jordan', '🇯🇴'), 
    '7': ('Kazakhstan', '🇰🇿'), '254': ('Kenya', '🇰🇪'), '82': ('South Korea', '🇰🇷'), '965': ('Kuwait', '🇰🇼'), '996': ('Kyrgyzstan', '🇰🇬'), 
    '856': ('Laos', '🇱🇦'), '371': ('Latvia', '🇱🇻'), '961': ('Lebanon', '🇱🇧'), '231': ('Liberia', '🇱🇷'), '218': ('Libya', '🇱🇾'), 
    '370': ('Lithuania', '🇱🇹'), '352': ('Luxembourg', '🇱🇺'), '261': ('Madagascar', '🇲🇬'), '265': ('Malawi', '🇲🇼'), '60': ('Malaysia', '🇲🇾'), 
    '960': ('Maldives', '🇲🇻'), '223': ('Mali', '🇲🇱'), '52': ('Mexico', '🇲🇽'), '373': ('Moldova', '🇲🇩'), '976': ('Mongolia', '🇲🇳'), 
    '382': ('Montenegro', '🇲🇪'), '212': ('Morocco', '🇲🇦'), '258': ('Mozambique', '🇲🇿'), '95': ('Myanmar', '🇲🇲'), '264': ('Namibia', '🇳🇦'), 
    '977': ('Nepal', '🇳🇵'), '31': ('Netherlands', '🇳🇱'), '64': ('New Zealand', '🇳🇿'), '505': ('Nicaragua', '🇳🇮'), '227': ('Niger', '🇳🇪'), 
    '234': ('Nigeria', '🇳🇬'), '47': ('Norway', '🇳🇴'), '968': ('Oman', '🇴🇲'), '92': ('Pakistan', '🇵🇰'), '507': ('Panama', '🇵🇦'), 
    '595': ('Paraguay', '🇵🇾'), '51': ('Peru', '🇵🇪'), '63': ('Philippines', '🇵🇭'), '48': ('Poland', '🇵🇱'), '351': ('Portugal', '🇵🇹'), 
    '974': ('Qatar', '🇶🇦'), '40': ('Romania', '🇷🇴'), '250': ('Rwanda', '🇷🇼'), '966': ('Saudi Arabia', '🇸🇦'), '221': ('Senegal', '🇸🇳'), 
    '381': ('Serbia', '🇷🇸'), '65': ('Singapore', '🇸🇬'), '421': ('Slovakia', '🇸🇰'), '386': ('Slovenia', '🇸🇮'), '27': ('South Africa', '🇿🇦'), 
    '34': ('Spain', '🇪🇸'), '94': ('Sri Lanka', '🇱🇰'), '249': ('Sudan', '🇸🇩'), '46': ('Sweden', '🇸🇪'), '41': ('Switzerland', '🇨🇭'), 
    '963': ('Syria', '🇸🇾'), '886': ('Taiwan', '🇹🇼'), '255': ('Tanzania', '🇹🇿'), '66': ('Thailand', '🇹🇭'), '228': ('Togo', '🇹🇬'), 
    '216': ('Tunisia', '🇹🇳'), '90': ('Turkey', '🇹🇷'), '993': ('Turkmenistan', '🇹🇲'), '256': ('Uganda', '🇺🇬'), '380': ('Ukraine', '🇺🇦'), 
    '971': ('United Arab Emirates', '🇦🇪'), '44': ('United Kingdom', '🇬🇧'), '598': ('Uruguay', '🇺🇾'), '998': ('Uzbekistan', '🇺🇿'), 
    '58': ('Venezuela', '🇻🇪'), '84': ('Vietnam', '🇻🇳'), '967': ('Yemen', '🇾🇪'), '260': ('Zambia', '🇿🇲'), '263': ('Zimbabwe', '🇿🇼')
}

LAST_MESSAGE_FILE = 'last_message_time.txt'

def get_country_info(number):
    if number.startswith('+'):
        number = number[1:]
    
    best_match_code = None
    for code in COUNTRY_DATA.keys():
        if number.startswith(code):
            if best_match_code is None or len(code) > len(best_match_code):
                best_match_code = code
    
    if best_match_code:
        return COUNTRY_DATA[best_match_code]
    return ('Unknown', '❓')

def extract_otp(message):
    match = re.search(r'(\b\d{4,8}\b)', message)
    if match:
        return match.group(1)
    return "N/A"

def mask_number(number, prefix_len=7, suffix_len=2):
    n_len = len(number)
    if n_len <= prefix_len + suffix_len:
        if n_len > prefix_len:
            return number[:prefix_len] + '★' * (n_len - prefix_len)
        return number + '★'
    
    prefix = number[:prefix_len]
    suffix = number[-suffix_len:]
    num_masked_chars = n_len - (prefix_len + suffix_len)
    masked_part = '★' * num_masked_chars
    return prefix + masked_part + suffix

def send_to_telegram(message, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps(reply_markup) if reply_markup else None
    }
    try:
        response = requests.post(url, data=params)
        response.raise_for_status()
        print("Message sent to Telegram successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")

def fetch_data():
    try:
        from_date = datetime.now().strftime('%Y-%m-%d') + " 00:00:00"
        to_date = datetime.now().strftime('%Y-%m-%d') + " 23:59:59"
        timestamp = int(time.time() * 1000)
        params = {'fdate1': from_date, 'fdate2': to_date, 'sEcho': 1, 'iDisplayStart': 0, 'iDisplayLength': 25, 'iSortCol_0': 0, 'sSortDir_0': 'desc', '_': timestamp}
        url = "http://54.37.83.141/ints/agent/res/data_smscdr.php"
        headers = {'User-Agent': 'Mozilla/5.0', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://5.37.83.141/ints/agent/SMSCDRReports'}
        cookies = {'PHPSESSID': SESSION_ID}
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    while True:
        print(f"Checking for new messages... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

        last_msg_timestamp = 0
        if os.path.exists(LAST_MESSAGE_FILE):
            with open(LAST_MESSAGE_FILE, 'r') as f:
                last_msg_timestamp = int(f.read().strip() or 0)

        data = fetch_data()

        if not data or 'aaData' not in data or not isinstance(data['aaData'], list):
            print("No valid data found. Waiting...")
            time.sleep(30)
            continue
        
        new_messages = []
        for row in data['aaData']:
            try:
                msg_timestamp = int(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').timestamp())
                if msg_timestamp > last_msg_timestamp:
                    new_messages.append({
                        'timestamp': msg_timestamp,
                        'number': row[2],
                        'platform': row[3],
                        'message': row[5],
                    })
            except (IndexError, ValueError) as e:
                print(f"Skipping a row due to parsing error: {e}")
                continue
        
        if new_messages:
            new_messages.sort(key=lambda x: x['timestamp'])
            for msg in new_messages:
                country_name, flag = get_country_info(msg['number'])
                otp = extract_otp(msg['message'])
                service = msg['platform']
                masked_number = mask_number(msg['number'])

                text = (
                    f"{flag} <b>{country_name.upper()} {service.upper()} OTP RECEIVED</b>\n\n"
                    f"☎️ <b>NUMBER:</b> <code>{masked_number}</code>\n"
                    f"🔐 <b>OTP CODE:</b> <code>{otp}</code>\n"
                    f"🧊 <b>SERVICE:</b> {service.upper()}\n"
                    f"🌍 <b>COUNTRY:</b> {flag} {country_name.upper()}\n"                                    
                    f"♨️ <b>MESSAGE:</b>\n"
                    f"<pre>{html.escape(msg['message'])}</pre>"
                )
                
                keyboard = [
                    [
                        {"text": CHANNEL_BUTTON_TEXT, "url": f"https://t.me/{CHANNEL_USERNAME}"},
                        {"text": SUPPORT_BUTTON_TEXT, "url": f"https://t.me/{SUPPORT_USERNAME}"}
                    ]
                ]
                reply_markup = {"inline_keyboard": keyboard}
                
                send_to_telegram(text, reply_markup)
                
                with open(LAST_MESSAGE_FILE, 'w') as f:
                    f.write(str(msg['timestamp']))
                
                time.sleep(1)
        else:
            print("No new messages.")

        time.sleep(30)

if __name__ == "__main__":
    main()
