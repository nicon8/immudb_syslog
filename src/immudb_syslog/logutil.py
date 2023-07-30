import json

def convert_log( row ):
    time = row[:15]
    host,prog,message = row[16:].split(maxsplit=2)
    if '[' in prog:
        prog,process = prog.split('[')
        process = process[:-2]
    else:
        proc = prog[:-1]
        process = ''

    data_field = {
        'timestamp': time,
        'hostname': host,
        'program': prog,
        'processid': process,
        'message': message
    }
    return json.dumps(data_field)


def convert_bin_log( row ):
  message = (row.split("] ", 1))[1]

  rest = row.split(" [",1)[0]
  clean = rest.split(" ")[1:5]

  data_field = {
    'timestamp': clean[0],
    'hostname': clean[1],
    'program': clean[2],
    'processid': clean[3],
    'message': message
  }
  return json.dumps(data_field)
