import serial
import pandas as pd
import numpy as np
import time
import struct
import random

def small_check():
    ser = serial.Serial('COM8', 9600, timeout=1)
    ser.write(b'*IDN?/n')
    identification = ser.read_until()
    ser.write(b'VSET1?/n')
    v_set = ser.read_until()
    ser.write(b'ISET1?/n')
    i_set = ser.read_until()
    print(f'VSET: {v_set}, ISET: {i_set}')
    user_input = input('Set output on?')
    if user_input == 'y' or user_input == 'Y':
        ser.write(b'OUTPUT1/n')
    else:
        ser.write(b'OUTPUT0/n')
    ser.close()


def value_to_fixed_width_string(value):
    """
    It needs a five character value


    Parameters
    ----------
    value

    Returns
    -------

    """
    value_string = f'{value:2.2f}'
    value_string = value_string.rjust(5, '0')
    return value_string


class LABPS3005DN:
    def __init__(self, com, baudrate=9600, timeout=1):
        self.df = None
        self.status = None
        self.set_v = None
        self.set_i = None
        self.on = None
        self.serial = serial.serial_for_url(com, baudrate=baudrate,
                                            timeout=timeout)
        self.serial.write(b'*IDN?/n')
        self.serial.flush()
        identification = self.serial.read_until()
        print(f'Connection: {identification}')
        self.get_status()

    def close_serial(self):
        self.serial.close()

    def read_csv(self, file='SequenceFile.csv'):
        self.df = pd.read_csv(file)

    def write_serial(self):
        while True:
            input_string = input('Serial: ')
            self.serial.write(input_string.encode())
            self.serial.flush()
            print(self.serial.read_until())

    def vset(self, value):
        value_string = value_to_fixed_width_string(value)
        v_string = b''.join([b'VSET1:', value_string.encode(), b'/n'])
        self.serial.write(v_string)
        self.serial.flush()
        self.get_status()

    def iset(self, value):
        value_string = value_to_fixed_width_string(value)
        i_string = b''.join([b'ISET1:', value_string.encode(), b'/n'])
        self.serial.write(i_string)
        self.serial.flush()
        self.get_status()

    def output_on(self):
        if not self.on:
            output_string = b'OUTPUT1/n'
            self.serial.write(output_string)
            self.serial.flush()
            self.get_status()

    def output_off(self):
        if not self.on:
            output_string = b'OUTPUT0/n'
            self.serial.write(output_string)
            self.serial.flush()
            self.get_status()

    def get_status(self, verbose=False):
        self.status = b''
        while len(self.status) == 0:
            self.serial.write(b'STATUS?/n')
            self.serial.flush()
            self.status = self.serial.read_until()
        if self.status[1] == 49:  # 49 is the binary for 1 in this encoding
            self.on = True
        else:
            self.on = False

        self.serial.write(b'VSET1?/n')
        self.serial.flush()
        self.set_v = self.serial.read_until()
        self.serial.write(b'ISET1?/n')
        self.serial.flush()
        self.set_i = self.serial.read_until()
        if verbose:
            print(f'STATUS: {self.status}, VSET: {self.set_v}, ISET: '
                  f'{self.set_i}')

    def info_csv_print(self, row):
        print(f"Step: {row['Step']:.0f}, Uset(V): {row['Uset(V)']}, Iset(A): "
              f"{row['Iset(A)']}, Duration(s): {row['Duration(s)']}")

    def follow_csv(self, repetitions=1):
        if self.df is None:
            print('No sequence file loaded')
            return

        # More checks
        self.vset(0.0)
        self.iset(0.0)
        self.output_on()

        for rep in range(repetitions):
            for index, row in self.df.iterrows():
                self.info_csv_print(row)
                self.vset(row['Uset(V)'])
                self.iset(row['Iset(A)'])
                time.sleep(row['Duration(s)'])


def check_of_class():
    lab = LABPS3005DN('COM8')
    lab.read_csv('SequenceFile.csv')
    lab.get_status(True)
    # print(value_to_fixed_width_string(1))
    lab.vset(random.uniform(0, 30))
    lab.get_status(True)
    # lab.write_serial()
    # lab.follow_csv()
    lab.close_serial()

if __name__ == '__main__':
    lab = LABPS3005DN('COM8')
    lab.read_csv('SequenceFile.csv')
    lab.follow_csv()



