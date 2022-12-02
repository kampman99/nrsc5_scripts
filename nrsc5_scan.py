from easyprocess import EasyProcess # python -m pip install easyprocess
from datetime import datetime

# US FM band 87.9 - 107.9
start_freq = 87.9
end_freq = 107.9

# How long to wait on a frequency before deciding there's no HD broadcast (seconds)
timeout = 10

date_time = datetime.now().strftime("%Y-%m-%d %H%M%S")

summary_filename = f'FM HD Radio bandscan {date_time}.txt'

def main():
    
    
    
    count_found = 0
    freq = start_freq

    summary = ''
    
    while freq <= end_freq:

        # Call nrsc5 and see if it can play program 0 on this frequency
        stderr = EasyProcess(f'nrsc5 {freq} 0').call(timeout = timeout).stderr

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
                    
            text += f'    Frequency: {freq} MHz\n'
            text += f'    {station_name}\n' if station_name else '    No station name\n'
            text += f'    {station_location}\n' if station_location else '    No station location\n'
            text += f'    {message}\n' if message else '    No message\n'
            if audio_prog_0:
                text += f'    {audio_prog_0}\n'
            if audio_prog_1:
                text += f'    {audio_prog_1}\n'
            if audio_prog_2:
                text += f'    {audio_prog_2}\n'
            if audio_prog_3:
                text += f'    {audio_prog_3}\n'
            if sig_services:
                for service in sig_services:
                    text += f'    {service}\n'

            if text:
                print(text)

            text += f'Timeout: {timeout}'

            with open(f'{freq} {station_name_only} {date_time}.txt', 'w') as f:
                f.write(stderr)
                f.write('\r\n')
                f.write(text)
                f.close()
            
            count_found += 1

            summary += text

        freq += .2
        freq = round(freq, 1)
    
    print(f'Scan {start_freq} - {end_freq} complete. {count_found} HD stations found.')

    with open(summary_filename, 'w') as f:
        f.write(f'FM HD Radio bandscan {start_freq}MHz - {end_freq}MHz. {count_found} HD stations.\n\n')
        f.write(summary)
        f.close()

if __name__ == "__main__":
    main()