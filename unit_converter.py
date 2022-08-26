# Authored by Geek Yogurt 2022-08-26
# Converting number

import re
        
def convert_unit(num,base_unit=None,out_unit=None,out_type=float):
    """
    base_unit : None
    base_unit : 'K' : Thousand
    base_unit : 'M' : Million
    base_unit : 'B' : Billion
    does not work properly on unit large than billion
    """
    # to str
    if type(num) != str:
        num = str(num);
    
    num = strip_unit(num, base_unit = base_unit );
    num = flatten(num, base_unit = base_unit);    
    
    if   out_type == str:   num = str(num);
    elif out_type == float: num = float(num);
    elif out_type == int:   num = int(num); 
    
    return num;

def strip_unit(num, base_unit=None):
    if base_unit == None:
        if re.findall(r"(?i)k",num):
            num = re.sub(r"(?i)k","",num);
            num = float(num);
            num = num * 1000;
        elif re.findall(r"(?i)m",num):
            num = re.sub(r"(?i)m","",num);
            num = float(num);
            num = num * 1000000;
        elif re.findall(r"(?i)b",num):
            num = re.sub(r"(?i)b","",num);
            num = float(num);
            num = num * 1000000000;        
        
    elif base_unit == 'K':
        if re.findall(r"(?i)k",num):
            num = re.sub(r"(?i)k","",num);
        elif re.findall(r"(?i)m",num):
            num = re.sub(r"(?i)m","",num);
            num = float(num);
            num = num * 1000;
        elif re.findall(r"(?i)b",num):
            num = re.sub(r"(?i)b","",num);
            num = float(num);
            num = num * 1000000;
                    
    elif base_unit == 'M':
        if re.findall(r"(?i)k",num):
            num = re.sub(r"(?i)k","",num);
            num = float(num);
            num = num * 0.001;
        elif re.findall(r"(?i)m",num):
            num = re.sub(r"(?i)m","",num);
        elif re.findall(r"(?i)b",num):
            num = re.sub(r"(?i)b","",num);
            num = float(num);
            num = num * 1000;
            
    elif base_unit == 'B':
        if re.findall(r"(?i)k",num):
            num = re.sub(r"(?i)k","",num);
            num = float(num);
            num = num * 0.000001;
        elif re.findall(r"(?i)m",num):
            num = re.sub(r"(?i)m","",num);
            num = float(num);
            num = num * 0.001;
        elif re.findall(r"(?i)b",num):
            num = re.sub(r"(?i)b","",num);

    else: raise KeyError("Select proper base_unit");
    
    return num;            

def flatten(num, base_unit=None):
        
    if type(num) != float:
        num = float(num);
    
    if base_unit == None:
        pass;
    elif base_unit == 'K':
        num = num * 1000;
    elif base_unit == 'M':
        num = num * 1000000;
    elif base_unit == 'B':
        num = num * 1000000000;
    else: raise KeyError("Select proper base_unit");
    
    return num;
