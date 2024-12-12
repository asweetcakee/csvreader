from enum import Enum

class CountriesEnum(Enum):
    AD = {"label": "Andorra", "phone": "376", "phoneLength": 6}
    AE = {"label": "United Arab Emirates", "phone": "971", "phoneLength": 9}
    AF = {"label": "Afghanistan", "phone": "93", "phoneLength": 9}
    AG = {"label": "Antigua and Barbuda", "phone": "1-268", "phoneLength": 10}
    AI = {"label": "Anguilla", "phone": "1-264", "phoneLength": 10}
    AL = {"label": "Albania", "phone": "355", "phoneLength": 9}
    AM = {"label": "Armenia", "phone": "374", "phoneLength": 6}
    AO = {"label": "Angola", "phone": "244", "phoneLength": 9}
    AQ = {"label": "Antarctica", "phone": "672", "phoneLength": 6}
    AR = {"label": "Argentina", "phone": "54", "phoneLength": [6, 7, 8]}
    AS = {"label": "American Samoa", "phone": "1-684", "phoneLength": 10}
    AT = {"label": "Austria", "phone": "43", "phoneLength": [10, 11]}
    AU = {"label": "Australia", "phone": "61", "phoneLength": 9}
    AW = {"label": "Aruba", "phone": "297", "phoneLength": 7}
    AX = {"label": "Alland Islands", "phone": "358", "phoneLength": [7, 8, 9, 10]}
    AZ = {"label": "Azerbaijan", "phone": "994", "phoneLength": 9}
    BA = {"label": "Bosnia and Herzegovina", "phone": "387", "phoneLength": 8}
    BB = {"label": "Barbados", "phone": "1-246", "phoneLength": 10}
    BD = {"label": "Bangladesh", "phone": "880", "phoneLength": 10}
    BE = {"label": "Belgium", "phone": "32", "phoneLength": 9}
    BF = {"label": "Burkina Faso", "phone": "226", "phoneLength": 8}
    BG = {"label": "Bulgaria", "phone": "359", "phoneLength": 9}
    BH = {"label": "Bahrain", "phone": "973", "phoneLength": 8}
    BI = {"label": "Burundi", "phone": "257", "phoneLength": 8}
    BJ = {"label": "Benin", "phone": "229", "phoneLength": 8}
    BL = {"label": "Saint Barthelemy", "phone": "590", "phoneLength": 9}
    BM = {"label": "Bermuda", "phone": "1-441", "phoneLength": 10}
    BN = {"label": "Brunei Darussalam", "phone": "673", "phoneLength": 7}
    BO = {"label": "Bolivia", "phone": "591", "phoneLength": 9}
    BR = {"label": "Brazil", "phone": "55", "phoneLength": 11}
    BS = {"label": "Bahamas", "phone": "1-242", "phoneLength": 10}
    BT = {"label": "Bhutan", "phone": "975", "phoneLength": 7}
    BV = {"label": "Bouvet Island", "phone": "47", "phoneLength": 10}
    BW = {"label": "Botswana", "phone": "267", "phoneLength": 7}
    BY = {"label": "Belarus", "phone": "375", "phoneLength": 9}
    BZ = {"label": "Belize", "phone": "501", "phoneLength": 7}
    CA = {"label": "Canada", "phone": "1", "phoneLength": 10}
    CC = {"label": "Cocos (Keeling) Islands", "phone": "61", "phoneLength": 10}
    CD = {"label": "Congo, Democratic Republic of the", "phone": "243", "phoneLength": 7}
    CF = {"label": "Central African Republic", "phone": "236", "phoneLength": 8}
    CG = {"label": "Congo, Republic of the", "phone": "242", "phoneLength": 9}
    CH = {"label": "Switzerland", "phone": "41", "phoneLength": 9}
    CI = {"label": "Cote d'Ivoire", "phone": "225", "phoneLength": 8}
    CK = {"label": "Cook Islands", "phone": "682", "phoneLength": 5}
    CL = {"label": "Chile", "phone": "56", "phoneLength": 9}
    CM = {"label": "Cameroon", "phone": "237", "phoneLength": 9}
    CN = {"label": "China", "phone": "86", "phoneLength": 11}
    CO = {"label": "Colombia", "phone": "57", "phoneLength": 10}
    CR = {"label": "Costa Rica", "phone": "506", "phoneLength": 8}
    CU = {"label": "Cuba", "phone": "53", "phoneLength": 8}
    CV = {"label": "Cape Verde", "phone": "238", "phoneLength": 7}
    CW = {"label": "Curacao", "phone": "599", "phoneLength": 7}
    CX = {"label": "Christmas Island", "phone": "61", "phoneLength": 9}
    CY = {"label": "Cyprus", "phone": "357", "phoneLength": 8}
    CZ = {"label": "Czech Republic", "phone": "420", "phoneLength": 9}
    DE = {"label": "Germany", "phone": "49", "phoneLength": 10}
    DJ = {"label": "Djibouti", "phone": "253", "phoneLength": 10}
    DK = {"label": "Denmark", "phone": "45", "phoneLength": 8}
    DM = {"label": "Dominica", "phone": "1-767", "phoneLength": 10}
    DO = {"label": "Dominican Republic", "phone": "1-809", "phoneLength": 10}
    DZ = {"label": "Algeria", "phone": "213", "phoneLength": 9}
    EC = {"label": "Ecuador", "phone": "593", "phoneLength": 9}
    EE = {"label": "Estonia", "phone": "372", "phoneLength": 8}
    EG = {"label": "Egypt", "phone": "20", "phoneLength": 10}
    EH = {"label": "Western Sahara", "phone": "212", "phoneLength": 9}
    ER = {"label": "Eritrea", "phone": "291", "phoneLength": 7}
    ES = {"label": "Spain", "phone": "34", "phoneLength": 9}
    ET = {"label": "Ethiopia", "phone": "251", "phoneLength": 9}
    FI = {"label": "Finland", "phone": "358", "phoneLength": 9}
    FJ = {"label": "Fiji", "phone": "679", "phoneLength": 7}
    FK = {"label": "Falkland Islands (Malvinas)", "phone": "500", "phoneLength": 5}
    FM = {"label": "Micronesia, Federated States of", "phone": "691", "phoneLength": 7}
    FO = {"label": "Faroe Islands", "phone": "298", "phoneLength": 5}
    FR = {"label": "France", "phone": "33", "phoneLength": 9}
    GA = {"label": "Gabon", "phone": "241", "phoneLength": 7}
    GB = {"label": "United Kingdom", "phone": "44", "phoneLength": 10}
    GD = {"label": "Grenada", "phone": "1-473", "phoneLength": 10}
    GE = {"label": "Georgia", "phone": "995", "phoneLength": 9}
    GF = {"label": "French Guiana", "phone": "594", "phoneLength": 9}
    GG = {"label": "Guernsey", "phone": "44", "phoneLength": 10}
    GH = {"label": "Ghana", "phone": "233", "phoneLength": 9}
    GI = {"label": "Gibraltar", "phone": "350", "phoneLength": 8}
    GL = {"label": "Greenland", "phone": "299", "phoneLength": 6}
    GM = {"label": "Gambia", "phone": "220", "phoneLength": 7}
    GN = {"label": "Guinea", "phone": "224", "phoneLength": 9}
    GP = {"label": "Guadeloupe", "phone": "590", "phoneLength": 9}
    GQ = {"label": "Equatorial Guinea", "phone": "240", "phoneLength": 9}
    GR = {"label": "Greece", "phone": "30", "phoneLength": 10}
    GS = {"label": "South Georgia and the South Sandwich Islands", "phone": "500", "phoneLength": 5}
    GT = {"label": "Guatemala", "phone": "502", "phoneLength": 8}
    GU = {"label": "Guam", "phone": "1-671", "phoneLength": 10}
    GW = {"label": "Guinea-Bissau", "phone": "245", "phoneLength": 9}
    GY = {"label": "Guyana", "phone": "592", "phoneLength": 7}
    HK = {"label": "Hong Kong", "phone": "852", "phoneLength": 8}
    HM = {"label": "Heard Island and McDonald Islands", "phone": "672", "phoneLength": 10}
    HN = {"label": "Honduras", "phone": "504", "phoneLength": 8}
    HR = {"label": "Croatia", "phone": "385", "phoneLength": 9}
    HT = {"label": "Haiti", "phone": "509", "phoneLength": 8}
    HU = {"label": "Hungary", "phone": "36", "phoneLength": 9}
    ID = {"label": "Indonesia", "phone": "62", "phoneLength": 11}
    IE = {"label": "Ireland", "phone": "353", "phoneLength": 9}
    IL = {"label": "Israel", "phone": "972", "phoneLength": 9}
    IM = {"label": "Isle of Man", "phone": "44", "phoneLength": 10}
    IN = {"label": "India", "phone": "91", "phoneLength": 10}
    IO = {"label": "British Indian Ocean Territory", "phone": "246", "phoneLength": 7}
    IQ = {"label": "Iraq", "phone": "964", "phoneLength": 10}
    IR = {"label": "Iran, Islamic Republic of", "phone": "98", "phoneLength": 11}
    IS = {"label": "Iceland", "phone": "354", "phoneLength": 7}
    IT = {"label": "Italy", "phone": "39", "phoneLength": 10}
    JE = {"label": "Jersey", "phone": "44", "phoneLength": 10}
    JM = {"label": "Jamaica", "phone": "1-876", "phoneLength": 10}
    JO = {"label": "Jordan", "phone": "962", "phoneLength": [8,9]}
    JP = {"label": "Japan", "phone": "81", "phoneLength": None}
    KE = {"label": "Kenya", "phone": "254", "phoneLength": 10}
    KG = {"label": "Kyrgyzstan", "phone": "996", "phoneLength": 9}
    KH = {"label": "Cambodia", "phone": "855", "phoneLength": 9}
    KI = {"label": "Kiribati", "phone": "686", "phoneLength": 8}
    KM = {"label": "Comoros", "phone": "269", "phoneLength": 7}
    KN = {"label": "Saint Kitts and Nevis", "phone": "1-869", "phoneLength": 10}
    KP = {"label": "Korea, Democratic People's Republic of", "phone": "850", "phoneLength": [4,6,7,13]}
    KR = {"label": "Korea, Republic of", "phone": "82", "phoneLength": [7,8]}
    KW = {"label": "Kuwait", "phone": "965", "phoneLength": 8}
    KY = {"label": "Cayman Islands", "phone": "1-345", "phoneLength": 7}
    KZ = {"label": "Kazakhstan", "phone": "7", "phoneLength": 10}
    LA = {"label": "Lao People's Democratic Republic", "phone": "856", "phoneLength": [8,9]}
    LB = {"label": "Lebanon", "phone": "961", "phoneLength": [7,8]}
    LC = {"label": "Saint Lucia", "phone": "1-758", "phoneLength": 7}
    LI = {"label": "Liechtenstein", "phone": "423", "phoneLength": 7}
    LK = {"label": "Sri Lanka", "phone": "94", "phoneLength": 7}
    LR = {"label": "Liberia", "phone": "231", "phoneLength": [8,9]}
    LS = {"label": "Lesotho", "phone": "266", "phoneLength": 8}
    LT = {"label": "Lithuania", "phone": "370", "phoneLength": 8}
    LU = {"label": "Luxembourg", "phone": "352", "phoneLength": 9}
    LV = {"label": "Latvia", "phone": "371", "phoneLength": 8}
    LY = {"label": "Libya", "phone": "218", "phoneLength": 10}
    MA = {"label": "Morocco", "phone": "212", "phoneLength": 9}
    MC = {"label": "Monaco", "phone": "377", "phoneLength": 8}
    MD = {"label": "Moldova, Republic of", "phone": "373", "phoneLength": 8}
    ME = {"label": "Montenegro", "phone": "382", "phoneLength": 8}
    MF = {"label": "Saint Martin (French part)", "phone": "590", "phoneLength": 6}
    MG = {"label": "Madagascar", "phone": "261", "phoneLength": 7}
    MH = {"label": "Marshall Islands", "phone": "692", "phoneLength": 7}
    MK = {"label": "Macedonia, the Former Yugoslav Republic of", "phone": "389", "phoneLength": 8}
    ML = {"label": "Mali", "phone": "223", "phoneLength": 8}
    MM = {"label": "Myanmar", "phone": "95", "phoneLength": [7,10]}
    MN = {"label": "Mongolia", "phone": "976", "phoneLength": 8}
    MO = {"label": "Macao", "phone": "853", "phoneLength": 8}
    MP = {"label": "Northern Mariana Islands", "phone": "1-670", "phoneLength": 7}
    MQ = {"label": "Martinique", "phone": "596", "phoneLength": 9}
    MR = {"label": "Mauritania", "phone": "222", "phoneLength": 8}
    MS = {"label": "Montserrat", "phone": "1-664", "phoneLength": 10}
    MT = {"label": "Malta", "phone": "356", "phoneLength": 8}
    MU = {"label": "Mauritius", "phone": "230", "phoneLength": 8}
    MV = {"label": "Maldives", "phone": "960", "phoneLength": 7}
    MW = {"label": "Malawi", "phone": "265", "phoneLength": [7, 8, 9]}
    MX = {"label": "Mexico", "phone": "52", "phoneLength": 10}
    MY = {"label": "Malaysia", "phone": "60", "phoneLength": 7}
    MZ = {"label": "Mozambique", "phone": "258", "phoneLength": 12}
    NA = {"label": "Namibia", "phone": "264", "phoneLength": 7}
    NC = {"label": "New Caledonia", "phone": "687", "phoneLength": 6}
    NE = {"label": "Niger", "phone": "227", "phoneLength": 8}
    NF = {"label": "Norfolk Island", "phone": "672", "phoneLength": 6}
    NG = {"label": "Nigeria", "phone": "234", "phoneLength": 8}
    NI = {"label": "Nicaragua", "phone": "505", "phoneLength": 8}
    NL = {"label": "Netherlands", "phone": "31", "phoneLength": 9}
    NO = {"label": "Norway", "phone": "47", "phoneLength": 8}
    NP = {"label": "Nepal", "phone": "977", "phoneLength": 10}
    NR = {"label": "Nauru", "phone": "674", "phoneLength": 7}
    NU = {"label": "Niue", "phone": "683", "phoneLength": 4}
    NZ = {"label": "New Zealand", "phone": "64", "phoneLength": [8, 9]}
    OM = {"label": "Oman", "phone": "968", "phoneLength": 8}
    PA = {"label": "Panama", "phone": "507", "phoneLength": 8}
    PE = {"label": "Peru", "phone": "51", "phoneLength": 9}
    PF = {"label": "French Polynesia", "phone": "689", "phoneLength": 8}
    PG = {"label": "Papua New Guinea", "phone": "675", "phoneLength": 8}
    PH = {"label": "Philippines", "phone": "63", "phoneLength": 10}
    PK = {"label": "Pakistan", "phone": "92", "phoneLength": 10}
    PL = {"label": "Poland", "phone": "48", "phoneLength": 9}
    PM = {"label": "Saint Pierre and Miquelon", "phone": "508", "phoneLength": 6}
    PN = {"label": "Pitcairn", "phone": "870", "phoneLength": 9}
    PR = {"label": "Puerto Rico", "phone": "1", "phoneLength": 10}
    PS = {"label": "Palestine, State of", "phone": "970", "phoneLength": 9}
    PT = {"label": "Portugal", "phone": "351", "phoneLength": 9}
    PW = {"label": "Palau", "phone": "680", "phoneLength": 7}
    PY = {"label": "Paraguay", "phone": "595", "phoneLength": 9}
    QA = {"label": "Qatar", "phone": "974", "phoneLength": 8}
    RE = {"label": "Reunion", "phone": "262", "phoneLength": 10}
    RO = {"label": "Romania", "phone": "40", "phoneLength": 10}
    RS = {"label": "Serbia", "phone": "381", "phoneLength": 9}
    RU = {"label": "Russian Federation", "phone": "7", "phoneLength": 10}
    RW = {"label": "Rwanda", "phone": "250", "phoneLength": 9}
    SA = {"label": "Saudi Arabia", "phone": "966", "phoneLength": 9}
    SB = {"label": "Solomon Islands", "phone": "677", "phoneLength": 7}
    SC = {"label": "Seychelles", "phone": "248", "phoneLength": 7}
    SD = {"label": "Sudan", "phone": "249", "phoneLength": 7}
    SE = {"label": "Sweden", "phone": "46", "phoneLength": 7}
    SG = {"label": "Singapore", "phone": "65", "phoneLength": 8}
    SH = {"label": "Saint Helena", "phone": "290", "phoneLength": 4}
    SI = {"label": "Slovenia", "phone": "386", "phoneLength": 9}
    SJ = {"label": "Svalbard and Jan Mayen", "phone": "47", "phoneLength": 8}
    SK = {"label": "Slovakia", "phone": "421", "phoneLength": 9}
    SL = {"label": "Sierra Leone", "phone": "232", "phoneLength": 8}
    SM = {"label": "San Marino", "phone": "378", "phoneLength": 10}
    SN = {"label": "Senegal", "phone": "221", "phoneLength": 9}
    SO = {"label": "Somalia", "phone": "252", "phoneLength": [8, 9]}
    SR = {"label": "Suriname", "phone": "597", "phoneLength": [6, 7]}
    SS = {"label": "South Sudan", "phone": "211", "phoneLength": 7}
    ST = {"label": "Sao Tome and Principe", "phone": "239", "phoneLength": 7}
    SV = {"label": "El Salvador", "phone": "503", "phoneLength": 8}
    SX = {"label": "Sint Maarten (Dutch part)", "phone": "1-721", "phoneLength": 10}
    SY = {"label": "Syrian Arab Republic", "phone": "963", "phoneLength": 7}
    SZ = {"label": "Swaziland", "phone": "268", "phoneLength": 8}
    TC = {"label": "Turks and Caicos Islands", "phone": "1-649", "phoneLength": 10}
    TD = {"label": "Chad", "phone": "235", "phoneLength": 6}
    TF = {"label": "French Southern Territories", "phone": "262", "phoneLength": 10}
    TG = {"label": "Togo", "phone": "228", "phoneLength": 8}
    TH = {"label": "Thailand", "phone": "66", "phoneLength": 9}
    TJ = {"label": "Tajikistan", "phone": "992", "phoneLength": 9}
    TK = {"label": "Tokelau", "phone": "690", "phoneLength": 5}
    TL = {"label": "Timor-Leste", "phone": "670", "phoneLength": 7}
    TM = {"label": "Turkmenistan", "phone": "993", "phoneLength": 8}
    TN = {"label": "Tunisia", "phone": "216", "phoneLength": 8}
    TO = {"label": "Tonga", "phone": "676", "phoneLength": 5}
    TR = {"label": "Turkey", "phone": "90", "phoneLength": 9}
    TT = {"label": "Trinidad and Tobago", "phone": "1-868", "phoneLength": 10}
    TV = {"label": "Tuvalu", "phone": "688", "phoneLength": 5}
    TZ = {"label": "Tanzania, United Republic of", "phone": "255", "phoneLength": 9}
    UA = {"label": "Ukraine", "phone": "380", "phoneLength": 9}
    UG = {"label": "Uganda", "phone": "256", "phoneLength": 9}
    UM = {"label": "United States Minor Outlying Islands", "phone": "1", "phoneLength": 7}
    US = {"label": "United States", "phone": "1", "phoneLength": [10, 11]}
    UY = {"label": "Uruguay", "phone": "598", "phoneLength": 8}
    UZ = {"label": "Uzbekistan", "phone": "998", "phoneLength": 9}
    VA = {"label": "Holy See (Vatican City State)", "phone": "379", "phoneLength": 9}
    VC = {"label": "Saint Vincent and the Grenadines", "phone": "1-784", "phoneLength": 10}
    VE = {"label": "Venezuela", "phone": "58", "phoneLength": [6, 7, 9]}
    VG = {"label": "Virgin Islands, British", "phone": "1-284", "phoneLength": 10}
    VI = {"label": "Virgin Islands, U.S.", "phone": "1-340", "phoneLength": 10}
    VN = {"label": "Vietnam", "phone": "84", "phoneLength": 9}
    VU = {"label": "Vanuatu", "phone": "678", "phoneLength": 7}
    WF = {"label": "Wallis and Futuna", "phone": "681", "phoneLength": 6}
    WS = {"label": "Samoa", "phone": "685", "phoneLength": 5}
    XK = {"label": "Kosovo", "phone": "383", "phoneLength": 9}
    YE = {"label": "Yemen", "phone": "967", "phoneLength": 9}
    YT = {"label": "Mayotte", "phone": "262", "phoneLength": 10}
    ZA = {"label": "South Africa", "phone": "27", "phoneLength": 10}
    ZM = {"label": "Zambia", "phone": "260", "phoneLength": 9}
    ZW = {"label": "Zimbabwe", "phone": "263", "phoneLength": 9}

    def get_label(self):
        return self.value['label']
    
    def get_phone(self):
        return self.value['phone']
    
    def get_phoneLength(self):
        if isinstance(self.value['phoneLength'], list):
            return self.value['phoneLength']
        else:
            return [self.value['phoneLength']] if self.value['phoneLength'] is not None else []
        
    def get_region_details(region_codes):
        details = {}
        
        # In case there is a single country code that can be a String type
        if isinstance(region_codes, str):
            region_codes = [region_codes]
        
        for code in region_codes:
            try:
                region = CountriesEnum[code]
                details[code] = {
                    "label": region.get_label(),
                    "phone": region.get_phone(),
                    "phoneLength": region.get_phoneLength()
                }
            except KeyError:
                details[code] = "Region not found."
        return details