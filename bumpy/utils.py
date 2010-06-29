def _mangle_wave_id(wave_id):
    return "%s/%s" % (wave_id.split("!")[0], wave_id.split("+")[1])

def extract_wave_id(url):
    _split = url.split('/')
    if(len(_split) < 4):
        return ""
    return "%s!w+%s" % (_split[2], _split[3])

def _discover_server(wave_id):
    return wave_id.split("!")[0]

def generate_wavelet_id_from_wave_id(wave_id):
    return _discover_server(wave_id) + "!conv+root"
