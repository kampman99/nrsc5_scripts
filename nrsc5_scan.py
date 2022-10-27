from easyprocess import EasyProcess # python -m pip install easyprocess
from datetime import datetime

def main():
    
    freq = 87.9
    count_found = 0
    timeout = 15
    
    while freq <= 108.1:

        #print(f'Checking {freq}:')
        
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
                    

            print(f'    Frequency: {freq} MHz')
            print(f'    {station_name}') if station_name else print('    No station name')
            print(f'    {station_location}') if station_location else print('    No station location')
            print(f'    {message}') if message else print('    No message')
            print(f'    {audio_prog_0}') if audio_prog_0 else print('    No audio program 0')
            print(f'    {audio_prog_1}') if audio_prog_1 else print('    No audio program 1')
            print(f'    {audio_prog_2}') if audio_prog_2 else print('    No audio program 2')
            print(f'    {audio_prog_3}') if audio_prog_3 else print('    No audio program 3')
            print()

            date_time = datetime.now().strftime("%Y-%m-%d %H%M%S")
            with open(f'{freq} {station_name_only} {date_time}.txt', 'w') as f:
                f.write(stderr)
                f.close()
            
            count_found += 1


        #else:
        #    print('    no HD')

        freq += .2
        freq = round(freq, 1)
    
    print(f'Scan complete. {count_found} HD stations found.')


if __name__ == "__main__":
    main()