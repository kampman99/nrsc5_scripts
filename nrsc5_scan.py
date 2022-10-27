from easyprocess import EasyProcess # python -m pip install easyprocess
from datetime import datetime

def main():
    
    start_freq = 87.9
    count_found = 0
    timeout = 15
    
    freq = start_freq

    while freq <= 108.1:

        # Call nrsc5 and see if it can play program 0 on this frequency
        stderr = EasyProcess(f'nrsc5 {freq} 0').call(timeout = timeout).stderr

        end_freq = freq

        if 'Synchronized' in stderr:
            
            station_name = ''
            audio_prog_0 = ''
            audio_prog_1 = ''
            audio_prog_2 = ''
            audio_prog_3 = ''
            message = ''
            station_location = ''
            station_name_only = '----'
            sig_services = []
            text = ''

            output_list = stderr.splitlines()
            for line in output_list:
                if 'Station name' in line:
                    # The station name is everything after the first space
                    station_name = line.split(' ', 1)[1]
                    station_name_only = line.split(' ')[-1]
                if 'Audio program 0' in line:
                    audio_prog_0 = line.split(' ', 1)[1]
                if 'Audio program 1' in line:
                    audio_prog_0 = line.split(' ', 1)[1]
                if 'Audio program 2' in line:
                    audio_prog_0 = line.split(' ', 1)[1]
                if 'Audio program 3' in line:
                    audio_prog_0 = line.split(' ', 1)[1]
                if 'Message' in line:
                    message = line.split(' ', 1)[1]
                if 'Station location' in line:
                    station_location = line.split(' ', 1)[1]
                if 'SIG Service:' in line:
                    sig_services.append(line.split(' ', 1)[1])
                    
            text += f'    Frequency: {freq} MHz'
            text += f'    {station_name}' if station_name else '    No station name'
            text += f'    {station_location}' if station_location else '    No station location'
            text += f'    {message}' if message else '    No message'
            if audio_prog_0:
                text += f'    {audio_prog_0}'
            if audio_prog_1:
                text += f'    {audio_prog_1}'
            if audio_prog_2:
                text += f'    {audio_prog_2}'
            if audio_prog_3:
                text += f'    {audio_prog_3}'
            if sig_services:
                for service in sig_services:
                    text += f'    {service}\n'

            if text:
                print(text)

            print()

            date_time = datetime.now().strftime("%Y-%m-%d %H%M%S")
            with open(f'{freq} {station_name_only} {date_time}.txt', 'w') as f:
                f.write(stderr)
                f.write('\n')
                f.write(text)
                f.close()
            
            count_found += 1

        freq += .2
        freq = round(freq, 1)
    
    print(f'Scan {start_freq} - {end_freq} complete. {count_found} HD stations found.')


if __name__ == "__main__":
    main()